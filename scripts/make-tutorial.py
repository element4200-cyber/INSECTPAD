"""Rebuild the bundled tutorial: pip install Pillow imageio-ffmpeg."""
from pathlib import Path
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
W, H, FPS, DURATION = 960, 600, 12, 26
INK, LIME, GREY = "#111111", "#c9ff53", "#777777"
font_root = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
def font(size, bold=False):
    candidates = [font_root / ("arialbd.ttf" if bold else "arial.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")]
    return next((ImageFont.truetype(str(p), size) for p in candidates if p.exists()), ImageFont.load_default())
F = {n: font(n) for n in (18, 20, 23, 26, 30)}
B = {n: font(n, True) for n in (20, 23, 26, 32, 36)}
LINES = [
 [210,80,285,112,238,160,210,80], [228,92,205,37,191,31], [266,98,297,47,307,41],
 [242,151,229,242,215,342], [234,194,166,205,191,139,209,156], [237,196,300,221,275,155,259,166],
 [227,252,139,277,88,365,49,379], [228,254,310,290,361,363,397,372],
 [219,305,168,349,147,418,122,427], [216,306,275,360,294,418,326,432], [215,342,206,375,220,388,233,348]
]
def box(d, xy, fill="white", width=2): d.rectangle(xy, fill=fill, outline=INK, width=width)
def label(d, xy, text, size=23, bold=False, fill=INK): d.text(xy, text, font=(B if bold else F)[size], fill=fill)
def draw_bug(d, progress=1, scale=.68, ox=578, oy=154):
    cursor = None
    for i, line in enumerate(LINES):
        portion = min(1, max(0, progress*len(LINES)-i))
        pts = [(line[k]*scale+ox, line[k+1]*scale+oy) for k in range(0,len(line),2)]
        if not portion: continue
        segment = portion*(len(pts)-1)
        j = min(len(pts)-2, int(segment))
        frac = segment-j
        end = (pts[j][0]+(pts[j+1][0]-pts[j][0])*frac,pts[j][1]+(pts[j+1][1]-pts[j][1])*frac)
        d.line(pts[:j+1]+[end], fill=INK, width=max(2,int(6*scale)), joint="curve")
        cursor = end
    if progress>.94:
        for x,y in [(227,111),(266,124)]:
            x,y=x*scale+ox,y*scale+oy
            d.ellipse((x-5*scale,y-5*scale,x+5*scale,y+5*scale),fill=INK)
        d.line((180*scale+ox,448*scale+oy,290*scale+ox,448*scale+oy),fill=LIME,width=max(3,int(12*scale)))
    if progress<1 and cursor:
        x,y=cursor
        d.polygon([(x,y),(x+8,y+24),(x+15,y+15),(x+24,y+12)],fill=LIME,outline=INK)

def frame(t):
    image=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(image)
    phase=0 if t<6 else 1 if t<15 else 2 if t<20 else 3
    titles=["01 / PICK A BUG. GIVE IT A NAME.","02 / DRAW YOUR VERY OWN MANTIS.","03 / USE YOUR DRAWING AS THE PFP.","04 / CONNECT. REVIEW. APPROVE."]
    tips=["Choose MANTIS. Name: Leaf Larry. Ticker: LARRY.","Use LINE or PEN. Add a head, six legs and two eyes.","Click USE AS PFP. Your image is now selected.","Add SOL for buy + fees. Approve only in your wallet."]
    box(d,(0,0,959,76),LIME)
    label(d,(27,21),titles[phase],32,True)
    label(d,(27,88),"InsectGenerator.exe  /  example walkthrough",20,True)
    box(d,(25,128,934,502)); d.line((500,128,500,502),fill=INK,width=2)
    label(d,(46,149),"CHARACTER TYPE",20,True)
    box(d,(46,186,174,224),LIME); label(d,(57,191),"MANTIS",23,True)
    box(d,(187,186,273,224)); label(d,(203,191),"ANT",23)
    label(d,(47,246),"Name",23); box(d,(150,240,475,282))
    label(d,(162,247),"Leaf Larry"[:min(10,int(t*5))] if phase==0 else "Leaf Larry",23,True)
    label(d,(47,302),"Ticker",23); box(d,(150,296,475,338))
    label(d,(162,303),"LARRY" if t>2 else "",23,True)
    label(d,(47,358),"Job",23); label(d,(160,358),"professional leaf",23)
    box(d,(46,411,475,477),LIME if phase==3 else INK)
    label(d,(67,430),"CREATE ON PUMP.FUN" if phase==3 else "ONE SMALL BUG. BIG VIBES.",23,True,INK if phase==3 else "white")
    if phase<3:
        if phase==0:
            label(d,(537,145),"PFP PREVIEW",20,True);draw_bug(d)
        elif phase==1:
            label(d,(537,145),"DRAW YOUR OWN  /  PEN",20,True)
            draw_bug(d,min(1,(t-6)/7.4))
        else:
            label(d,(537,145),"IMAGE SELECTION",20,True);draw_bug(d,1,.5,628,170)
            box(d,(550,417,910,478),LIME)
            label(d,(570,434),"YOUR IMAGE  /  SELECTED",23,True)
    else:
        label(d,(531,150),"READY TO HATCH?",26,True)
        for i, text in enumerate(["Leaf Larry  /  $LARRY","PFP: Your custom image","Network: Solana mainnet","Initial buy + rent + fees"]):
            label(d,(531,201+i*46),text,23)
        box(d,(531,412,906,476),LIME);label(d,(552,432),"REVIEW IN YOUR WALLET",23,True)
    label(d,(26,518),tips[phase],26,True)
    d.rectangle((26,567,934,579),fill="#eeeeee")
    d.rectangle((26,567,26+int(908*t/DURATION),579),fill=INK)
    return image

frame(15.8).save(OUT/"tutorial-poster.png",optimize=True)
writer=imageio_ffmpeg.write_frames(str(OUT/"insect-tutorial.mp4"),(W,H),fps=FPS,codec="libx264",quality=7,pix_fmt_in="rgb24",pix_fmt_out="yuv420p",output_params=["-movflags","+faststart"])
writer.send(None)
for n in range(DURATION*FPS): writer.send(frame(n/FPS).tobytes())
writer.close()
print({"seconds":DURATION,"frames":DURATION*FPS,"video_bytes":(OUT/"insect-tutorial.mp4").stat().st_size})
