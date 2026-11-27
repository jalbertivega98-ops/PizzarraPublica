
const $=s=>document.querySelector(s);
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=clamp(x,0,1);return 1-Math.pow(1-x,3)};
const back=x=>{x=clamp(x,0,1);const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
const soloEmoji=s=>/^(\p{Extended_Pictographic}|️|‍|\s){1,8}$/u.test(s);
const MAPSVG=`<svg viewBox="0 0 640 340" width="640" height="340"><rect width="640" height="340" fill="#e8eae0"/>
<rect x="0" y="0" width="200" height="120" fill="#cfe6c4"/><rect x="470" y="230" width="170" height="110" fill="#cfe6c4"/>
<g stroke="#fff" stroke-width="24" fill="none"><path d="M-10 100 L650 150"/><path d="M190 -10 L250 350"/><path d="M-10 270 L650 240"/><path d="M450 -10 L420 350"/></g>
<g stroke="#f7d774" stroke-width="12" fill="none"><path d="M-10 100 L650 150"/></g>
%%ICONO%%
<g transform="translate(335 145)"><path d="M0 0 C-28 -32 -28 -66 0 -66 C28 -66 28 -32 0 0Z" fill="#ea4335"/><circle cy="-44" r="11" fill="#7b1c14"/></g></svg>`;

window.setup=function(G,opt){
  window.G=G; opt=opt||{};
  $('#hook span').textContent=G.hook||'';
  $('#head .nm').textContent=G.chat;
  $('#head .av').textContent=(G.avatar||G.chat.match(/\p{Extended_Pictographic}/u)?.[0]||G.chat[0]);
  $('#final span').textContent=G.final||'';
  const yo=G.yo||'yo', L=$('#list'), P=G.personas||{};
  const otros=Object.keys(P).filter(k=>k!==yo);
  G._grupo=otros.length>1||G.grupo;
  let h=G.hora||'13:45'; let [hh,mm]=h.split(':').map(Number);
  $('#hora').textContent=h;
  if(G.fecha!==false){const r=document.createElement('div');r.className='row sis';r.innerHTML=`<div class="b sisb fecha">${G.fecha||'HOY'}</div>`;L.appendChild(r);}
  let prev=null;
  G.mensajes.forEach((m,i)=>{
    if(m.hora){[hh,mm]=m.hora.split(':').map(Number);}
    const hs=String(hh).padStart(2,'0')+':'+String(mm).padStart(2,'0');
    const r=document.createElement('div');
    const tipo=m.de==='sistema'?'sis':(m.de===yo?'yo':'otro');
    const tail=tipo!=='sis'&&prev!==m.de;
    r.className='row '+tipo+(tail?' tail':''); r.id='m'+i;
    const meta=`<span class="meta">${hs}${tipo==='yo'?'<span class="tk">✓✓</span>':''}</span>`;
    if(tipo==='sis') r.innerHTML=`<div class="b sisb">${esc(m.texto)}</div>`;
    else if(soloEmoji(m.texto)&&!m.tipo) r.innerHTML=`<div class="b big">${esc(m.texto)}</div>`;
    else{
      let who=(tipo==='otro'&&G._grupo&&tail)?`<div class="who" style="color:${P[m.de]?.color||'#1fa855'}">${esc(P[m.de]?.nombre||m.de)}</div>`:'';
      let body=m.tipo==='mapa'?`<div class="map">${MAPSVG.replace('%%ICONO%%', m.icono? `<text x="335" y="225" font-size="64" text-anchor="middle" font-family="Noto Color Emoji">${m.icono}</text>` : '<rect x="265" y="165" width="140" height="62" rx="8" fill="#f4c4c4"/><text x="335" y="207" font-size="34" text-anchor="middle" fill="#c62828" font-family="Inter" font-weight="800">H</text>')}</div><div class="maplbl">📍 ${esc(m.texto)}</div>`:esc(m.texto);
      r.innerHTML=`<div class="b">${who}${body}${meta}${m.reaccion?`<span class="rc">${m.reaccion}</span>`:''}</div>`;
      if(m.reaccion) r.classList.add('rx');
    }
    r.style.visibility='hidden'; L.appendChild(r);
    prev=m.de==='sistema'?null:m.de;
    if(m.minutos) mm+=m.minutos; while(mm>=60){mm-=60;hh=(hh+1)%24;}
  });
  // línea de tiempo
  let t=opt.inicio??1.2; const ev=[], T=[];
  const vel=G.velocidad||1;
  G.mensajes.forEach((m,i)=>{
    const n=(m.texto||'').length, p=m.pausa||0;
    if(m.de==='sistema'){T.push({i,show:t});ev.push({t,s:'sys'});t+=(1.2+p)/vel;return;}
    if(m.de===yo){
      const d=clamp(n*0.05,0.5,2.2)/vel; T.push({i,typeA:t,typeB:t+d,show:t+d+0.18});
      for(let k=0;k<n;k++) ev.push({t:t+d*k/n,s:'key'});
      t+=d+0.18; ev.push({t,s:'sent'}); t+=(clamp(0.5+n*0.03,0.7,1.8)+p)/vel; return;
    }
    const d=(m.tipo==='mapa'?1.0:clamp(0.4+n*0.022,0.6,1.5))/vel;
    T.push({i,dotsA:t,show:t+d,de:m.de}); t+=d; ev.push({t,s:'recv'});
    if(m.reaccion) {T[T.length-1].react={e:m.reaccion,t:t+0.9}; ev.push({t:t+0.9,s:'sys'});}
    t+=((m.tipo==='mapa'?1.8:clamp(0.55+n*0.04,0.8,3.0))+p)/vel;
  });
  G._T=T; G._final=t; G.dur=t+(G.final?3.0:0.8); G.ev=ev;
  G._bot=T.map(x=>{const e=$('#m'+x.i);return e.offsetTop+e.offsetHeight+10});
  G._top0=L.firstElementChild?L.firstElementChild.offsetTop+L.firstElementChild.offsetHeight+10:30;
  return {dur:G.dur,events:ev};
};

window.draw=function(t){
  const G=window.G,T=G._T,VH=document.getElementById('wall').clientHeight,TY=120;
  let typing=null, inText='', last=-1;
  const target=(k,extra)=>Math.max(0,(k>=0?G._bot[k]:G._top0)+extra-VH+(G._margen??30));
  T.forEach((x,k)=>{
    const e=document.getElementById('m'+x.i);
    if(t>=x.show){
      last=k; e.style.visibility='visible';
      const a=(t-x.show)/0.25;
      e.firstElementChild.style.transform=`scale(${0.6+0.4*back(a)})`;
      e.firstElementChild.style.transformOrigin=e.classList.contains('yo')?'right bottom':'left bottom';
      e.style.opacity=ease(a*1.5);
    } else e.style.visibility='hidden';
    if(x.dotsA!==undefined && t>=x.dotsA && t<x.show) typing=x;
    if(x.typeA!==undefined && t>=x.typeA && t<x.show){
      const s=G.mensajes[x.i].texto, n=Math.round(s.length*clamp((t-x.typeA)/(x.typeB-x.typeA),0,1));
      inText=s.slice(0,n);
    }
  });
  let from=0, at=-9, to=0;
  const valAt=(f,tt,a,now)=>f+(tt-f)*ease((now-a)/0.3);
  T.forEach((x,k)=>{
    if(x.dotsA!==undefined && t>=x.dotsA){ const tg=target(k-1,TY); if(tg!==to){from=valAt(from,to,at,x.dotsA);to=tg;at=x.dotsA;} }
    if(t>=x.show){ const tg=target(k,0); if(tg!==to){from=valAt(from,to,at,x.show);to=tg;at=x.show;} }
  });
  const cur=valAt(from,to,at,t);
  $('#list').style.transform=`translateY(${-cur}px)`;
  const ty=$('#typing');
  if(typing){
    ty.style.display='block'; const base=last>=0?G._bot[last]:G._top0; ty.style.top=(base+12-cur)+'px';
    ty.querySelectorAll('.dot').forEach((d,j)=>{d.style.transform=`translateY(${-9*Math.max(0,Math.sin((t*7)-j*0.9))}px)`;d.style.opacity=.55+.45*Math.max(0,Math.sin((t*7)-j*0.9))});
  } else ty.style.display='none';
  // reacciones
  T.forEach(x=>{ if(x.react){const e=document.querySelector('#m'+x.i+' .rc'); if(e) e.style.transform=`scale(${t>=x.react.t?back((t-x.react.t)/0.3):0})`;}});
  let nm=G.chat; T.forEach(x=>{const m=G.mensajes[x.i]; if(m.nuevoNombre&&t>=x.show) nm=m.nuevoNombre;}); $('#head .nm').textContent=nm;
  const P=G.personas||{};
  $('#head .st').textContent=typing?(G._grupo?(P[typing.de]||{}).nombre+' está escribiendo…':'escribiendo…'):(G._grupo?Object.keys(P).map(k=>P[k].nombre).join(', '):'en línea');
  $('#input .t').innerHTML=inText?'<b>'+esc(inText.length>24?'…'+inText.slice(-23):inText)+'</b><i class="cur"></i>':'Mensaje';
  $('#mic').style.display=inText?'none':'block'; $('#plane').style.display=inText?'block':'none';
  const hk=$('#hook'); const ha=t<3.6?ease(t/0.3):1-ease((t-3.6)/0.4);
  hk.style.opacity=G.hook?ha:0; hk.style.transform=`scale(${0.9+0.1*ha})`;
  const f=$('#final'); const fa=ease((t-G._final-0.3)/0.35);
  f.style.opacity=G.final?fa:0; f.style.transform=`scale(${0.85+0.15*back((t-G._final-0.3)/0.35)})`;
};
