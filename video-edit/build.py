import json, os, subprocess, sys
B=os.path.dirname(os.path.abspath(__file__)); P=B+'/png/'
U='/root/.claude/uploads/a651efc4-c81a-5144-a95d-2bb16dc72f43/'
V1=U+'00397a2f-1.mp4'; V2=U+'892bb559-____.mp4'
OUTF=sys.argv[1] if len(sys.argv)>1 else B+'/out.mp4'
L1=6.016; XF=0.4
pieces=[(0,10.65,1.0,1.08,0),(11.02,19.02,1.22,1.28,-30),(19.40,27.40,1.0,1.06,0),(27.40,35.40,1.2,1.26,30),(35.40,45.20,1.0,1.08,0)]
recap=[('r1.png',2.9),('r2.png',2.9),('r3.png',2.6),('r4.png',3.4)]
D2=sum(b-a for a,b,*_ in pieces); T2=L1-XF; R=sum(d for _,d in recap)
T3=T2+D2-XF; TOT=T3+R
caps=json.load(open(B+'/captions.json')) if os.path.exists(B+'/captions.json') else []
inp=['-i',V1,'-i',V2,'-i',B+'/music.wav']
def img(p): inp.extend(['-loop','1','-framerate','30','-i',p])
img(P+'wm.png'); img(P+'hook.png'); img(P+'lower.png')
for i,_ in enumerate(caps): img(P+f'cap{i}.png')
r0=len(inp)//2 if False else None
base=3+3+len(caps)
for f,d in recap: inp.extend(['-loop','1','-framerate','30','-t',str(d),'-i',P+f])
F=[]
eq='eq=contrast=1.07:saturation=1.14:brightness=0.025:gamma=0.97'
zs=lambda z0,z1,D:f"scale=w='2*trunc(1080*({z0}+({z1}-{z0})*t/{D:.3f})/2)':h='2*trunc(1920*({z0}+({z1}-{z0})*t/{D:.3f})/2)':eval=frame:flags=bicubic"
F.append(f"[0:v]fps=30,scale=1080:1920:flags=lanczos,{eq},unsharp=5:5:0.4,setpts=PTS-STARTPTS,{zs(1.0,1.08,L1)},crop=1080:1920,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.5[va]")
F.append(f"[1:v]fps=30,crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,hqdn3d=1.3:1.3:5:5,unsharp=5:5:0.9:5:5:0.0,{eq},split={len(pieces)}"+''.join(f"[s{i}]" for i in range(len(pieces))))
for i,(a,b,z0,z1,xo) in enumerate(pieces):
    D=b-a
    F.append(f"[s{i}]trim={a}:{b},setpts=PTS-STARTPTS,{zs(z0,z1,D)},crop=1080:1920:(iw-1080)/2+({xo}):(ih-1920)/2,setsar=1[p{i}]")
F.append(''.join(f"[p{i}]" for i in range(len(pieces)))+f"concat=n={len(pieces)}:v=1:a=0,settb=1/30,fps=30,format=yuv420p[vb]")
rl=[]
for k,(f,d) in enumerate(recap):
    ix=base+k
    F.append(f"[{ix}:v]fps=30,format=yuv420p,{zs(1.0,1.05,d)},crop=1080:1920,setsar=1,fade=t=in:st=0:d=0.3,fade=t=out:st={d-0.3}:d=0.3[rc{k}]"); rl.append(f"[rc{k}]")
F.append(''.join(rl)+f"concat=n={len(recap)}:v=1:a=0,settb=1/30,fps=30[vr]")
F.append(f"[va][vb]xfade=transition=zoomin:duration={XF}:offset={T2:.3f}[x1]")
F.append(f"[x1][vr]xfade=transition=fade:duration={XF}:offset={T3:.3f}[x2]")
cur='x2'
def ov(idx,S,E,xexpr,yexpr,n):
    global cur
    F.append(f"[{idx}:v]format=rgba,fade=t=in:st={S}:d=0.35:alpha=1,fade=t=out:st={E-0.35}:d=0.35:alpha=1[o{n}]")
    F.append(f"[{cur}][o{n}]overlay=x='{xexpr}':y='{yexpr}':eof_action=pass:shortest=0[m{n}]"); cur=f'm{n}'
ov(3,0.6,T3-0.1,'W-w-20','60',0)
ov(4,0.3,3.9,'0',"250-110*pow(max(0,1-(t-0.3)/0.35),2)",1)
ov(5,7.2,11.4,"60+0*t","330-80*pow(max(0,1-(t-7.2)/0.35),2)",2)
for i,c in enumerate(caps):
    ov(6+i,c['t0'],c['t1'],'(W-w)/2',f"1380+40*pow(max(0,1-(t-{c['t0']})/0.25),2)",3+i)
F.append(f"[{cur}]format=yuv420p[vout]")
# audio
ac="volume=0.7,highpass=f=90,lowpass=f=14000,afftdn=nr=14:nf=-30,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3"
F.append(f"[0:a]aresample=48000,{ac}[a1]")
F.append(f"[1:a]aresample=48000,{ac},asplit={len(pieces)}"+''.join(f"[b{i}]" for i in range(len(pieces))))
# audio cut at same points as video pieces 0,1 and merge of 2-4 (continuous)
acuts=[(0,10.65),(11.02,19.02),(19.40,45.20)]
F[-1]=f"[1:a]aresample=48000,{ac},asplit={len(acuts)}"+''.join(f"[b{i}]" for i in range(len(acuts)))
for i,(a,b) in enumerate(acuts):
    F.append(f"[b{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.015,afade=t=out:st={b-a-0.015}:d=0.015[c{i}]")
F.append(f"[c0][c1][c2]concat=n=3:v=0:a=1[a2]")
F.append(f"[a1][a2]acrossfade=d={XF}:c1=tri:c2=tri[av]")
F.append(f"[av]loudnorm=I=-16:TP=-2:LRA=9,apad=whole_dur={TOT:.3f}[voice]")
F.append(f"[2:a]atrim=0:{TOT:.3f},volume='if(lt(t,{T3-0.3:.2f}),0.16,0.16+0.30*min(1,(t-{T3-0.3:.2f})/0.8))':eval=frame[mus]")
F.append(f"[voice][mus]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOT-1.2:.2f}:d=1.2[aout]")
cmd=['ffmpeg','-y','-v','error','-stats']+inp+['-filter_complex',';\n'.join(F),'-map','[vout]','-map','[aout]','-t',f'{TOT:.3f}','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',OUTF]
open(B+'/last_cmd.txt','w').write(' '.join(cmd))
print('total',TOT); subprocess.run(cmd,check=True)
