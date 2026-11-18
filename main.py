#!/usr/bin/env python3
"""
Discord DM Deleter - Kivy Android Version
A mobile-friendly Discord DM cleaner built with Kivy/KivyMD.
"""

import os
import sys
import threading
import time
import json
import requests
from functools import partial

# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import platform

# KivyMD imports (for Material Design components)
try:
    from kivymd.app import MDApp
    from kivymd.uix.toolbar import MDTopAppBar
    from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.card import MDCard
    from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.selectioncontrol import MDCheckbox
    from kivymd.uix.progressbar import MDProgressBar
    from kivymd.uix.snackbar import MDSnackbar
    from kivymd.uix.label import MDLabel
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.scrollview import MDScrollView
    from kivymd.icon_definitions import md_icons
    KIVYMD_AVAILABLE = True
except ImportError:
    KIVYMD_AVAILABLE = False

# Constants
API = "https://discord.com/api/v9"
DELAY = 1.5

# KV Language UI Definition
KV = '''
<MessageRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(56)
    padding: dp(8), dp(4)
    spacing: dp(8)
    
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8),]
    
    MDCheckbox:
        id: checkbox
        size_hint_x: None
        width: dp(48)
        active: root.checked
        on_active: root.on_checkbox_active(self.active)
        disabled: not root.is_mine
        opacity: 1 if root.is_mine else 0.4
    
    MDLabel:
        id: time_label
        text: root.timestamp
        size_hint_x: None
        width: dp(120)
        font_size: sp(12)
        theme_text_color: 'Hint'
        halign: 'center'
        valign: 'middle'
    
    MDLabel:
        id: content_label
        text: root.content
        font_size: sp(13)
        theme_text_color: 'Primary' if root.is_mine else 'Secondary'
        halign: 'left'
        valign: 'middle'
        shorten: True
        shorten_from: 'right'

<ChannelButton@Button>:
    size_hint_y: None
    height: dp(48)
    background_normal: ''
    background_color: 0, 0, 0, 0
    text_size: self.width - dp(16), None
    halign: 'left'
    valign: 'middle'
    padding: dp(12), dp(8)
    font_size: sp(14)
    color: 1, 1, 1, 1
    
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8),]

<LoginScreen>:
    name: 'login'
    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.backgroundColor
        
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(24)
                spacing: dp(16)
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: min(root.width * 0.9, dp(480))
                
                MDLabel:
                    text: '🗑️ Discord DM Deleter'
                    font_style: 'H5'
                    halign: 'center'
                    size_hint_y: None
                    height: self.texture_size[1] + dp(16)
                
                MDLabel:
                    text: 'Enter your Discord user token to continue'
                    font_style: 'Body1'
                    halign: 'center'
                    theme_text_color: 'Hint'
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8)
                
                MDCard:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(16)
                    elevation: 2
                    radius: [dp(16),]
                    size_hint_y: None
                    height: dp(380)
                    
                    MDLabel:
                        text: 'Token'
                        font_style: 'Subtitle1'
                        theme_text_color: 'Primary'
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDTextField:
                        id: token_field
                        hint_text: 'Paste token here...'
                        password: True
                        mode: 'fill'
                        font_size: sp(13)
                        on_text_validate: root.do_login()
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: dp(48)
                        spacing: dp(12)
                        
                        MDCheckbox:
                            id: show_checkbox
                            size_hint_x: None
                            width: dp(48)
                            on_active: root.toggle_show(self.active)
                        
                        MDLabel:
                            text: 'Show token'
                            font_style: 'Body2'
                            theme_text_color: 'Secondary'
                            valign: 'middle'
                    
                    MDLabel:
                        id: error_label
                        text: ''
                        font_style: 'Caption'
                        theme_text_color: 'Error'
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDRaisedButton:
                        id: login_button
                        text: 'Login'
                        size_hint_y: None
                        height: dp(48)
                        font_size: sp(15)
                        on_release: root.do_login()
                    
                    MDLabel:
                        text: 'How to get your token:'
                        font_style: 'Subtitle2'
                        theme_text_color: 'Primary'
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(4)
                        size_hint_y: None
                        height: dp(120)
                        
                        MDLabel:
                            text: '1. Open discord.com in Chrome'
                            font_style: 'Caption'
                            theme_text_color: 'Hint'
                            halign: 'left'
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            text: '2. Press F12 → Network tab'
                            font_style: 'Caption'
                            theme_text_color: 'Hint'
                            halign: 'left'
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            text: '3. Send any message, click "messages" request'
                            font_style: 'Caption'
                            theme_text_color: 'Hint'
                            halign: 'left'
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            text: '4. Copy "authorization" header value'
                            font_style: 'Caption'
                            theme_text_color: 'Hint'
                            halign: 'left'
                            size_hint_y: None
                            height: self.texture_size[1]

<MainScreen>:
    name: 'main'
    
    MDBoxLayout:
        orientation: 'horizontal'
        
        # Sidebar - Channels
        MDCard:
            id: sidebar
            orientation: 'vertical'
            size_hint_x: None
            width: dp(280)
            elevation: 2
            radius: 0
            md_bg_color: app.theme_cls.surfaceColor
            
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(56)
                padding: dp(16)
                spacing: dp(12)
                
                MDIconButton:
                    icon: 'menu'
                    on_release: root.toggle_sidebar()
                    theme_text_color: 'Custom'
                    text_color: app.theme_cls.primaryColor
                
                MDLabel:
                    text: 'Conversations'
                    font_style: 'H6'
                    valign: 'middle'
            
            MDTextField:
                id: channel_search
                hint_text: 'Search conversations...'
                mode: 'fill'
                size_hint_y: None
                height: dp(48)
                on_text: root.filter_channels(self.text)
            
            MDScrollView:
                MDList:
                    id: channel_list
        
        # Main Content
        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: app.theme_cls.backgroundColor
            
            # Top Bar
            MDTopAppBar:
                id: top_bar
                title: 'Select a conversation'
                elevation: 2
                left_action_items: [['menu', lambda x: root.toggle_sidebar()]]
                right_action_items: [
                    ['checkbox-marked-outline', lambda x: root.select_all()],
                    ['checkbox-blank-outline', lambda x: root.deselect_all()],
                    ['delete', lambda x: root.delete_selected(), 'Delete Selected']
                ]
            
            # Filter Bar
            MDCard:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(64)
                padding: dp(12), dp(8)
                spacing: dp(12)
                elevation: 1
                radius: [0, 0, 0, 0]
                
                MDLabel:
                    text: 'Filter:'
                    font_style: 'Subtitle2'
                    theme_text_color: 'Primary'
                    size_hint_x: None
                    width: dp(60)
                    valign: 'middle'
                
                MDTextField:
                    id: message_filter
                    hint_text: 'Search messages...'
                    mode: 'fill'
                    size_hint_x: 0.5
                    on_text: root.apply_filter()
                
                MDCheckbox:
                    id: mine_only
                    active: True
                    on_active: root.apply_filter()
                    size_hint_x: None
                    width: dp(48)
                
                MDLabel:
                    text: 'Only my messages'
                    font_style: 'Body2'
                    theme_text_color: 'Secondary'
                    valign: 'middle'
                    size_hint_x: None
                    width: dp(140)
                
                Widget:
                
                MDRaisedButton:
                    id: load_more_btn
                    text: 'Load More'
                    size_hint_x: None
                    width: dp(120)
                    on_release: root.load_more()
                    disabled: True
                
                MDRaisedButton:
                    id: load_all_btn
                    text: 'Load All'
                    size_hint_x: None
                    width: dp(120)
                    on_release: root.load_all()
                    disabled: True
            
            # Message List
            MDScrollView:
                MDList:
                    id: message_list

            # Status Bar
            MDCard:
                size_hint_y: None
                height: dp(48)
                padding: dp(16), dp(8)
                elevation: 0
                radius: 0
                md_bg_color: app.theme_cls.surfaceColor
                
                MDLabel:
                    id: status_label
                    text: 'Select a conversation to load messages.'
                    font_style: 'Caption'
                    theme_text_color: 'Hint'
                    valign: 'middle'

<LoadingPopup@MDDialog>:
    auto_dismiss: False
    
<ConfirmDialog@MDDialog>:
    buttons: []
'''

