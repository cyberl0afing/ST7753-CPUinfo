# -*- coding: UTF-8 -*-

from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont

serial = spi(port=0, device=0)
device = st7735(serial, width=128, height=128, rotate=2, h_offset=1, v_offset=2, bgr=True)

buffer = Image.new(device.mode, device.size)
draw = ImageDraw.Draw(buffer)

while True:
    draw.rectangle(device.bounding_box, outline=None, fill=(152, 152, 3))
    draw.text((30, 50), "hello world!", "white")
    device.display(buffer)
