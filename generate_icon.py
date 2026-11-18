#!/usr/bin/env python3
"""Generate app icon for Discord DM Deleter"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 512x512 icon
size = 512
img = Image.new('RGBA', (size, size), (0x3b, 0x4e, 0x9b, 0xFF))  # Discord-like indigo
draw = ImageDraw.Draw(img)

# Draw a trash/bin icon
margin = size // 8
bin_width = size - 2 * margin
bin_height = int(bin_width * 1.3)
bin_left = (size - bin_width) // 2
bin_top = (size - bin_height) // 2 + size // 16

# Bin body
draw.rounded_rectangle(
    [bin_left + bin_width//4, bin_top + bin_height//5, 
     bin_left + 3*bin_width//4, bin_top + 4*bin_height//5],
    radius=size//20,
    fill=(0x2b, 0x2d, 0x31, 0xFF)  # Dark gray
)

# Bin lid
draw.rounded_rectangle(
    [bin_left + bin_width//4, bin_top, 
     bin_left + 3*bin_width//4, bin_top + bin_height//6],
    radius=size//20,
    fill=(0x2b, 0x2d, 0x31, 0xFF)
)

# Lid handle
draw.rounded_rectangle(
    [bin_left + bin_width//2 - bin_width//10, bin_top - bin_height//20,
     bin_left + bin_width//2 + bin_width//10, bin_top + bin_height//40],
    radius=size//40,
    fill=(0x3b, 0x4e, 0x9b, 0xFF)
)

# Vertical lines on bin
for i in range(1, 3):
    x = bin_left + bin_width//4 + i * bin_width//6
    draw.line(
        [x, bin_top + bin_height//5, x, bin_top + 4*bin_height//5],
        fill=(0x3b, 0x4e, 0x9b, 0xFF),
        width=size//30
    )

# Save multiple sizes
output_dir = '/Users/urvisha/Documents/4911/dmdeleter/data'
os.makedirs(output_dir, exist_ok=True)

for icon_size in [48, 72, 96, 144, 192, 512]:
    resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    resized.save(f'{output_dir}/icon-{icon_size}.png')

# Save as icon.png (512x512 for buildozer)
img.save(f'{output_dir}/icon.png')
print("✅ Icons generated in data/")