# Custom Widgets
class MessageRow(MDBoxLayout):
    message_id = StringProperty('')
    timestamp = StringProperty('')
    content = StringProperty('')
    is_mine = BooleanProperty(False)
    checked = BooleanProperty(False)
    bg_color = ListProperty([0.9, 0.9, 0.9, 1])
    on_delete_callback = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_bg_color()
    
    def update_bg_color(self):
        if self.is_mine:
            self.bg_color = [0.85, 0.9, 1, 1]  # Light blue for own messages
        else:
            self.bg_color = [0.95, 0.95, 0.95, 1]  # Light gray for others
    
    def on_checkbox_active(self, active):
        self.checked = active
        if self.on_delete_callback:
            self.on_delete_callback(self.message_id, active)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
    
    def on_enter(self):
        self.app = App.get_running_app()
        if hasattr(self.ids, 'token_field'):
            Clock.schedule_once(lambda dt: setattr(self.ids.token_field, 'focus', True), 0.1)
    
    def toggle_show(self, active):
        if hasattr(self.ids, 'token_field'):
            self.ids.token_field.password = not active
    
    def do_login(self):
        token = self.ids.token_field.text.strip()
        if not token:
            self.ids.error_label.text = 'Token cannot be empty.'
            return
        
        self.ids.login_button.disabled = True
        self.ids.login_button.text = 'Connecting...'
        self.ids.error_label.text = ''
        
        def run_login():
            try:
                me = self.app.api_get_me(token)
                dms = self.app.api_get_dms(token)
                Clock.schedule_once(lambda dt: self.on_login_success(me, dms), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.on_login_error(str(e)), 0)
        
        threading.Thread(target=run_login, daemon=True).start()
    
    def on_login_success(self, me, dms):
        self.app.token = self.ids.token_field.text.strip()
        self.app.my_id = me['id']
        self.app.channels = dms
        self.app.screen_manager.current = 'main'
        self.app.main_screen.on_enter()
    
    def on_login_error(self, error):
        self.ids.error_label.text = error
        self.ids.login_button.disabled = False
        self.ids.login_button.text = 'Login'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.sidebar_open = True
        self.selected_channel = None
        self.all_messages = []
        self.displayed_messages = {}
        self.checked_messages = set()
        self.deleting = False
        self.loading_all = False
    
    def on_enter(self):
        self.app = App.get_running_app()
        self.render_channel_list()
    
    def toggle_sidebar(self):
        sidebar = self.ids.sidebar
        if self.sidebar_open:
            sidebar.width = 0
            sidebar.opacity = 0
        else:
            sidebar.width = dp(280)
            sidebar.opacity = 1
        self.sidebar_open = not self.sidebar_open
    
    def render_channel_list(self, channels=None):
        if channels is None:
            channels = self.app.channels
        
        channel_list = self.ids.channel_list
        channel_list.clear_widgets()
        
        for ch in channels:
            name = self.get_channel_name(ch)
            btn = Button(
                text=name,
                size_hint_y=None,
                height=dp(48),
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
                font_size=sp(14),
                halign='left',
                valign='middle',
                padding=(dp(12), dp(8)),
                text_size=(dp(250), None)
            )
            btn.bind(on_release=partial(self.select_channel, ch))
            
            # Add canvas for background
            with btn.canvas.before:
                Color(0.2, 0.2, 0.2, 1)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(8),])
            btn.bind(pos=self.update_btn_rect, size=self.update_btn_rect)
            
            channel_list.add_widget(btn)
    
    def update_btn_rect(self, instance, value):
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
    
    def get_channel_name(self, ch):
        if ch.get('type') == 3:
            return ch.get('name') or 'Group DM'
        recipients = ch.get('recipients', [])
        if recipients:
            u = recipients[0]
            return u.get('global_name') or u.get('username') or 'Unknown'
        return f"Channel {ch['id']}"
    
    def filter_channels(self, query):
        query = query.lower()
        filtered = [c for c in self.app.channels if query in self.get_channel_name(c).lower()]
        self.render_channel_list(filtered)
    
    def select_channel(self, ch, *args):
        self.selected_channel = ch
        self.all_messages = []
        self.checked_messages = set()
        self.ids.top_bar.title = self.get_channel_name(ch)
        self.ids.load_more_btn.disabled = True
        self.ids.load_all_btn.disabled = True
        self.update_status('Loading messages...')
        self.clear_message_list()
        threading.Thread(target=self._fetch_msgs, args=(ch['id'], None), daemon=True).start()
    
    def _fetch_msgs(self, cid, before):
        try:
            msgs = self.app.api_get_messages(self.app.token, cid, before)
            Clock.schedule_once(lambda dt: self._on_msgs(msgs, before is not None), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error: {e}'), 0)
    
    def _on_msgs(self, msgs, appended):
        if not appended:
            self.all_messages = msgs
        else:
            self.all_messages.extend(msgs)
        
        has_more = len(msgs) == 100
        self.ids.load_more_btn.disabled = not has_more
        self.ids.load_all_btn.disabled = not has_more
        self.apply_filter()
    
    def load_more(self):
        if not self.all_messages or not self.selected_channel:
            return
        oldest = self.all_messages[-1]['id']
        self.update_status('Loading older messages...')
        self.ids.load_more_btn.disabled = True
        threading.Thread(target=self._fetch_msgs, args=(self.selected_channel['id'], oldest), daemon=True).start()
    
    def load_all(self):
        if not self.selected_channel:
            return
        self.loading_all = True
        self.ids.load_more_btn.disabled = True
        self.ids.load_all_btn.disabled = True
        self.ids.load_all_btn.text = 'Loading...'
        self.update_status('Loading all messages — please wait...')
        
        cid = self.selected_channel['id']
        
        def run():
            try:
                while True:
                    before = self.all_messages[-1]['id'] if self.all_messages else None
                    msgs = self.app.api_get_messages(self.app.token, cid, before)
                    if not msgs:
                        break
                    self.all_messages.extend(msgs)
                    total = len(self.all_messages)
                    Clock.schedule_once(lambda dt, t=total: self.update_status(f'Loaded {t} messages so far...'), 0)
                    if len(msgs) < 100:
                        break
                    time.sleep(0.3)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f'Error: {e}'), 0)
            finally:
                Clock.schedule_once(lambda dt: self._on_load_all_done(), 0)
        
        threading.Thread(target=run, daemon=True).start()
    
    def _on_load_all_done(self):
        self.loading_all = False
        self.ids.load_all_btn.disabled = True
        self.ids.load_all_btn.text = 'Load All'
        self.ids.load_more_btn.disabled = True
        self.apply_filter()
        self.update_status(f'All messages loaded — {len(self.all_messages)} total')
    
    def apply_filter(self, *args):
        query = self.ids.message_filter.text.lower() if hasattr(self.ids, 'message_filter') else ''
        only_mine = self.ids.mine_only.active if hasattr(self.ids, 'mine_only') else True
        
        filtered = []
        for m in self.all_messages:
            if only_mine and m['author']['id'] != self.app.my_id:
                continue
            if query and query not in m.get('content', '').lower():
                continue
            filtered.append(m)
        
        self.render_messages(filtered)
    
    def clear_message_list(self):
        self.ids.message_list.clear_widgets()
        self.displayed_messages = {}

    def render_messages(self, msgs):
        self.clear_message_list()
        for m in msgs:
            mid = m['id']
            ts = m.get('timestamp', '')[:16].replace('T', ' ')
            content = m.get('content', '') or '[attachment/embed]'
            is_mine = m['author']['id'] == self.app.my_id
            
            row = MessageRow(
                message_id=mid,
                timestamp=ts,
                content=content[:180],
                is_mine=is_mine,
                checked=mid in self.checked_messages,
                on_delete_callback=self.toggle_check
            )
            
            self.ids.message_list.add_widget(row)
            self.displayed_messages[mid] = row
        
        total = len(self.all_messages)
        shown = len(msgs)
        selected = len(self.checked_messages)
        self.update_status(f'{shown} shown | {total} loaded | {selected} selected')
    
    def toggle_check(self, mid, checked):
        if checked:
            self.checked_messages.add(mid)
        else:
            self.checked_messages.discard(mid)
        self.update_status_count()
    
    def select_all(self):
        for mid, row in self.displayed_messages.items():
            if row.is_mine:
                row.checked = True
                row.ids.checkbox.active = True
                self.checked_messages.add(mid)
        self.update_status_count()
    
    def deselect_all(self):
        for mid, row in self.displayed_messages.items():
            row.checked = False
            row.ids.checkbox.active = False
        self.checked_messages.clear()
        self.update_status_count()
    
    def update_status_count(self):
        total = len(self.all_messages)
        shown = len(self.displayed_messages)
        selected = len(self.checked_messages)
        self.update_status(f'{shown} shown | {total} loaded | {selected} selected')
    
    def update_status(self, text):
        if hasattr(self.ids, 'status_label'):
            self.ids.status_label.text = text
    
    def delete_selected(self):
        if not self.checked_messages:
            self.show_dialog('Nothing selected', 'Check some messages first.')
            return
        if self.deleting:
            return
        
        count = len(self.checked_messages)
        self.show_confirm_dialog(
            'Confirm Delete',
            f'Permanently delete {count} message(s)?\n\n1.5s delay between deletions. Cannot be undone.',
            lambda: self._do_delete()
        )
    
    def _do_delete(self):
        to_delete = list(self.checked_messages)
        cid = self.selected_channel['id']
        self.deleting = True
        self.ids.load_all_btn.disabled = True
        self.ids.load_more_btn.disabled = True
        
        def run():
            done = 0
            failed = 0
            for mid in to_delete:
                ok = self.app.api_delete_message(self.app.token, cid, mid)
                if ok:
                    done += 1
                    Clock.schedule_once(lambda dt, m=mid, d=done, t=len(to_delete): self.on_deleted(m, d, t), 0)
                else:
                    failed += 1
                time.sleep(DELAY)
            Clock.schedule_once(lambda dt: self.on_done(done, failed), 0)
        
        threading.Thread(target=run, daemon=True).start()
    
    def on_deleted(self, mid, done, total):
        self.checked_messages.discard(mid)
        if mid in self.displayed_messages:
            row = self.displayed_messages[mid]
            self.ids.message_list.remove_widget(row)
            del self.displayed_messages[mid]
        self.update_status(f'Deleting... {done}/{total}')
    
    def on_done(self, done, failed):
        self.deleting = False
        self.ids.load_all_btn.disabled = False
        self.ids.load_more_btn.disabled = False
        msg = f'Done. {done} message(s) deleted.'
        if failed:
            msg += f' {failed} failed.'
        self.update_status(msg)
        self.show_dialog('Complete', msg)
    
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text='OK', on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
    
    def show_confirm_dialog(self, title, text, callback):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text='Cancel', on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text='Delete', md_bg_color=(1, 0.2, 0.2, 1), 
                              on_release=lambda x: (dialog.dismiss(), callback()))
            ]
        )
        dialog.open()


