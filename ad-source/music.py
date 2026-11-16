import numpy as np, wave
SR=44100; DUR=25.0; N=int(SR*DUR)
rng=np.random.default_rng(7)
L=np.zeros(N+SR*4); R=np.zeros(N+SR*4)
def pluck(f,dur=2.6,bright=0.5):
    n=int(SR*dur); p=int(SR/f)
    buf=rng.uniform(-1,1,p)
    # soften excitation
    k=np.ones(3)/3
    for _ in range(int(3-2*bright)): buf=np.convolve(buf,k,mode='same')
    out=np.empty(n); 
    reps=n//p+1
    cur=buf
    chunks=[]
    for _ in range(reps):
        chunks.append(cur)
        cur=0.996*0.5*(cur+np.roll(cur,-1))
    out=np.concatenate(chunks)[:n]
    env=np.minimum(1,np.arange(n)/(0.004*SR))
    return out*env
def add(t,f,g=0.3,pan=0.5,dur=2.6,bright=0.5):
    s=pluck(f,dur,bright)*g; i=int(t*SR)
    L[i:i+len(s)]+=s*np.cos(pan*np.pi/2); R[i:i+len(s)]+=s*np.sin(pan*np.pi/2)
def pad(t,freqs,dur,g=0.05):
    n=int(dur*SR); x=np.arange(n)/SR
    env=np.clip(np.minimum(x/1.2,(dur-x)/1.5),0,1)
    s=sum(np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*f*2.003*x)+0.3*np.sin(2*np.pi*f*1.004*x) for f in freqs)*env*g
    i=int(t*SR); L[i:i+n]+=s; R[i:i+n]+=s
m=lambda n:440*2**((n-69)/12)
# D minor: Dm - Bb - F - C, 2.2s per bar, eighth = 0.275s
bar=2.2; e=bar/8
chords=[[50,57,62,65,69,74],[46,53,58,62,65,70],[41,53,57,60,65,69],[48,55,60,64,67,72]]
pat=[0,2,3,4,5,4,3,2]
for b in range(11):
    c=chords[b%4]; t0=b*bar
    if b==10: break
    pad(t0,[m(c[0]),m(c[2]),m(c[3])],bar+0.6)
    add(t0,m(c[0]-12),0.38,0.5,3.0,0.2)
    if b>=1:
        for i,p in enumerate(pat):
            add(t0+i*e,m(c[p]),0.22 if i%2 else 0.3,0.25+0.5*((i*3)%5)/4,2.4,0.6)
    else:
        for i,p in enumerate([0,2,3,5]): add(t0+i*2*e,m(c[p]),0.28,0.5)
    if b>=3:  # sparkle melody
        mel=[c[5]+12,c[4]+12,c[5]+12,c[3]+12]
        for i,nn in enumerate(mel): add(t0+i*2*e,m(nn),0.13,0.7,1.8,0.9)
# final glissando + chord at 19.8
t=22.0
for i,nn in enumerate([50,57,62,65,69,74,77,81,86]): add(t+i*0.055,m(nn),0.3,0.2+0.07*i,3.5,0.7)
pad(t,[m(50),m(57),m(65)],2.4,0.06)
# accents on scene changes
for t in [3.5,7.3,15.2,17.3]:
    for i,nn in enumerate([62,69,74,81]): add(t+i*0.05,m(nn),0.2,0.3+0.15*i,2.5,0.8)
st=np.stack([L[:N],R[:N]],1)
# simple reverb-ish delays
for d,g in [(0.11,0.25),(0.23,0.18),(0.37,0.12)]:
    k=int(d*SR); st[k:]+=st[:-k][:, ::-1]*g
st/=np.abs(st).max()/0.85
x=np.arange(N)/SR
st*=np.clip(np.minimum(x/0.3,(DUR-x)/1.2),0,1)[:,None]
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
