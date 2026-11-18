import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time

API = "https://discord.com/api/v9"
DELAY = 1.5
MESSAGE_PAGE_SIZE = 200
MESSAGE_RENDER_BATCH_SIZE = 20

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }


def get_me(token):
    r = requests.get(f"{API}/users/@me", headers=headers(token))
    if r.status_code == 401:
        raise ValueError("Invalid token.")
    r.raise_for_status()
    return r.json()


def get_dms(token):
    r = requests.get(f"{API}/users/@me/channels", headers=headers(token))
    r.raise_for_status()
    return [c for c in r.json() if c.get("type") in (1, 3)]


def get_messages(token, channel_id, before=None):
    params = {"limit": 100}
    if before:
        params["before"] = before
    r = requests.get(f"{API}/channels/{channel_id}/messages",
                     headers=headers(token), params=params)
    if r.status_code in (403, 404):
        return []
    r.raise_for_status()
    return r.json()


def delete_message(token, channel_id, msg_id):
    r = requests.delete(f"{API}/channels/{channel_id}/messages/{msg_id}",
                        headers=headers(token))
    return r.status_code in (200, 204)


def ch_name(ch):
    if ch.get("type") == 3:
        return ch.get("name") or "Group DM"
    recipients = ch.get("recipients", [])
    if recipients:
        u = recipients[0]
        return u.get("global_name") or u.get("username") or "Unknown"
    return f"Channel {ch['id']}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Discord DM Deleter")
        self.geometry("1200x750")
        self.minsize(900, 600)

        self.token = ""
        self.my_id = ""
        self.channels = []
        self.all_messages = []
        self.filtered_messages = []
        self.message_page = 0
        self._render_generation = 0
        self.displayed = {}
        self.selected_channel = None
        self.checked = set()
        self.deleting = False

        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ── LOGIN ────────────────────────────────────────────────
    def show_login(self):
        self.clear()

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.pack(fill="both", expand=True)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(outer, width=520, corner_radius=16)
        card.grid(row=0, column=0)
        card.grid_propagate(False)

        ctk.CTkLabel(card, text="⚔  Discord DM Deleter",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(36, 4))
        ctk.CTkLabel(card, text="Paste your Discord user token to continue",
                     font=ctk.CTkFont(size=13),
                     text_color="gray70").pack(pady=(0, 24))

        ctk.CTkLabel(card, text="Token", font=ctk.CTkFont(size=12, weight="bold"),
                     anchor="w").pack(padx=40, fill="x")

        self.token_entry = ctk.CTkEntry(card, width=440, height=42,
                                        show="•", placeholder_text="Paste token here…",
                                        font=ctk.CTkFont(family="Courier", size=12))
        self.token_entry.pack(padx=40, pady=(4, 8))
        self.token_entry.bind("<Return>", lambda e: self.do_login())

        self.show_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(card, text="Show token", variable=self.show_var,
                        command=self.toggle_show,
                        font=ctk.CTkFont(size=11)).pack(padx=40, anchor="w")

        self.login_msg = ctk.CTkLabel(card, text="",
                                      font=ctk.CTkFont(size=11),
                                      text_color="#f38ba8")
        self.login_msg.pack(pady=(8, 0))

        self.login_btn = ctk.CTkButton(card, text="Login", width=200, height=42,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       command=self.do_login)
        self.login_btn.pack(pady=(12, 10))

        # Token instructions
        hint_box = ctk.CTkFrame(card, fg_color=("gray85", "gray20"), corner_radius=10)
        hint_box.pack(padx=40, pady=(8, 36), fill="x")

        ctk.CTkLabel(hint_box, text="How to get your token:",
                     font=ctk.CTkFont(size=11, weight="bold"), anchor="w").pack(
            padx=14, pady=(10, 2), anchor="w")
        steps = [
            "1. Open discord.com/app in Chrome",
            "2. Press F12 → Network tab",
            "3. Send any message, click the 'messages' request",
            "4. Scroll to Request Headers",
            "5. Copy the value next to 'authorization'",
        ]
        for s in steps:
            ctk.CTkLabel(hint_box, text=s, font=ctk.CTkFont(size=11),
                         text_color="gray60", anchor="w").pack(
                padx=14, anchor="w")
        ctk.CTkLabel(hint_box, text="", height=8).pack()

        self.token_entry.focus()

    def toggle_show(self):
        self.token_entry.configure(show="" if self.show_var.get() else "•")

    def do_login(self):
        token = self.token_entry.get().strip()
        if not token:
            self.login_msg.configure(text="Token cannot be empty.")
            return
        self.login_btn.configure(state="disabled", text="Connecting…")
        self.login_msg.configure(text="", text_color="#f38ba8")

        def run():
            try:
                me = get_me(token)
                dms = get_dms(token)
                self.token = token
                self.my_id = me["id"]
                self.channels = dms
                self.after(0, self.show_main)
            except ValueError as e:
                self.after(0, lambda: self.login_msg.configure(text=str(e)))
                self.after(0, lambda: self.login_btn.configure(state="normal", text="Login"))
            except Exception as e:
                self.after(0, lambda: self.login_msg.configure(text=f"Error: {e}"))
                self.after(0, lambda: self.login_btn.configure(state="normal", text="Login"))

        threading.Thread(target=run, daemon=True).start()

    # ── MAIN SCREEN ──────────────────────────────────────────
    def show_main(self):
        self.clear()

        # ── Sidebar ──
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="Conversations",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(padx=14, pady=(18, 6), anchor="w")

        self.ch_search = ctk.CTkEntry(sidebar, placeholder_text="Search…", height=34)
        self.ch_search.pack(padx=10, pady=(0, 8), fill="x")
        self.ch_search.bind("<KeyRelease>", self.filter_channels)

        self.ch_list_frame = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        self.ch_list_frame.pack(fill="both", expand=True, padx=4)

        self.ch_buttons = []
        self.render_channel_list(self.channels)

        # ── Right panel ──
        right = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray95", "gray17"))
        right.pack(side="left", fill="both", expand=True)

        # Top bar
        top = ctk.CTkFrame(right, height=56, corner_radius=0,
                           fg_color=("gray88", "gray22"))
        top.pack(fill="x")
        top.pack_propagate(False)

        self.ch_title = ctk.CTkLabel(top, text="← Select a conversation",
                                     font=ctk.CTkFont(size=15, weight="bold"))
        self.ch_title.pack(side="left", padx=16)

        btn_row = ctk.CTkFrame(top, fg_color="transparent")
        btn_row.pack(side="right", padx=10)

        ctk.CTkButton(btn_row, text="Select All", width=100, height=32,
                      fg_color=("gray75", "gray35"),
                      hover_color=("gray65", "gray45"),
                      command=self.select_all).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Deselect All", width=110, height=32,
                      fg_color=("gray75", "gray35"),
                      hover_color=("gray65", "gray45"),
                      command=self.deselect_all).pack(side="left", padx=4)
        self.del_btn = ctk.CTkButton(btn_row, text="🗑  Delete Selected",
                                     width=150, height=32,
                                     fg_color="#ed4245", hover_color="#c03537",
                                     font=ctk.CTkFont(weight="bold"),
                                     command=self.delete_selected)
        self.del_btn.pack(side="left", padx=4)

        # Filter bar
        filter_row = ctk.CTkFrame(right, height=46, fg_color="transparent")
        filter_row.pack(fill="x", padx=12, pady=(8, 0))

        ctk.CTkLabel(filter_row, text="Filter:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.msg_filter = ctk.CTkEntry(filter_row, width=240, height=32,
                                       placeholder_text="Search messages…")
        self.msg_filter.pack(side="left", padx=8)
        self.msg_filter.bind("<KeyRelease>", self.apply_filter)

        self.mine_only = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(filter_row, text="Only my messages", variable=self.mine_only,
                        command=self.apply_filter,
                        font=ctk.CTkFont(size=12)).pack(side="left")

        self.load_all_btn = ctk.CTkButton(filter_row, text="Load All ⏬", width=110, height=32,
                                          fg_color=("gray65", "gray40"),
                                          hover_color=("gray55", "gray50"),
                                          command=self.load_all, state="disabled")
        self.load_all_btn.pack(side="right", padx=(0, 4))

        self.load_more_btn = ctk.CTkButton(filter_row, text="Load More ↓", width=110, height=32,
                                           command=self.load_more, state="disabled")
        self.load_more_btn.pack(side="right")

        # Message list (scrollable)
        self.msg_frame = ctk.CTkScrollableFrame(right, fg_color="transparent",
                                                label_text="")
        self.msg_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Header row
        hdr = ctk.CTkFrame(self.msg_frame, fg_color=("gray82", "gray25"), height=32)
        hdr.pack(fill="x", pady=(0, 2))
        ctk.CTkLabel(hdr, text="✓", width=30, font=ctk.CTkFont(size=12)).pack(side="left", padx=4)
        ctk.CTkLabel(hdr, text="Time", width=130, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(hdr, text="Message", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=8)

        self.msg_rows = []

        # Keep the number of live Tk widgets bounded for very large histories.
        page_nav = ctk.CTkFrame(right, fg_color="transparent")
        page_nav.pack(fill="x", padx=12, pady=(0, 4))
        self.prev_page_btn = ctk.CTkButton(
            page_nav, text="← Previous", width=100, command=self.previous_page
        )
        self.prev_page_btn.pack(side="left")
        self.page_label = ctk.CTkLabel(page_nav, text="No messages")
        self.page_label.pack(side="left", padx=12)
        self.next_page_btn = ctk.CTkButton(
            page_nav, text="Next →", width=100, command=self.next_page
        )
        self.next_page_btn.pack(side="left")

        # Status bar
        self.status = ctk.CTkLabel(right, text="Select a conversation to load messages.",
                                   font=ctk.CTkFont(size=11), text_color="gray55",
                                   anchor="w")
        self.status.pack(fill="x", padx=14, pady=(0, 8))

    def render_channel_list(self, channels):
        for w in self.ch_list_frame.winfo_children():
            w.destroy()
        self.ch_buttons = []
        for ch in channels:
            name = ch_name(ch)
            btn = ctk.CTkButton(self.ch_list_frame, text=name, anchor="w",
                                height=36, corner_radius=8,
                                fg_color="transparent",
                                hover_color=("gray80", "gray30"),
                                text_color=("gray10", "gray90"),
                                font=ctk.CTkFont(size=12),
                                command=lambda c=ch: self.select_channel(c))
            btn.pack(fill="x", pady=1)
            self.ch_buttons.append((btn, ch))

    def filter_channels(self, *_):
        q = self.ch_search.get().lower()
        filtered = [c for c in self.channels if q in ch_name(c).lower()]
        self.render_channel_list(filtered)

    def select_channel(self, ch):
        self.selected_channel = ch
        self.all_messages = []
        self.checked = set()
        self.ch_title.configure(text=ch_name(ch))
        self.load_more_btn.configure(state="disabled")
        self.load_all_btn.configure(state="disabled")
        self.update_status("Loading messages…")
        self.clear_msg_rows()
        threading.Thread(target=self._fetch_msgs, args=(ch["id"], None), daemon=True).start()

    def _fetch_msgs(self, cid, before):
        try:
            msgs = get_messages(self.token, cid, before)
            self.after(0, lambda: self._on_msgs(msgs, before is not None))
        except Exception as e:
            self.after(0, lambda err=str(e): self.update_status(f"Error: {err}"))

    def _on_msgs(self, msgs, appended):
        if not appended:
            self.all_messages = msgs
        else:
            self.all_messages.extend(msgs)
        has_more = len(msgs) == 100
        self.load_more_btn.configure(state="normal" if has_more else "disabled")
        self.load_all_btn.configure(state="normal" if has_more else "disabled")
        self.apply_filter()

    def load_more(self):
        if not self.all_messages or not self.selected_channel:
            return
        oldest = self.all_messages[-1]["id"]
        self.update_status("Loading older messages…")
        threading.Thread(target=self._fetch_msgs,
                         args=(self.selected_channel["id"], oldest), daemon=True).start()

    def load_all(self):
        if not self.selected_channel:
            return
        self.load_more_btn.configure(state="disabled")
        self.load_all_btn.configure(state="disabled", text="Loading…")
        self.update_status("Loading all messages — please wait…")

        cid = self.selected_channel["id"]

        def run():
            batch_count = 0
            while True:
                before = self.all_messages[-1]["id"] if self.all_messages else None
                try:
                    msgs = get_messages(self.token, cid, before)
                except Exception as e:
                    self.after(0, lambda err=e: self.update_status(f"Error: {err}"))
                    break
                if not msgs:
                    break
                self.all_messages.extend(msgs)
                batch_count += len(msgs)
                total = len(self.all_messages)
                self.after(0, lambda t=total: self.update_status(f"Loaded {t} messages so far…"))
                if len(msgs) < 100:
                    break
                time.sleep(0.3)  # small pause to avoid rate limiting

            self.after(0, self._on_load_all_done)

        threading.Thread(target=run, daemon=True).start()

    def _on_load_all_done(self):
        self.load_all_btn.configure(state="disabled", text="Load All ⏬")
        self.load_more_btn.configure(state="disabled")
        self.apply_filter()

    def apply_filter(self, *_):
        q = self.msg_filter.get().lower()
        only_mine = self.mine_only.get()
        filtered = []
        for m in self.all_messages:
            if only_mine and m["author"]["id"] != self.my_id:
                continue
            if q and q not in m.get("content", "").lower():
                continue
            filtered.append(m)
        self.filtered_messages = filtered
        self.message_page = 0
        self.render_messages()

    def clear_msg_rows(self):
        self._render_generation += 1
        for row_frame in self.msg_rows:
            row_frame.destroy()
        self.msg_rows = []
        self.displayed = {}

    def previous_page(self):
        if self.message_page > 0:
            self.message_page -= 1
            self.render_messages()

    def next_page(self):
        start = (self.message_page + 1) * MESSAGE_PAGE_SIZE
        if start < len(self.filtered_messages):
            self.message_page += 1
            self.render_messages()

    def render_messages(self):
        self.clear_msg_rows()
        start = self.message_page * MESSAGE_PAGE_SIZE
        end = min(start + MESSAGE_PAGE_SIZE, len(self.filtered_messages))
        self._page_messages = self.filtered_messages[start:end]
        page_count = max(1, (len(self.filtered_messages) + MESSAGE_PAGE_SIZE - 1) // MESSAGE_PAGE_SIZE)
        self.page_label.configure(
            text=f"Page {self.message_page + 1} of {page_count} · {len(self.filtered_messages)} match"
        )
        self.prev_page_btn.configure(
            state="normal" if self.message_page > 0 else "disabled"
        )
        self.next_page_btn.configure(
            state="normal" if end < len(self.filtered_messages) else "disabled"
        )
        self._render_index = 0
        generation = self._render_generation
        if self._page_messages:
            self.update_status(f"Rendering 0/{len(self._page_messages)} messages…")
            self.after(0, lambda g=generation: self._render_message_batch(g))
        else:
            self.update_status(self._message_count_status(0))

    def _message_count_status(self, shown):
        return (
            f"{shown} shown | {len(self.all_messages)} loaded | "
            f"{len(self.checked)} selected"
        )

    def _render_message_batch(self, generation):
        if generation != self._render_generation:
            return
        stop = min(self._render_index + MESSAGE_RENDER_BATCH_SIZE, len(self._page_messages))
        for m in self._page_messages[self._render_index:stop]:
            mid = m["id"]
            ts = m.get("timestamp", "")[:16].replace("T", " ")
            content = m.get("content", "") or "[attachment/embed]"
            is_mine = m["author"]["id"] == self.my_id

            row = ctk.CTkFrame(
                self.msg_frame,
                corner_radius=6,
                height=36,
                fg_color=("gray88", "gray23") if is_mine else ("gray92", "gray20"),
            )
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            chk_var = ctk.BooleanVar(value=mid in self.checked)
            chk = ctk.CTkCheckBox(
                row,
                text="",
                variable=chk_var,
                width=30,
                state="normal" if is_mine else "disabled",
                command=lambda mv=mid, v=chk_var: self.toggle_check(mv, v),
            )
            chk.pack(side="left", padx=6)
            ctk.CTkLabel(
                row, text=ts, width=130,
                font=ctk.CTkFont(size=11), text_color="gray50",
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=content[:180],
                font=ctk.CTkFont(size=12),
                text_color=("gray10", "gray90") if is_mine else "gray50",
                anchor="w",
            ).pack(side="left", padx=8, fill="x", expand=True)

            self.msg_rows.append(row)
            self.displayed[mid] = {"msg": m, "chk_var": chk_var, "row": row}

        self._render_index = stop
        if stop < len(self._page_messages):
            self.update_status(f"Rendering {stop}/{len(self._page_messages)} messages…")
            self.after(1, lambda g=generation: self._render_message_batch(g))
        else:
            self.update_status(self._message_count_status(stop))

    def toggle_check(self, mid, var):
        if var.get():
            self.checked.add(mid)
        else:
            self.checked.discard(mid)
        self.update_status_count()

    def select_all(self):
        for mid, d in self.displayed.items():
            if d["msg"]["author"]["id"] == self.my_id:
                d["chk_var"].set(True)
                self.checked.add(mid)
        self.update_status_count()

    def deselect_all(self):
        for mid, d in self.displayed.items():
            d["chk_var"].set(False)
        self.checked.clear()
        self.update_status_count()

    def update_status_count(self):
        self.update_status(f"{len(self.displayed)} shown | {len(self.all_messages)} loaded | {len(self.checked)} selected")

    def update_status(self, text):
        self.status.configure(text=text)

    def delete_selected(self):
        if not self.checked:
            messagebox.showinfo("Nothing selected", "Check some messages first.")
            return
        if self.deleting:
            return
        count = len(self.checked)
        ok = messagebox.askyesno("Confirm Delete",
                                 f"Permanently delete {count} message(s)?\n\n"
                                 f"1.5s delay between deletions. Cannot be undone.")
        if not ok:
            return

        to_delete = list(self.checked)
        cid = self.selected_channel["id"]
        self.deleting = True
        self.del_btn.configure(state="disabled", text="Deleting…")

        def run():
            done = 0
            failed = 0
            for mid in to_delete:
                ok = delete_message(self.token, cid, mid)
                if ok:
                    done += 1
                    self.after(0, lambda m=mid, d=done, t=len(to_delete): self.on_deleted(m, d, t))
                else:
                    failed += 1
                time.sleep(DELAY)
            self.after(0, lambda: self.on_done(done, failed))

        threading.Thread(target=run, daemon=True).start()

    def on_deleted(self, mid, done, total):
        self.checked.discard(mid)
        if mid in self.displayed:
            self.displayed[mid]["row"].destroy()
            del self.displayed[mid]
        self.update_status(f"Deleting… {done}/{total}")

    def on_done(self, done, failed):
        self.deleting = False
        self.del_btn.configure(state="normal", text="🗑  Delete Selected")
        msg = f"Done. {done} message(s) deleted."
        if failed:
            msg += f" {failed} failed."
        self.update_status(msg)
        messagebox.showinfo("Complete", msg)


if __name__ == "__main__":
    app = App()
    app.mainloop()