class DMDeleterApp(MDApp):
    token = StringProperty('')
    my_id = StringProperty('')
    channels = ListProperty([])
    screen_manager = ObjectProperty(None)
    main_screen = ObjectProperty(None)
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Teal"
        
        # Load KV
        Builder.load_string(KV)
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Login screen
        login_screen = LoginScreen()
        self.screen_manager.add_widget(login_screen)
        
        # Main screen
        self.main_screen = MainScreen()
        self.screen_manager.add_widget(self.main_screen)
        
        return self.screen_manager
    
    # API Methods
    def _headers(self, token):
        return {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
        }
    
    def api_get_me(self, token):
        r = requests.get(f'{API}/users/@me', headers=self._headers(token))
        if r.status_code == 401:
            raise ValueError('Invalid token.')
        r.raise_for_status()
        return r.json()
    
    def api_get_dms(self, token):
        r = requests.get(f'{API}/users/@me/channels', headers=self._headers(token))
        r.raise_for_status()
        return [c for c in r.json() if c.get('type') in (1, 3)]
    
    def api_get_messages(self, token, channel_id, before=None):
        params = {'limit': 100}
        if before:
            params['before'] = before
        r = requests.get(f'{API}/channels/{channel_id}/messages', 
                        headers=self._headers(token), params=params)
        if r.status_code in (403, 404):
            return []
        r.raise_for_status()
        return r.json()
    
    def api_delete_message(self, token, channel_id, msg_id):
        r = requests.delete(f'{API}/channels/{channel_id}/messages/{msg_id}',
                           headers=self._headers(token))
        return r.status_code in (200, 204)


if __name__ == '__main__':
    DMDeleterApp().run()
