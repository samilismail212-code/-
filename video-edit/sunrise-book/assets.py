import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
B=os.path.dirname(os.path.abspath(__file__)); S=os.path.dirname(B)
FD=S+'/fonts/'; OUT=B+'/png/'; os.makedirs(OUT,exist_ok=True)
LOGO=S+'/../images/2.webp'
NAVY=(12,62,92); BLUE=(16,88,128); GOLD=(212,170,80); CREAM=(247,242,230); WHITE=(255,255,255)
def F(sz,w=900): return ImageFont.truetype(FD+f'Cairo{w}.ttf',sz)
def isar(t): return any('\u0600'<=c<='\u06ff' for c in t)
def tw(d,t,f): return d.textlength(t,font=f,direction='rtl' if isar(t) else 'ltr',language='ar' if isar(t) else 'en')
def wrap(d,t,f,maxw):
    lines=[];cur=''
    for w in t.split():
        c=(cur+' '+w).strip()
        if tw(d,c,f)<=maxw or not cur: cur=c
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def rt(d,xr,y,t,f,fill,**k): d.text((xr,y),t,font=f,fill=fill,anchor='ra',direction='rtl',language='ar',**k)

def logo_circle(size):
    im=Image.open(LOGO).convert('RGB'); n=im.width
    r=int(n*0.44); c=n//2
    im=im.crop((c-r,c-r,c+r,c+r)).resize((size*2,size*2),Image.LANCZOS)
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse((0,0,im.width-1,im.height-1),fill=255)
    im.putalpha(m); return im.resize((size,size),Image.LANCZOS)

def watermark():
    s=210; l=logo_circle(s); im=Image.new('RGBA',(s+30,s+30),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).ellipse((10,16,s+14,s+20),fill=(0,0,0,90))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(6))); im.alpha_composite(l,(10,8)); im.save(OUT+'wm.png')

def pill(w,h,fill,r=None):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(im).rounded_rectangle((0,0,w-1,h-1),r or h//2,fill=fill); return im

def hook(title,sub):
    W,H=1080,420; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=F(104); fs=F(58,700)
    lines=wrap(d,title,f,980); y=10
    for ln in lines:
        w=tw(d,ln,f); d.rounded_rectangle((W-40-w-30,y,W-40+30,y+150),28,fill=GOLD+(255,))
        rt(d,W-40,y-2,ln,f,NAVY); y+=165
    w=tw(d,sub,fs); d.rounded_rectangle((W-40-w-30,y+4,W-40+30,y+124),60,fill=NAVY+(235,))
    rt(d,W-40,y+10,sub,fs,WHITE); im.crop((0,0,W,y+140)).save(OUT+'hook.png')

def lower():
    W,H=900,190; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,10,W-1,H-10),40,fill=NAVY+(238,),outline=GOLD+(255,),width=4)
    l=logo_circle(130); im.alpha_composite(l,(W-150,30))
    rt(d,W-170,6,'مكتب القيثارة',F(70),WHITE)
    rt(d,W-170,108,'قرطاسية • خدمات تقنية',F(40,700),GOLD)
    im.save(OUT+'lower.png')

def caption(i,text,prefix='cap',sz=70,lh=118):
    # {{..}} = highlighted (price). RTL: first run on the right.
    segs=[];hl=False
    for p in text.split('{{') :
        pass
    import re
    parts=re.split(r'(\{\{.*?\}\})',text); runs=[(p[2:-2],True) if p.startswith('{{') else (p,False) for p in parts if p]
    W=1000; d0=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    f=F(sz)
    toks=[]
    for t,h in runs:
        t=t.strip() if h else t
        if h and tw(d0,t,f)<=W-160: toks.append((t,True))
        else: toks.extend((w,h) for w in t.split())
    lines=[];cur=[];cw=0
    for w,h in toks:
        wl=tw(d0,w,f)+tw(d0,' ',f)+(36 if h else 0)
        if cw+wl>W-80 and cur: lines.append(cur);cur=[];cw=0
        cur.append((w,h));cw+=wl
    lines.append(cur)
    H=lh*len(lines)+40
    im=Image.new('RGBA',(W+40,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,W+39,H-1),44,fill=(8,30,48,215))
    for li,ln in enumerate(lines):
        x=W+20-30; base=20+li*lh+int(sz*1.25)
        for w,h in ln:
            wl=tw(d,w,f); sp=tw(d,' ',f)
            if h: x-=18
            if h: d.rounded_rectangle((x-wl-18,base-int(sz*1.3),x+18,base+int(sz*0.4)),30,fill=GOLD+(255,))
            d.text((x,base),w,font=f,fill=NAVY if h else WHITE,anchor='rs',direction='rtl' if isar(w) else 'ltr',language='ar' if isar(w) else 'en')
            x-=wl+sp+(18 if h else 0)
    im.save(OUT+f'{prefix}{i}.png')

