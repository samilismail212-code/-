import json, os, subprocess, sys, glob
B=os.path.dirname(os.path.abspath(__file__)); P=B+'/png/'
U='/root/.claude/uploads/a651efc4-c81a-5144-a95d-2bb16dc72f43/'
V1=glob.glob(U+'f0dd3b61*')[0]; V2=glob.glob(U+'2639665d*')[0]
OUTF=sys.argv[1] if len(sys.argv)>1 else B+'/out.mp4'
sys.path.insert(0,B)
import assets

L1=5.93; XF=0.4
END=116.2
keep=[(0,24.30),(24.60,END)]            # v2 source seconds
D2=sum(b-a for a,b in keep)
def tmap(t):
    acc=0.0
    for a,b in keep:
        if t<=a: return acc
        if t<=b: return acc+t-a
        acc+=b-a
    return acc
T2=L1-XF
def ft(t): return T2+tmap(t)           # v2 source time -> final timeline
OUTRO=3.4
T3=T2+D2-XF; TOT=T3+OUTRO
caps=json.load(open(B+'/captions5.json'))
for i,c in enumerate(caps):
    c['a']=c['t0'] if c.get('abs') else ft(c['t0'])
    c['b']=c['t1'] if c.get('abs') else ft(c['t1'])
    assets.caption(i,c['text'],prefix='gc',sz=62,lh=104)
subprocess.run(['python3',B+'/music.py',str(TOT+2),str(T2-0.4)],check=True,cwd=B)

inp=['-i',V1,'-i',V2,'-i',B+'/music.wav']
def img(p,t=None): inp.extend(['-loop','1','-framerate','30']+(['-t',str(t)] if t else [])+['-i',p])
img(P+'wm.png'); img(P+'lower.png')
for i in range(len(caps)): img(P+f'gc{i}.png')
img(P+'r4.png',OUTRO)
base=3+2+len(caps)
zs=lambda w,h,z0,z1,d:f"scale=w='2*trunc({w}*({z0}+({z1}-{z0})*t/{d:.3f})/2)':h='2*trunc({h}*({z0}+({z1}-{z0})*t/{d:.3f})/2)':eval=frame:flags=bicubic"
eq='eq=contrast=1.07:saturation=1.14:brightness=0.025:gamma=0.97'
ac="volume=0.7,highpass=f=90,lowpass=f=14000,afftdn=nr=14:nf=-30,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3"
G=[]
G.append(f"[0:v]fps=30,scale=1080:1920:flags=lanczos,{eq},unsharp=5:5:0.4,setpts=PTS-STARTPTS,{zs(1080,1920,1.0,1.08,L1)},crop=1080:1920,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.5[va]")
# main video: cut pause, then zoom pieces (source-time ranges)
pieces=[(0,12,1.0,1.06,0),(12,24.3,1.2,1.25,-90),(24.6,40,1.0,1.05,0),(40,55,1.22,1.27,-90),(55,70,1.0,1.05,0),
        (70,78,1.2,1.25,-90),(78,90,1.0,1.06,0),(90,103,1.22,1.27,-90),(103,END,1.0,1.05,0)]
G.append(f"[1:v]fps=30,scale=1080:1920:flags=lanczos,hqdn3d=1.0:1.0:3:3,unsharp=5:5:0.6:5:5:0.0,{eq},split={len(pieces)}"+''.join(f"[s{i}]" for i in range(len(pieces))))
for i,(a,b,z0,z1,oy) in enumerate(pieces):
    d=b-a
    G.append(f"[s{i}]trim={a}:{b},setpts=PTS-STARTPTS,{zs(1080,1920,z0,z1,d)},crop=1080:1920:(iw-1080)/2:(ih-1920)/2+({oy}),setsar=1[p{i}]")
G.append(''.join(f"[p{i}]" for i in range(len(pieces)))+f"concat=n={len(pieces)}:v=1:a=0,settb=1/30,fps=30,format=yuv420p[vb]")
G.append(f"[{base}:v]fps=30,format=yuv420p,{zs(1080,1920,1.0,1.05,OUTRO)},crop=1080:1920,setsar=1,fade=t=out:st={OUTRO-0.3}:d=0.3,settb=1/30[vr]")
G.append(f"[va][vb]xfade=transition=smoothleft:duration={XF}:offset={T2:.3f}[x1]")
G.append(f"[x1][vr]xfade=transition=fade:duration=0.5:offset={T3:.3f}[x2]")
cur='x2'
def ov(idx,S,E,xe,ye,n,pre=''):
    global cur
    G.append(f"[{idx}:v]{pre}format=rgba,fade=t=in:st={S:.3f}:d=0.3:alpha=1,fade=t=out:st={E-0.3:.3f}:d=0.3:alpha=1[o{n}]")
    G.append(f"[{cur}][o{n}]overlay=x='{xe}':y='{ye}':eof_action=pass:shortest=0[m{n}]"); cur=f'm{n}'
ov(3,0.3,T3-0.1,'W-w-20','60',0)
ov(4,0.3,T3-0.1,'20','40',1,'scale=520:-1,')
for i,c in enumerate(caps):
    a=c['a']; b=min(c['b'],T3-0.2)
    ov(5+i,a,b,'(W-w)/2',f"1330+40*pow(max(0,1-(t-{a:.3f})/0.25),2)",2+i)
G.append(f"[{cur}]format=yuv420p[vout]")
G.append(f"[0:a]aresample=48000,{ac}[a1]")
G.append(f"[1:a]aresample=48000,{ac},asplit={len(keep)}"+''.join(f"[b{i}]" for i in range(len(keep))))
for i,(a,b) in enumerate(keep):
    G.append(f"[b{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.02,afade=t=out:st={b-a-0.02:.3f}:d=0.02[c{i}]")
G.append(''.join(f"[c{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1[a2]")
G.append(f"[a1][a2]acrossfade=d={XF}:c1=tri:c2=tri[av]")
G.append(f"[av]loudnorm=I=-16:TP=-2:LRA=9,apad=whole_dur={TOT:.3f}[voice]")
G.append(f"[2:a]atrim=0:{TOT:.3f},volume='if(lt(t,{T3-0.3:.2f}),0.14,0.14+0.30*min(1,(t-{T3-0.3:.2f})/0.8))':eval=frame[mus]")
G.append(f"[voice][mus]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOT-1.2:.2f}:d=1.2[aout]")
cmd=['ffmpeg','-y','-v','error','-stats']+inp+['-filter_complex',';\n'.join(G),'-map','[vout]','-map','[aout]','-t',f'{TOT:.3f}','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',OUTF]
print('T2',T2,'T3',T3,'total',TOT)
subprocess.run(cmd,check=True)
