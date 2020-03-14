from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont
import time,psutil,uptime
def ioPic(rs,ws):
    # 10 30 50 70
    rs=round(rs/1024/1024,1) # cpnvert to MB/s
    ws=round(ws/1024/1024,1) # convert to MB/s

    draw.text((15,100),"R","black",io_font)
    draw.text((40,100),"W","black",io_font)
    
    draw.rectangle([10,103,25,10],(100,100,100))
    draw.rectangle([35,103,50,10],(100,100,100))
    draw.rectangle([10,103,25,int(103-rs)],orange_color)
    draw.rectangle([35,103,50,int(103-ws)],orange_color)

    draw.text((10,int(103-rs-20)),str(rs),"black")
    draw.text((35,int(103-ws-20)),str(ws),"black")


serial = spi(port=0, device=0)
device = st7735(serial, width=128, height=128, rotate=3, h_offset=1, v_offset=2, bgr=True)

buffer = Image.new(device.mode, device.size)
draw = ImageDraw.Draw(buffer)

font=ImageFont.truetype("font.ttf" ,32)
standard_font=ImageFont.truetype("astro.ttf",10)
io_font=ImageFont.truetype("font.ttf" ,20)

black_color=(68,68,68)
orange_color=(249,12,23)
while True:
    current_time=time.time()
    uptime_days=int(uptime.uptime()/(24*60*60))
    uptime_hours=int((uptime.uptime()%(24*60*60))/3600)
    while (time.time()-current_time)<=30.0:
        cpu_info=psutil.cpu_percent()
        draw.rectangle(device.bounding_box, outline=None, fill=(255, 255, 255))
        draw.arc([21,21,107,107],0,360,black_color,2)
        draw.arc([11,11,117,117],0,360,black_color,2)
        draw.arc([12,12,116,116],-90,(cpu_info/100)*360-90,(249,122,23),8)
        draw.text((40, 35), str(cpu_info)+"%", (0,0,0),font)
        draw.text((40,65),"Load",(0,0,0),standard_font)
        draw.text((40,80),"ut:","black",standard_font)
        draw.text((70,80),""+str(uptime_days)+"d"+str(uptime_hours)+"h",black_color)
        device.display(buffer)
        time.sleep(0.5)
    #视图1：CPU负载
    current_time=time.time()
    rs=0
    ws=0
    while (time.time()-current_time)<=10.0:
        current_time_inner=time.time()
        read_bytes = psutil.disk_io_counters(perdisk=True)['mmcblk0p2'][2]
        write_bytes = psutil.disk_io_counters(perdisk=True)['mmcblk0p2'][3]


         #绘制出图形
        time.sleep(0.1)
        print("not dead")
        rs=(psutil.disk_io_counters(perdisk=True)['mmcblk0p2'][2]-read_bytes)/(time.time()-current_time_inner) # read speed bytes
        ws=(psutil.disk_io_counters(perdisk=True)['mmcblk0p2'][3]-write_bytes)/(time.time()-current_time_inner) # write speed bytes
        draw.rectangle(device.bounding_box, outline=None, fill=(255, 255, 255))
        ioPic(rs, ws)
        device.display(buffer)


    #视图2：DiskI/O与网络