def bg():
    im=Image.new('RGB',(1080,1920)); px=im.load()
    top=(8,44,70);bot=(18,102,140)
    for y in range(1920):
        t=y/1919; c=tuple(int(top[k]+(bot[k]-top[k])*t) for k in range(3))
        for x in range(0,1080): px[x,y]=c
    d=ImageDraw.Draw(im); d.ellipse((-420,1300,1500,3220),outline=GOLD,width=5); d.ellipse((-300,1420,1380,3100),outline=(*GOLD,),width=2)
    return im

def card_frame(name,title,items,note=None,icon_nums=True):
    im=bg().convert('RGBA'); d=ImageDraw.Draw(im)
    l=logo_circle(190); im.alpha_composite(l,(445,90))
    rt(d,540+tw(d,title,F(92))/2,330,title,F(92),WHITE)
    d.rectangle((340,485,740,492),fill=GOLD)
    y=640; fi=F(60,700)
    for k,t in enumerate(items):
        lines=wrap(d,t,fi,780); h=len(lines)*84+60
        d.rounded_rectangle((60,y,1020,y+h),44,fill=CREAM+(255,))
        if icon_nums:
            d.ellipse((900,y+h//2-42,984,y+h//2+42),fill=GOLD); rt(d,0,0,'',fi,NAVY)
            n=str(k+1); d.text((942,y+h//2),n,font=F(56),fill=NAVY,anchor='mm')
        for j,ln in enumerate(lines): rt(d,880,y+28+j*84,ln,fi,NAVY)
        y+=h+34
    if note: rt(d,1020,y+10,note,F(46,700),GOLD)
    im.convert('RGB').save(OUT+name)

def big_date(name):
    im=bg().convert('RGBA'); d=ImageDraw.Draw(im)
    im.alpha_composite(logo_circle(190),(445,90))
    d.text((540,420),'آخر موعد للتقديم',font=F(90),fill=WHITE,anchor='mm',direction='rtl',language='ar')
    d.rounded_rectangle((90,560,990,960),60,fill=GOLD+(255,))
    d.text((540,660),'السبت',font=F(120),fill=NAVY,anchor='mm',direction='rtl',language='ar')
    d.text((540,830),'2026/10/24',font=F(170),fill=NAVY,anchor='mm')
    d.text((540,1090),'عبر تطبيق «منصة قدم»',font=F(70,700),fill=WHITE,anchor='mm',direction='rtl',language='ar')
    d.text((540,1190),'حتى 10 خيارات حسب الحدود الدنيا',font=F(52,700),fill=GOLD,anchor='mm',direction='rtl',language='ar')
    im.convert('RGB').save(OUT+name)

def outro(name):
    im=bg().convert('RGBA'); d=ImageDraw.Draw(im)
    im.alpha_composite(logo_circle(560),(260,330))
    d.text((540,1010),'مكتب القيثارة',font=F(150),fill=WHITE,anchor='mm',direction='rtl',language='ar')
    d.text((540,1150),'AL-QITHARA OFFICE',font=F(60,700),fill=GOLD,anchor='mm')
    d.text((540,1260),'قرطاسية • خدمات تقنية',font=F(64,700),fill=WHITE,anchor='mm',direction='rtl',language='ar')
    d.rounded_rectangle((120,1390,960,1530),70,fill=GOLD+(255,))
    d.text((540,1460),'تفضّل بزيارتنا وقدّم معنا',font=F(72),fill=NAVY,anchor='mm',direction='rtl',language='ar')
    im.convert('RGB').save(OUT+name)

if __name__=='__main__':
    watermark(); lower(); outro('r4.png')
