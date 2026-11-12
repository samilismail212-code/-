#!/usr/bin/env python3
"""Al-Qithara Office ad editor: builds the final ad from assets/video1.mp4 (+ optional video2)."""
import subprocess, math, os, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import arabic_reshaper
from bidi.algorithm import get_display

D = os.path.dirname(os.path.abspath(__file__)); A = f"{D}/assets"; W = f"{D}/work"; os.makedirs(W, exist_ok=True)
OUT = f"{D}/../output/Al-Qithara_Ad_Full.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
FONT = f"{A}/tajawal.ttf"
BLUE=(14,74,122); GOLD=(201,162,74); LGOLD=(242,201,100); CREAM=(245,241,232)
# ---- أسعار الملازم: ضع السعر هنا (مثال: "5,000 د.ع") لتظهر بشارة السعر المميزة ----
PRICES = {"Treasure Island": None, "Sunrise Twelve": None}

_R=arabic_reshaper.ArabicReshaper(configuration={'support_ligatures':False})
def ar(t): return t
def F(s): return ImageFont.truetype(FONT, s, layout_engine=ImageFont.Layout.RAQM)
def canvas(): return Image.new("RGBA", (1080,1920), (0,0,0,0))
def shadowed(img, blur=14, off=8, alpha=120):
    sh = Image.new("RGBA", img.size, (0,0,0,0)); sh.putalpha(img.split()[3].point(lambda v: min(v,alpha)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); base = Image.new("RGBA", img.size,(0,0,0,0)); base.alpha_composite(sh,(0,off)); base.alpha_composite(img); return base
def text_c(d, xy, t, size, fill, stroke=0, sfill=(0,0,0)):
    isar=any("\u0600"<=c<="\u06ff" for c in t)
    d.text(xy, t, font=F(size), fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sfill, direction="rtl" if isar else "ltr", language="ar" if isar else None)

# ---------- overlays ----------
def price_badge(img, price):
    d = ImageDraw.Draw(img); cx, cy = 870, 1180
    d.ellipse((cx-135,cy-135,cx+135,cy+135), fill=LGOLD, outline=(255,255,255), width=8)
    text_c(d,(cx,cy-52),ar("السعر"),52,BLUE); text_c(d,(cx,cy+22),ar(price),68,(150,20,20))
def fit(d,t,size,maxw=840):
    while size>40 and d.textlength(t,font=F(size))>maxw: size-=4
    return size
def lower_third(name, teacher, extra=None, price=None):
    im = canvas(); d = ImageDraw.Draw(im); h = 330 if extra else 280; y0 = 1400
    d.rounded_rectangle((60,y0,1020,y0+h), 36, fill=BLUE+(238,), outline=GOLD, width=5)
    d.rounded_rectangle((60+22,y0+22,60+34,y0+h-22), 6, fill=LGOLD)
    text_c(d,(560,y0+85),name,fit(d,name,104),(255,255,255))
    text_c(d,(560,y0+185),ar(f"الأستاذ: {teacher}"),fit(d,f"الأستاذ: {teacher}",58),LGOLD)
    if extra: text_c(d,(560,y0+265),ar(extra),44,(220,230,240))
    im = shadowed(im)
    if price: price_badge(im, price)
    return im
def hook():
    im = canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((330,330,750,430),50,fill=(200,30,30,245)); text_c(d,(540,380),ar("جديد!"),70,(255,255,255))
    text_c(d,(540,1330),ar("ملازم جديدة"),150,LGOLD,stroke=10,sfill=BLUE)
    text_c(d,(540,1500),ar("وصلت مكتبتنا!"),120,(255,255,255),stroke=10,sfill=BLUE)
    return shadowed(im,10,6,90)
def cta():
    im = canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((90,1380,990,1640),44,fill=BLUE+(240,),outline=LGOLD,width=6)
    text_c(d,(540,1455),ar("متوفرة الآن في"),66,(255,255,255))
    text_c(d,(540,1560),ar("مكتب القيثارة"),104,LGOLD)
    return shadowed(im)
def logo_circle(px):
    L = Image.open(f"{A}/logo.jpg").convert("RGB"); c=720; r=665
    L = L.crop((c-r,c-r,c+r,c+r)).resize((px,px),Image.LANCZOS)
    m = Image.new("L",(px,px),0); ImageDraw.Draw(m).ellipse((0,0,px-1,px-1),fill=255)
    o = Image.new("RGBA",(px,px),(0,0,0,0)); o.paste(L,(0,0),m)
    return o
def watermark():
    im = canvas(); lg = logo_circle(200); im.alpha_composite(shadowed(lg,10,4,110).crop((0,0,200,200)) if False else lg,(840,120)); return shadowed(im,10,5,110)
def endcard():
    im = Image.new("RGBA",(1080,1920),CREAM+(255,)); d = ImageDraw.Draw(im)
    for i in range(0,1920,6):   # soft vignette bands
        a = int(18*abs(i-960)/960); d.rectangle((0,i,1080,i+6),fill=tuple(int(c*(1-a/255)+g*(a/255)) for c,g in zip(CREAM,(180,150,90)))+(255,))
    im.alpha_composite(shadowed(logo_circle(940),24,14,90),(70,250))
    d.rounded_rectangle((190,1330,890,1470),70,fill=BLUE); text_c(d,(540,1400),ar("زورونا الآن"),82,(255,255,255))
    text_c(d,(540,1590),ar("ملازم • قرطاسية • خدمات تقنية"),56,GOLD)
    return im

# ---------- timeline ----------
XF = 0.25
# (name, src(0=video1,1=video2,2=endcard), a, b, z0,z1, rot0,rot1, dx0,dx1, dy0,dy1, transition_in)
SEGS = [
 ("hook",0,10.0,11.6, 1.00,1.28, 0,0,  0,0,   0,0,   None),
 ("ti1", 0, 0.4, 3.2, 1.00,1.20, 0,0,  0,0,   0,0,   "slideleft"),
 ("ti2", 0, 3.4, 6.0, 1.26,1.26,-3,3, -40,40,-20,20, "circleopen"),
 ("sr1", 0, 8.9,12.0, 1.00,1.22, 0,0,  0,0,   0,0,   "wipeleft"),
 ("phy", 1, 8.0,12.6, 1.00,1.12, 0,0, -70,-70, 0,0,   "slideright"),
 ("en1", 1,19.4,23.9, 1.05,1.22, 0,0, -30,-30, 0,0,   "zoomin"),
 ("en2", 1,24.4,28.6, 1.22,1.22,-2.5,2.5,-30,30,-10,10,"wipeleft"),
 ("ar",  1,35.4,40.4, 1.00,1.18, 0,0, -50,-30, 0,0,   "circleopen"),
 ("ch1", 1,46.8,52.2, 1.20,1.05, 0,0, -20,-20, 0,0,   "slideleft"),
 ("ch2", 1,53.0,56.6, 1.22,1.22, 2.5,-2.5,-20,20,-10,10,"fadewhite"),
 ("end", 2, 0,2.4,   1.00,1.06, 0,0,  0,0,   0,0,   "fade"),
]
L = [s[3]-s[2] for s in SEGS]
starts=[0.0]; M=L[0]
for i in range(1,len(SEGS)): starts.append(M-XF); M += L[i]-XF
TOTAL = M; END_START = starts[-1]
print("segment starts", [round(x,2) for x in starts], "total", round(TOTAL,2))
st = dict(zip([s[0] for s in SEGS], starts)); Ld = dict(zip([s[0] for s in SEGS], L))

OVL = []
def add(name, im, t0, t1, slide=70): p=f"{W}/{name}.png"; im.save(p); OVL.append((p,t0,t1,slide))
add("hook", hook(), 0.15, st["ti1"]+0.1, 50)
add("t_ti", lower_third("Treasure Island","Rahwan Azad",price=PRICES.get("Treasure Island")), st["ti1"]+0.3, st["ti2"]+1.9)
add("t_sr", lower_third("Sunrise Twelve","Rahwan Azad","معهد نيروز · Newroz Institute",price=PRICES.get("Sunrise Twelve")), st["sr1"]+0.3, st["sr1"]+3.0)
CARDS = [("phy","المعاصر في الفيزياء","علي الذهبي","السادس العلمي · الجزء الأول"),
         ("en1","الملتقى في اللغة الإنكليزية","محمد العبيدي","Part Two · السادس الإعدادي"),
         ("en2","دورة قطع الخارجية","محمد العبيدي","مع الوزاريات · السادس الإعدادي"),
         ("ar","موسوعة المعموري","هشام المعموري","في قواعد اللغة العربية · الجزء الثاني"),
         ("ch1","شفرة الكيمياء","فاضل الهاشمي","السادس العلمي · الجزء الثاني"),
         ("ch2","الملخص الذهبي في الكيمياء","فاضل الهاشمي","السادس العلمي")]
for k,title,teacher,extra in CARDS:
    add("c_"+k, lower_third(title,teacher,extra,price=PRICES.get(title)), st[k]+0.3, st[k]+min(Ld[k]-0.35,3.6))
add("cta", cta(), st["ch2"]+Ld["ch2"]-1.5, END_START-0.1)   # shown right before the end card
add("wm", watermark(), 1.3, END_START+0.1, 0)
endcard().convert("RGB").save(f"{W}/end.png")

# ---------- music (original, synthesized) ----------
SR=44100
def music(total):
    n=int((total+0.6)*SR); t=np.arange(n)/SR; out=np.zeros((2,n)); bpm=118; beat=60/bpm
    def add_at(sig,t0,pan=0.5,g=1.0):
        i=int(t0*SR); 
        if i>=n: return
        s=sig[:n-i]*g; out[0,i:i+len(s)]+=s*(1-pan); out[1,i:i+len(s)]+=s*pan
    def pluck(f,dur=0.5):
        tt=np.arange(int(dur*SR))/SR; e=np.exp(-tt*7)
        w=sum(np.sin(2*np.pi*f*k*tt)/k**1.3 for k in (1,2,3,4,5)); return w*e*(1-np.exp(-tt*400))
    def kick(): tt=np.arange(int(0.25*SR))/SR; return np.sin(2*np.pi*(55*tt+ 90*(1-np.exp(-tt*30))/30*1.0))*np.exp(-tt*14)
    rng=np.random.default_rng(3)
    def hat(): tt=np.arange(int(0.05*SR))/SR; x=rng.standard_normal(len(tt)); x=np.diff(x,prepend=0); return x*np.exp(-tt*90)*0.5
    def clap(): tt=np.arange(int(0.18*SR))/SR; x=rng.standard_normal(len(tt)); x=np.convolve(x,np.ones(4)/4,'same'); return x*np.exp(-tt*22)*0.7
    def bass(f,dur): tt=np.arange(int(dur*SR))/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt*3.5)*(1-np.exp(-tt*200))
    D=146.83; sc=[0,1,4,5,7,8,10,12]  # D hijaz (D Eb F# G A Bb C D)
    fr=lambda k: D*2*2**(sc[k%8]/12+ (k//8))
    mel=[7,6,4,3,4,5,3,0, 7,6,4,3,1,3,0,0]   # eighth-note motif
    for b in range(int(total/beat)+2):
        T=b*beat
        add_at(kick(),T,0.5,0.9); 
        if b%2==1: add_at(clap(),T,0.5,0.35)
        add_at(hat(),T+beat/2,0.65,0.25)
        add_at(bass(D/2 if (b//4)%2==0 else D/2*2**(5/12),beat*.95),T,0.5,0.55)
    for e in range(int(total/(beat/2))+2):
        k=mel[e%len(mel)]; add_at(pluck(fr(k),0.45),e*beat/2,0.35+0.3*(e%2),0.22)
    # whooshes at transitions
    for s in starts[1:]:
        dur=0.45; tt=np.arange(int(dur*SR))/SR; x=rng.standard_normal(len(tt))
        y=np.zeros_like(x); a=0.0; env=np.sin(np.pi*tt/dur)**2
        for j in range(len(x)): 
            c=0.02+0.5*(tt[j]/dur)**2; a+= c*(x[j]-a); y[j]=a
        add_at(y*env*3.0, s-0.05, 0.5, 0.5)
    fade=np.minimum(1,t/0.6)*np.minimum(1,(total+0.3-t).clip(0)/1.2)
    out*=fade; out/= (np.abs(out).max()+1e-9)/0.9
    import wave
    with wave.open(f"{W}/music.wav","wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.T*32767).astype("<i2").tobytes())
music(TOTAL)

# ---------- ffmpeg graph (video only) ----------
SRCP=[f"{A}/video1.mp4",f"{A}/video2.mp4"]
inputs=["-i",SRCP[0],"-i",SRCP[1],"-loop","1","-t",str(L[-1]+0.5),"-i",f"{W}/end.png"]
for p,t0,t1,_ in OVL: inputs+=["-loop","1","-t",f"{TOTAL:.2f}","-i",p]
fc=[]
for i,(n,k,a,b,z0,z1,r0,r1,dx0,dx1,dy0,dy1,tr) in enumerate(SEGS):
    d=b-a; p=lambda v0,v1: f"({v0}+({v1}-{v0})*t/{d:.3f})"
    src = f"[{k}:v]trim={a}:{b},setpts=PTS-STARTPTS,hqdn3d=3:2:4:3,scale=1080:1920:flags=lanczos,unsharp=5:5:0.9:5:5:0.0" if k<2 else f"[2:v]trim=0:{d},setpts=PTS-STARTPTS,fps=30"
    chain=f"{src},scale=w='trunc(1080*{p(z0,z1)}/2)*2':h='trunc(1920*{p(z0,z1)}/2)*2':eval=frame:flags=bicubic"
    if r0 or r1: chain+=f",rotate=a='({p(r0,r1)})*PI/180':c=black"
    chain+=f",crop=1080:1920:x='(iw-1080)/2+{p(dx0,dx1)}':y='(ih-1920)/2+{p(dy0,dy1)}'"
    if k<2: chain+=",eq=brightness=0.035:contrast=1.10:saturation=1.22:gamma=1.04,vignette=PI/6"
    chain+=f",fps=30,format=yuv420p,setsar=1[v{i}]"; fc.append(chain)
m="v0"; cum=L[0]
for i in range(1,len(SEGS)):
    fc.append(f"[{m}][v{i}]xfade=transition={SEGS[i][12]}:duration={XF}:offset={cum-XF:.3f}[x{i}]"); m=f"x{i}"; cum+=L[i]-XF
for j,(p,t0,t1,sl) in enumerate(OVL):
    idx=3+j; dur=t1-t0
    fc.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={max(dur-0.3,0.1):.2f}:d=0.3:alpha=1,setpts=PTS+{t0:.3f}/TB[o{j}]")
    ex = f"y='{sl}*pow(max(0,1-(t-{t0:.3f})/0.4),2)'" if sl else "y=0"
    fc.append(f"[{m}][o{j}]overlay=x=0:{ex}:enable='between(t,{t0:.3f},{t1:.3f})':eof_action=pass[ov{j}]"); m=f"ov{j}"
fc.append(f"[{m}]format=yuv420p[vout]")
cmd=["ffmpeg","-y","-v","error","-stats",*inputs,"-filter_complex",";".join(fc),"-map","[vout]",
     "-t",f"{TOTAL:.3f}","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-r","30","-an",f"{W}/video_only.mp4"]
rc=subprocess.call(cmd)
if rc: sys.exit(rc)
# ---------- audio (numpy) ----------
import wave
def run(*a): subprocess.check_call(["ffmpeg","-y","-v","error",*a])
AF="highpass=f=90,lowpass=f=11000,afftdn=nr=14:nf=-30,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,alimiter=limit=0.95"
for q in (0,1): run("-i",SRCP[q],"-vn","-af",AF,"-ac","2","-ar","44100",f"{W}/voice{q}.wav")
def rd(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()),"<i2").reshape(-1,2).T.astype(np.float64)/32768
VO=[rd(f"{W}/voice0.wav"),rd(f"{W}/voice1.wav")]; Mu=rd(f"{W}/music.wav")
xf=int(XF*SR); voice=np.zeros((2,0))
for (n,k,a,b,*_) in SEGS:
    seg = VO[k][:,int(a*SR):int(b*SR)] if k<2 else np.zeros((2,int((b-a)*SR)))
    if voice.shape[1]==0: voice=seg.copy(); continue
    ramp=np.linspace(0,1,xf); voice[:,-xf:]=voice[:,-xf:]*(1-ramp)+seg[:,:xf]*ramp
    voice=np.concatenate([voice,seg[:,xf:]],axis=1)
N=int(TOTAL*SR); voice=np.pad(voice,((0,0),(0,max(0,N-voice.shape[1]))))[:,:N]; Mu=np.pad(Mu,((0,0),(0,max(0,N-Mu.shape[1]))))[:,:N]
env=np.abs(voice).mean(0); win=int(0.05*SR); env=np.convolve(env,np.ones(win)/win,"same"); env=np.convolve(env,np.ones(int(0.3*SR))/int(0.3*SR),"same")
duck=1-0.65*np.clip(env/0.04,0,1)
mix=voice+Mu*0.55*duck; mix=np.tanh(mix*0.9)/np.tanh(0.9)
with wave.open(f"{W}/mix.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix.T,-1,1)*32767).astype("<i2").tobytes())
run("-i",f"{W}/mix.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","44100","-c:a","aac","-b:a","192k",f"{W}/audio.m4a")
run("-i",f"{W}/video_only.mp4","-i",f"{W}/audio.m4a","-c","copy","-shortest","-movflags","+faststart",OUT)
print("DONE",OUT)
