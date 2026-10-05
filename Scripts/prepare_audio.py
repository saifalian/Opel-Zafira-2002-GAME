import pathlib,wave,json,hashlib
import numpy as np
root=pathlib.Path('D:/blender/project/zafira/driving/audio');out=root/'processed';out.mkdir(exist_ok=True)
report={'authenticity':'NOT original Opel. CC0 Joseph Sardin BigSoundBank Iveco Daily 3.0 diesel fallback. Region selection algorithmic, not auditory verified.','assets':[]}
for name,src,start,length in [('DieselFallback_IdleLoop','FALLBACK_iveco_daily_3l_engine_BSB_1145.wav',8,8),('DieselFallback_RunLoop','FALLBACK_iveco_daily_3l_engine_BSB_1145.wav',20,8)]:
 p=root/'raw'/src
 with wave.open(str(p),'rb') as w:
  rate=w.getframerate();assert w.getnchannels()==1 and w.getsampwidth()==2;x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 x=x[int(start*rate):int((start+length)*rate)];x-=x.mean();n=int(.25*rate);fade=np.linspace(0,1,n);y=np.concatenate([x[n:-n],x[-n:]*(1-fade)+x[:n]*fade]);y*=.65/max(abs(y));data=(y*32767).astype('<i2').tobytes();dest=out/(name+'.wav')
 with wave.open(str(dest),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(data)
 report['assets'].append({'name':name,'source':src,'source_range_seconds':[start,start+length],'duration':len(y)/rate,'frames':len(y),'rms':float(np.sqrt(np.mean(y*y))),'peak':float(max(abs(y))),'loop_boundary_delta':float(abs(y[-1]-y[0])),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'path':str(dest)})
(out/'processing_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
