import numpy as np, wave, sys
sr=48000; D=float(sys.argv[1]); n=int(sr*D); t=np.arange(n)/sr
rng=np.random.default_rng(3)
bpm=104; beat=60/bpm
out=np.zeros(n)
def add(x,at):
    i=int(at*sr)
    if i>=n: return
    j=min(n,i+len(x)); out[i:j]+=x[:j-i]
def note(f,dur,amp,kind='pluck'):
    tt=np.arange(int(dur*sr))/sr
    w=np.sin(2*np.pi*f*tt)+0.4*np.sin(4*np.pi*f*tt)+0.15*np.sin(6*np.pi*f*tt)
    env=np.exp(-tt*(5 if kind=='pluck' else 0.6)); 
    if kind=='pad': env=np.minimum(1,tt/0.8)*np.minimum(1,(dur-tt)/0.8)
    return w*env*amp
chords=[(220.0,261.63,329.63),(174.61,220.0,261.63),(261.63,329.63,392.0),(196.0,246.94,293.66)]
bar=4*beat; nb=int(D/bar)+1
for b in range(nb):
    ch=chords[b%4]; at=b*bar
    for f in ch: add(note(f/2,bar+0.5,0.05,'pad'),at)
    add(note(ch[0]/4,beat*1.9,0.22,'pad'),at)
    arp=[ch[0],ch[1],ch[2],ch[1]*2,ch[2],ch[1],ch[0]*2,ch[2]]
    for k,f in enumerate(arp): add(note(f*2,beat,0.11),at+k*beat/2)
    for k in range(4):  # kick
        tt=np.arange(int(0.25*sr))/sr; kick=np.sin(2*np.pi*(55+90*np.exp(-tt*30))*tt)*np.exp(-tt*14)*0.5
        add(kick,at+k*beat)
    for k in range(8):  # hat
        tt=np.arange(int(0.05*sr))/sr; h=rng.standard_normal(len(tt))*np.exp(-tt*90)*0.05; h=np.diff(h,prepend=0)
        add(h,at+k*beat/2+beat/4)
def whoosh(at,dur=0.9):
    m=int(dur*sr); tt=np.arange(m)/sr; x=rng.standard_normal(m)
    y=np.zeros(m); a=0.02; s=0
    for i in range(m):
        a=0.02+0.5*(i/m)**2; s+=a*(x[i]-s); y[i]=s
    env=np.sin(np.pi*np.clip(tt/dur,0,1))**1.5
    add(y*env*1.4,at)
whoosh(float(sys.argv[2]))
out*=np.minimum(1,(D-t)/2.0)
out/=np.max(np.abs(out))*1.1
st=np.stack([out,out*0.98],1)
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
