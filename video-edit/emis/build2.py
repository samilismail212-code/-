import json, os, subprocess, sys, glob
B=os.path.dirname(os.path.abspath(__file__)); P=B+'/png/'
SRC=glob.glob('/root/.claude/uploads/a651efc4-c81a-5144-a95d-2bb16dc72f43/21650f4d*')[0]
OUTF=sys.argv[1] if len(sys.argv)>1 else B+'/out.mp4'
sys.path.insert(0,B)
import assets

# ---- pass 1: cut pauses (times in source seconds) ----
END=158.5
pauses=[(14.94,15.36),(51.29,52.27),(63.34,63.77),(69.25,69.67),(79.59,80.20),(112.41,112.82),(123.17,123.65),(142.90,143.20),(156.40,156.94)]
keep=[];cur=0.0
for s,e in pauses:
    cs,ce=s+0.10,e-0.10
    if ce-cs<0.1: continue
    keep.append((cur,cs)); cur=ce
keep.append((cur,END))
D=sum(b-a for a,b in keep)
def tmap(t):                      # source time -> tight timeline
    acc=0.0
    for a,b in keep:
        if t<=a: return acc
        if t<=b: return acc+t-a
        acc+=b-a
    return acc
ac="volume=0.7,highpass=f=90,lowpass=f=14000,afftdn=nr=14:nf=-30,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3"
n=len(keep)
F=[f"[0:v]fps=30,split={n}"+''.join(f"[v{i}]" for i in range(n))]
F.append(f"[0:a]aresample=48000,{ac},asplit={n}"+''.join(f"[a{i}]" for i in range(n)))
for i,(a,b) in enumerate(keep):
    F.append(f"[v{i}]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[tv{i}]")
    F.append(f"[a{i}]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.02,afade=t=out:st={b-a-0.02:.3f}:d=0.02[ta{i}]")
F.append(''.join(f"[tv{i}][ta{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[tv][ta]")
if not os.path.exists(B+'/tight.mkv') or '--redo' in sys.argv:
    subprocess.run(['ffmpeg','-y','-v','error','-i',SRC,'-filter_complex',';'.join(F),'-map','[tv]','-map','[ta]','-c:v','libx264','-crf','10','-preset','veryfast','-c:a','pcm_s16le',B+'/tight.mkv'],check=True)

# ---- captions (source-time) ----
caps=json.load(open(B+'/captions2.json'))
for i,c in enumerate(caps): assets.caption(i,c['text'],prefix='ec',sz=62,lh=104)
XF=0.5; OUTRO=3.4
T3=D-XF; TOT=T3+OUTRO
subprocess.run(['python3',B+'/music.py',str(TOT+2),str(T3-0.2)],check=True,cwd=B)

# ---- pass 2: compose ----
inp=['-i',B+'/tight.mkv','-i',B+'/music.wav']
def img(p,t=None): inp.extend(['-loop','1','-framerate','30']+(['-t',str(t)] if t else [])+['-i',p])
img(P+'wm.png'); img(P+'lower.png')
for i in range(len(caps)): img(P+f'ec{i}.png')
img(P+'r4.png',OUTRO)
base=2+2+len(caps)
zs=lambda w,h,z0,z1,d:f"scale=w='2*trunc({w}*({z0}+({z1}-{z0})*t/{d:.3f})/2)':h='2*trunc({h}*({z0}+({z1}-{z0})*t/{d:.3f})/2)':eval=frame:flags=bicubic"
# (src start, src end, zoom0, zoom1, y offset)
pieces=[(0,22,1.0,1.06,0),(22,36,1.28,1.32,-110),(36,50,1.0,1.05,0),(50,67,1.25,1.28,-40),(67,84,1.0,1.06,0),
        (84,97,1.28,1.32,40),(97,110,1.0,1.05,0),(110,128,1.25,1.28,80),(128,148,1.0,1.06,0),(148,END,1.28,1.32,110)]
eq='eq=contrast=1.07:saturation=1.12:brightness=0.02:gamma=0.97'
FW,FH=756,1344
G=[]
G.append("[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:6,eq=brightness=-0.18:saturation=0.8,drawbox=x=156:y=124:w=768:h=1356:color=0xD4AA50:t=fill,setsar=1[bg]")
G.append(f"[0:v]fps=30,scale={FW}:{FH}:flags=lanczos,hqdn3d=1.2:1.2:4:4,unsharp=5:5:0.8:5:5:0.0,{eq},split={len(pieces)}"+''.join(f"[s{i}]" for i in range(len(pieces))))
for i,(a,b,z0,z1,oy) in enumerate(pieces):
    ta,tb=tmap(a),tmap(b); d=tb-ta
    G.append(f"[s{i}]trim={ta:.3f}:{tb:.3f},setpts=PTS-STARTPTS,{zs(FW,FH,z0,z1,d)},crop={FW}:{FH}:(iw-{FW})/2:(ih-{FH})/2+({oy}),setsar=1[p{i}]")
G.append(''.join(f"[p{i}]" for i in range(len(pieces)))+f"concat=n={len(pieces)}:v=1:a=0,settb=1/30,fps=30[fg]")
G.append(f"[bg][fg]overlay=x=162:y=130:shortest=1,format=yuv420p,settb=1/30,fps=30,tpad=stop_mode=clone:stop_duration=1[vm]")
G.append(f"[{base}:v]fps=30,format=yuv420p,{zs(1080,1920,1.0,1.05,OUTRO)},crop=1080:1920,setsar=1,fade=t=out:st={OUTRO-0.3}:d=0.3,settb=1/30[vr]")
G.append(f"[vm][vr]xfade=transition=fade:duration={XF}:offset={T3:.3f}[x]")
cur='x'
def ov(idx,S,E,xe,ye,n,pre=''):
    global cur
    G.append(f"[{idx}:v]{pre}format=rgba,fade=t=in:st={S:.3f}:d=0.3:alpha=1,fade=t=out:st={E-0.3:.3f}:d=0.3:alpha=1[o{n}]")
    G.append(f"[{cur}][o{n}]overlay=x='{xe}':y='{ye}':eof_action=pass:shortest=0[m{n}]"); cur=f'm{n}'
ov(2,0.3,T3-0.1,'W-w-14','8',0,'scale=150:-1,')
ov(3,0.3,T3-0.1,'20','24',1,'scale=520:-1,')
for i,c in enumerate(caps):
    a=tmap(c['t0']); b=min(tmap(c['t1']),T3-0.2)
    ov(4+i,a,b,'(W-w)/2',f"1505+30*pow(max(0,1-(t-{a:.3f})/0.25),2)",2+i)
G.append(f"[{cur}]format=yuv420p[vout]")
G.append(f"[0:a]loudnorm=I=-16:TP=-2:LRA=9,apad=whole_dur={TOT:.3f}[voice]")
G.append(f"[1:a]atrim=0:{TOT:.3f},volume='if(lt(t,{T3-0.3:.2f}),0.13,0.13+0.30*min(1,(t-{T3-0.3:.2f})/0.8))':eval=frame[mus]")
G.append(f"[voice][mus]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOT-1.2:.2f}:d=1.2[aout]")
cmd=['ffmpeg','-y','-v','error','-stats']+inp+['-filter_complex',';\n'.join(G),'-map','[vout]','-map','[aout]','-t',f'{TOT:.3f}','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',OUTF]
print('tight',D,'total',TOT)
subprocess.run(cmd,check=True)
