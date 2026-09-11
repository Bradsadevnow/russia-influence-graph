/* Renderer for the Russia->US influence evidence graph.
   Reads the canonical ../graph/graph.json at runtime. No inlined data, no second taxonomy.
   publication.layer is authoritative; this file displays it, it does not decide it.
   Default = BACKBONE (9 intermediary architectures); click a vehicle to expand (focus);
   full 179-edge database is a toggle. */
const GRAPH_URL="../graph/graph.json";
const esc=s=>(s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
let NODES=[],EDGES=[],NBYID={},META={},VEH=new Set(),ADJ={};
let showLedger=false,showResearch=false,showDnc=true,showDomestic=true,showLabels=true;
let mode="backbone",focusId=null;          // backbone | full ; focusId set when a vehicle is expanded

fetch(GRAPH_URL).then(r=>{if(!r.ok)throw new Error("HTTP "+r.status);return r.json();}).then(init)
 .catch(e=>{document.getElementById("side").innerHTML=
   `<div class="err"><b>Could not load ${GRAPH_URL}</b><br><br>This renderer reads the repo's canonical graph.json directly, so it must be served over http (browsers block file:// fetches).<br><br>From the repo root:<br><code>python3 -m http.server 8000</code><br>then open <code>http://localhost:8000/renderer/index.html</code><br><br><small>${esc(e.message)}</small></div>`;});

function init(g){
  const ruV=n=>{const ap=n.arch_profile||{};const v=ap.is_russian_vehicle;return v&&typeof v==="object"?v.value:null;};
  NODES=g.nodes.map(n=>({...n,ru:ruV(n)}));
  NBYID=Object.fromEntries(NODES.map(n=>[n.id,n]));
  EDGES=g.edges.map(e=>{const pub=e.publication||{},cites=e.citations||(e.citation?[e.citation]:[]);
    return {id:e.id,s:e.source,t:e.target,es:e.evidence_state,layer:pub.layer,conf:e.confidence,
      rel:e.relationship_type||e.mechanism,domain:e.domain||"influence",claim:e.claim||"",
      scope:e.claim_scope,idc:e.identity_check,temp:e.temporal_check,disputed:!!e.disputed,
      contradiction:e.contradiction,pc:e.primary_candidate||{},cites};});
  VEH=new Set(NODES.filter(n=>(n.arch_profile||{}).intermediary_class).map(n=>n.id));
  ADJ={};NODES.forEach(n=>ADJ[n.id]=new Set());
  EDGES.forEach(e=>{if(ADJ[e.s]&&ADJ[e.t]){ADJ[e.s].add(e.t);ADJ[e.t].add(e.s);}});
  const c={pv:0,multi:0,dnc:0,con:0};
  EDGES.forEach(e=>{if(e.es==="primary_verified")c.pv++;else if(e.es==="multi_source_verified")c.multi++;
    else if(e.es==="negative_finding")c.dnc++;else if(e.es==="contested")c.con++;});
  META.counts=c;META.distinctions=(g.metadata||{}).architecture_distinctions||{};
  META.arch=NODES.filter(n=>(n.arch_profile||{}).intermediary_class).sort((a,b)=>String(a.arch_profile.era).localeCompare(String(b.arch_profile.era)));
  document.getElementById("s-pv").textContent=c.pv;document.getElementById("s-multi").textContent=c.multi;
  document.getElementById("s-dnc").textContent=c.dnc;document.getElementById("s-con").textContent=c.con;
  document.getElementById("side").innerHTML='<div class="hint">The 9 intermediary architectures are shown by era.<br><br>Click a vehicle to expand its people, organizations, edges &amp; evidence.<br><br>Then click any edge for the primary source.</div>';
  buildLegend();bindUI();relayout();updateBanner();
}

/* ---------- colour / lane / style ---------- */
function nodeColor(n){const ac=n.actor_class;
  if(ac==="RUSSIAN_STATE"||ac==="RUSSIAN_STATE_MEDIA")return "#e5484d";
  if(ac==="RUSSIAN_STATE_LINKED_PRIVATE")return "#f2663a";
  if(ac==="RUSSIAN_POLITICAL_ACTOR")return "#c94f8f";
  if(ac==="INTERMEDIARY")return "#e8a13a";
  if(n.layer==="us_media")return "#7aa2f7";if(n.layer==="us_political")return "#9d7cd8";
  if(n.layer==="content")return "#5bc0be";if(n.layer==="platform")return "#6b7280";return "#8b95a5";}
function lane(n){const ac=n.actor_class;
  if(ac==="RUSSIAN_STATE"||ac==="RUSSIAN_STATE_MEDIA"||ac==="RUSSIAN_POLITICAL_ACTOR")return 0;
  if(ac==="RUSSIAN_STATE_LINKED_PRIVATE")return 1;if(ac==="INTERMEDIARY")return 2;
  if(n.layer==="us_political"||n.layer==="us_media")return 3;if(n.layer==="content")return 4;return 5;}
function edgeStyle(e){
  if(e.es==="negative_finding")return{stroke:"#5c6270",w:1.4,dash:"5,5",op:.5};
  if(e.es==="contested"||e.disputed)return{stroke:"#e0a53a",w:1.7,dash:"6,4",op:.9};
  if(e.es==="primary_verified")return{stroke:"#4bb96b",w:2.2,dash:"",op:.92};
  if(e.es==="multi_source_verified")return{stroke:"#6ea8fe",w:2.0,dash:"",op:.92};
  return{stroke:"#8892a0",w:1.3,dash:"2,4",op:.6};}

/* ---------- visibility (persistent constellation: all nodes stay; selection lights edges + dims others) ---------- */
function baseVisible(e){
  if(e.layer==="research_graph")return showResearch;
  if(e.es==="negative_finding")return showDnc;
  if(e.layer==="evidence_ledger")return showLedger;
  if(e.domain==="domestic"||e.domain==="personnel")return showDomestic;
  return e.layer==="public_core";}
function edgeVisible(e){return baseVisible(e);}  // for the node panel's incident-edge list
let FOCUSSET=new Set(),FOCUSHOP={};
function bfsHops(seed,depth){const hop={};hop[seed]=0;let fr=[seed];
  for(let h=0;h<depth;h++){const nx=[];fr.forEach(id=>{EDGES.forEach(e=>{if(!baseVisible(e))return;
    if(e.s===id&&hop[e.t]===undefined){hop[e.t]=h+1;nx.push(e.t);}
    if(e.t===id&&hop[e.s]===undefined){hop[e.s]=h+1;nx.push(e.s);}});});fr=nx;}return hop;}
function computeFocus(){FOCUSHOP=focusId?bfsHops(focusId,2):{};FOCUSSET=new Set(Object.keys(FOCUSHOP));}
let hoverId=null,HOVERHOP={};
function computeHover(){HOVERHOP=hoverId?bfsHops(hoverId,1):{};}
function edgesToDraw(){
  if(mode==="full")return EDGES.filter(baseVisible);
  if(focusId)return EDGES.filter(e=>baseVisible(e)&&FOCUSSET.has(e.s)&&FOCUSSET.has(e.t));
  if(hoverId)return EDGES.filter(e=>baseVisible(e)&&(e.s===hoverId||e.t===hoverId));
  return EDGES.filter(e=>baseVisible(e)&&(VEH.has(e.s)||VEH.has(e.t)));  // landing: faint architecture backbone
}
/* ---------- layered layout over ALL nodes (computed once; stable across selection) ---------- */
const svg=document.getElementById("svg"),gEdges=document.getElementById("edges"),gNodes=document.getElementById("nodes"),gView=document.getElementById("view");
let W=1000,H=700,P={},TGT={},laidOut=false;
svg.insertAdjacentHTML("afterbegin",'<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#6b7280"/></marker></defs>');
function laneX(l){return (l+.5)/6*W;}
function assignAll(){
  const st=document.getElementById("stage").getBoundingClientRect();
  W=Math.max(600,st.width);H=Math.max(400,st.height);
  const cnt={},idx={};NODES.forEach(n=>{const l=lane(n);cnt[l]=(cnt[l]||0)+1;});
  NODES.forEach(n=>{const l=lane(n);idx[l]=idx[l]||0;const k=idx[l]++,c=cnt[l];
    TGT[n.id]={x:laneX(l),y:H*(0.05+0.90*((k+0.5)/c))};
    if(!P[n.id])P[n.id]={x:TGT[n.id].x+(Math.random()*20-10),y:TGT[n.id].y+(Math.random()*20-10)};});
}
function settle(){
  for(let i=0;i<NODES.length;i++)for(let j=i+1;j<NODES.length;j++){
    const a=P[NODES[i].id],b=P[NODES[j].id];let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+.01;
    if(d2<2600){const d=Math.sqrt(d2),fo=900/d2;a.x+=fo*dx/d;a.y+=fo*dy/d;b.x-=fo*dx/d;b.y-=fo*dy/d;}}
  NODES.forEach(n=>{const p=P[n.id],t=TGT[n.id];p.x+=(t.x-p.x)*.11;p.y+=(t.y-p.y)*.09;
    p.x=Math.max(30,Math.min(W-30,p.x));p.y=Math.max(34,Math.min(H-26,p.y));});
}
function relayout(){assignAll();let f=0;(function loop(){if(f++<200){settle();draw();requestAnimationFrame(loop);}else{laidOut=true;draw();}})();}
function draw(){
  const ed=edgesToDraw(),focusOn=!!focusId&&mode!=="full",hoverOn=!focusOn&&!!hoverId&&mode!=="full";
  const HOP = focusOn?FOCUSHOP:(hoverOn?HOVERHOP:null);
  function nOp(id){
    if(mode==="full")return 1;
    if(HOP){const h=HOP[id];if(h===0)return 1;if(h===1)return .85;if(h===2)return .45;return .20;}
    return VEH.has(id)?1:.55;                 // landing: vehicles prominent, rest present-but-quiet
  }
  gEdges.innerHTML=ed.map(e=>{const a=P[e.s],b=P[e.t];if(!a||!b)return"";const st=edgeStyle(e);
    let op=st.op;
    if(mode!=="full"&&!focusOn&&!hoverOn)op=st.op*0.42;         // subdued landing backbone
    return `<line data-e="${e.id}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${st.stroke}" stroke-width="${st.w}" stroke-dasharray="${st.dash}" opacity="${op}" marker-end="url(#arr)" style="cursor:pointer"/>`;}).join("");
  gNodes.innerHTML=NODES.map(n=>{const p=P[n.id];if(!p)return"";const c=nodeColor(n),veh=VEH.has(n.id),op=nOp(n.id);
    const r=veh?9:((n.layer==="platform"||n.type==="audience")?4.5:6.5);
    const ring=n.ru===true?'stroke="#e5484d" stroke-width="2.6"':(n.ru===false?'stroke="#4bb96b" stroke-width="2.6"':(veh?'stroke="#dfe6f2" stroke-width="1.6"':'stroke="#0e1116" stroke-width="1"'));
    // labels stay legible for the relevant set; vehicles always; unrelated stay dots (dim weight, not soup)
    const relevant = HOP ? (HOP[n.id]!==undefined) : (mode==="full"?showLabels:veh);
    const doLabel = veh || (relevant && (HOP? true : (mode==="full"&&showLabels)));
    const lblOp = Math.max(op,0.55);
    const lbl=doLabel?`<text x="${p.x+(veh?12:9)}" y="${p.y+4}" font-size="${veh?"12":"10.5"}" font-weight="${veh?"600":"400"}" fill="${veh?"#eef2f8":"#d3dae6"}" opacity="${lblOp}" style="pointer-events:none">${esc(n.label).slice(0,40)}</text>`:"";
    return `<g><circle data-n="${n.id}" cx="${p.x}" cy="${p.y}" r="${r}" fill="${c}" ${ring} opacity="${op}" style="cursor:pointer"/></g>${lbl}`;}).join("");
}

/* ---------- pan / zoom ---------- */
let tx=0,ty=0,scl=1,drag=null;
const applyT=()=>gView.setAttribute("transform",`translate(${tx},${ty}) scale(${scl})`);
svg.addEventListener("mousedown",e=>{if(e.target.dataset.n||e.target.dataset.e)return;drag={x:e.clientX,y:e.clientY,tx,ty};svg.style.cursor="grabbing";});
addEventListener("mousemove",e=>{if(!drag)return;tx=drag.tx+(e.clientX-drag.x);ty=drag.ty+(e.clientY-drag.y);applyT();});
addEventListener("mouseup",()=>{drag=null;svg.style.cursor="grab";});
svg.addEventListener("wheel",e=>{e.preventDefault();scl=Math.max(.3,Math.min(3.2,scl*(e.deltaY<0?1.1:.9)));applyT();},{passive:false});

/* ---------- banner (progressive-disclosure state) ---------- */
function updateBanner(){const b=document.getElementById("banner");
  if(mode==="full"){b.innerHTML=`<b>Full database view</b> &mdash; all ${META.counts.pv+META.counts.multi} verified + ${META.counts.dnc} not-established edges. <span class="muted">The explanation view is the architecture backbone.</span>`;return;}
  if(focusId){const n=NBYID[focusId],a=n.arch_profile||{};
    b.innerHTML=`<button class="back" id="btn-back">&larr; all 9 architectures</button> <b>${esc(n.label)}</b> <span class="pill">${esc(a.intermediary_class||"")}</span> <span class="pill">${esc(a.era||"")}</span> &mdash; <span class="muted">its people, organizations, edges &amp; evidence. Click any edge for the primary source.</span>`;
    document.getElementById("btn-back").onclick=()=>{focusId=null;computeFocus();draw();updateBanner();};return;}
  b.innerHTML=`<b>9 documented intermediary architectures</b>, by era. <span class="muted">Click a vehicle (large node) to expand its underlying people, organizations, edges &amp; evidence.</span>`;
}

/* ---------- inspector ---------- */
const side=document.getElementById("side");
function badge(es){const m={primary_verified:["b-pv","PRIMARY VERIFIED"],multi_source_verified:["b-multi","MULTI-SOURCE VERIFIED"],negative_finding:["b-dnc","NOT ESTABLISHED"],contested:["b-contested","CONTESTED"],reported:["b-reported","REPORTED"]};const x=m[es]||["b-reported",esc(es||"?")];return `<span class="badge ${x[0]}">${x[1]}</span>`;}
function cites(cs){return cs.map(c=>c.url?`<a class="cite" href="${esc(c.url)}" target="_blank" rel="noopener">${esc(c.publisher||"")} <span class="p">${c.primary?"· primary":""} ${esc(c.date||"")} ↗</span></a>`:`<span class="cite">${esc(c.publisher||"")}</span>`).join("");}
svg.addEventListener("click",e=>{const n=e.target.dataset.n,ed=e.target.dataset.e;
  if(n){const node=NBYID[n];if(mode!=="full"&&focusId!==n){focusId=n;hoverId=null;computeFocus();draw();updateBanner();}showNode(node);}
  else if(ed)showEdge(EDGES.find(x=>x.id===ed));
  else if(!n&&!ed&&focusId&&mode!=="full"){focusId=null;computeFocus();draw();updateBanner();side.innerHTML='<div class="hint">Selection cleared. Click any node to light up its relationships; click a vehicle to expand an architecture.</div>';}});
window.__pick=id=>{const e=EDGES.find(x=>x.id===id);if(e)showEdge(e);};
svg.addEventListener("mouseover",e=>{const id=e.target&&e.target.dataset&&e.target.dataset.n;if(id&&id!==hoverId&&!focusId){hoverId=id;computeHover();draw();}});
svg.addEventListener("mouseout",e=>{const id=e.target&&e.target.dataset&&e.target.dataset.n;if(id&&hoverId===id){hoverId=null;computeHover();draw();}});

function showEdge(e){const s=NBYID[e.s],t=NBYID[e.t],pc=e.pc||{},open=(e.cites.find(c=>c.url)||{}).url;
  side.innerHTML=`<h2>Relationship &middot; ${esc(e.rel||"")}</h2>
   <div class="rel"><b>${esc(s.label)}</b> &rarr; <b>${esc(t.label)}</b></div>
   ${badge(e.es)} <span class="pill">${esc(e.domain)}</span> ${e.scope&&e.scope!=="exact"?`<span class="pill">scope: ${esc(e.scope)}</span>`:""}
   <div class="claim">${esc(e.claim)}</div>
   ${pc.supporting_quote?`<h2>Support</h2><div class="quote">${esc(pc.supporting_quote)}</div>`:""}
   ${pc.document?`<div class="kv"><span class="k">document</span><span>${esc(pc.document)}</span>
      ${pc.section?`<span class="k">section</span><span>${esc(pc.section)}</span>`:""}
      ${pc.page?`<span class="k">page</span><span>${esc(pc.page)}</span>`:""}
      ${pc.proposition?`<span class="k">proposition</span><span>${esc(pc.proposition)}</span>`:""}</div>`:""}
   ${e.contradiction?`<div class="kv"><span class="k tag">contradiction</span><span>${esc(e.contradiction)}</span></div>`:""}
   <div class="kv"><span class="k">identity chk</span><span>${esc(e.idc||"—")}</span><span class="k">temporal chk</span><span>${esc(e.temp||"—")}</span></div>
   ${open?`<a class="openbtn" href="${esc(open)}" target="_blank" rel="noopener">Open primary &rarr;</a>`:""}
   <h2 style="margin-top:14px">Sources</h2>${cites(e.cites)||'<span class="muted">cites the absence (a preserved negative finding)</span>'}`;
}
function showNode(n){const ins=EDGES.filter(e=>e.t===n.id&&edgeVisible(e)),outs=EDGES.filter(e=>e.s===n.id&&edgeVisible(e));
  const li=e=>`<div class="edgeitem" onclick="window.__pick('${e.id}')">${badge(e.es)} ${esc(NBYID[e.s].label)} &rarr; ${esc(NBYID[e.t].label)}</div>`;
  let arch="";const a=n.arch_profile;
  if(a&&a.intermediary_class){const rv=a.is_russian_vehicle||{};
    arch=`<h2 style="margin-top:15px">Architecture profile</h2><div class="kv">
      <span class="k">class</span><span>${esc(a.intermediary_class)}</span><span class="k">era</span><span>${esc(a.era)}</span>
      <span class="k">principal</span><span>${esc(a.foreign_principal)}</span><span class="k">ownership</span><span>${esc(a.foreign_ownership)}</span>
      <span class="k">concealment</span><span>${esc(a.concealment)}</span>
      <span class="k">Russian vehicle?</span><span>${rv.value===true?"yes":"no"} <span class="muted">(${esc(rv.basis||"")})</span></span></div>
      ${mode==="backbone"&&focusId!==n.id?'<div class="muted" style="margin-top:8px">Click this vehicle in the graph to expand its subgraph.</div>':""}`;}
  side.innerHTML=`<h2>${esc(n.actor_class||n.layer||"")}</h2>
    <div class="rel"><b>${esc(n.label)}</b></div>
    ${n.ru===false?'<span class="badge b-pv">NOT a Russian vehicle</span>':""}
    <p class="muted">${esc(n.notes||"")}</p>${arch}
    ${outs.length?`<h2 style="margin-top:15px">Outgoing (${outs.length})</h2>${outs.map(li).join("")}`:""}
    ${ins.length?`<h2 style="margin-top:15px">Incoming (${ins.length})</h2>${ins.map(li).join("")}`:""}`;
}

/* ---------- legend / tools / tabs ---------- */
function buildLegend(){document.getElementById("legend").innerHTML=`
   <div class="row"><span class="sw" style="border-top:2.5px solid #4bb96b"></span>primary-verified</div>
   <div class="row"><span class="sw" style="border-top:2.5px solid #6ea8fe"></span>multi-source-verified</div>
   <div class="row"><span class="sw" style="border-top:2.5px dashed #e0a53a"></span>contested</div>
   <div class="row"><span class="sw" style="border-top:2.5px dashed #5c6270"></span>NOT established (kept)</div>
   <div class="row"><span class="sw" style="border-top:2.5px dotted #8892a0"></span>reported (ledger)</div>
   <div class="row" style="margin-top:6px"><span class="dot" style="background:#e5484d"></span>Russian state / media</div>
   <div class="row"><span class="dot" style="background:#e8a13a"></span>intermediary &nbsp;<span class="dot" style="background:#7aa2f7"></span>US media <span class="dot" style="background:#9d7cd8"></span>US political</div>
   <div class="row"><span class="dot" style="width:14px;height:14px;background:#e8a13a;border:1.6px solid #dfe6f2"></span>large + ring = an architecture vehicle</div>
   <div class="row"><span class="dot" style="background:#0e1116;border:2px solid #4bb96b"></span>green ring = NOT a Russian vehicle</div>`;}
function bindUI(){
  const cb=(id,fn)=>document.getElementById(id).addEventListener("change",e=>{fn(e.target.checked);computeFocus();draw();});
  cb("cb-dnc",v=>showDnc=v);cb("cb-domestic",v=>showDomestic=v);cb("cb-labels",v=>showLabels=v);
  document.getElementById("ly-ledger").onclick=e=>{showLedger=!showLedger;e.target.classList.toggle("on",showLedger);computeFocus();draw();};
  document.getElementById("ly-research").onclick=e=>{showResearch=!showResearch;e.target.classList.toggle("on",showResearch);computeFocus();draw();};
  const mb=document.getElementById("mode-backbone"),mf=document.getElementById("mode-full");
  mb.onclick=()=>{mode="backbone";focusId=null;computeFocus();mb.classList.add("on");mf.classList.remove("on");draw();updateBanner();};
  mf.onclick=()=>{mode="full";focusId=null;computeFocus();mf.classList.add("on");mb.classList.remove("on");draw();updateBanner();};
  document.querySelectorAll("button.tab").forEach(b=>b.onclick=()=>setTab(b.dataset.tab));
  addEventListener("resize",()=>relayout());
}
function setTab(t){
  document.querySelectorAll("button.tab").forEach(b=>b.classList.toggle("on",b.dataset.tab===t));
  document.getElementById("stage").style.display=t==="graph"?"block":"none";
  document.getElementById("side").style.display=t==="graph"?"block":"none";
  document.getElementById("app").style.gridTemplateColumns=t==="graph"?"1fr 400px":"1fr";
  const pa=document.getElementById("page-arch"),pd=document.getElementById("page-dnc");
  pa.classList.toggle("hidden",t!=="arch");pd.classList.toggle("hidden",t!=="dnc");
  if(t==="arch"&&!pa.dataset.done){pa.innerHTML=archView();pa.dataset.done="1";wireArch();}
  if(t==="dnc"&&!pd.dataset.done){pd.innerHTML=dncView();pd.dataset.done="1";}
  if(t==="graph")relayout();
}
function archView(){
  const rows=META.arch.map(n=>{const a=n.arch_profile,rv=a.is_russian_vehicle||{};
    return `<tr class="arow" data-v="${n.id}"><td>${esc(a.era)}</td><td><b>${esc(n.label)}</b></td><td>${esc(a.intermediary_class)}</td>
     <td>${esc(a.foreign_principal)}</td><td>${esc(a.foreign_ownership)}</td><td>${esc(a.concealment)}</td>
     <td class="${rv.value===false?"no":""}">${rv.value===true?"yes":"no ("+esc(rv.basis||"")+")"}</td></tr>`;}).join("");
  const d=META.distinctions,dl=Object.keys(d).map(k=>`<p><b>${esc(k)}</b> &mdash; ${esc(d[k])}</p>`).join("");
  return `<h2 class="big">The finding: Russia adapts the vehicle, not the architecture</h2>
   <p class="muted" style="max-width:1000px">${META.arch.length} documented intermediary vehicles across 2016&ndash;2024. The <b>intermediary class</b> changes at nearly every vehicle while the <b>shape</b> holds: foreign principal &rarr; intermediary &rarr; American-facing output &rarr; audience / Congress / courts. The "no" rows are contracted U.S. firms &mdash; the negative controls that keep the comparison honest. Architectural comparison, not a claim of one continuous operation. <span class="muted">Click a row to expand that vehicle in the graph.</span></p>
   <table><tr><th>era</th><th>vehicle</th><th>intermediary class</th><th>foreign principal</th><th>ownership</th><th>concealment</th><th>Russian vehicle?</th></tr>${rows}</table>
   ${dl?`<h2 class="big" style="margin-top:26px">Interaction modes</h2><div style="max-width:1000px">${dl}</div>`:""}`;
}
function wireArch(){document.querySelectorAll("tr.arow").forEach(r=>r.style.cursor="pointer");
  document.querySelectorAll("tr.arow").forEach(r=>r.onclick=()=>{mode="backbone";focusId=r.dataset.v;computeFocus();setTab("graph");document.querySelector('button.tab[data-tab="graph"]').classList.add("on");document.querySelector('button.tab[data-tab="arch"]').classList.remove("on");draw();updateBanner();showNode(NBYID[r.dataset.v]);});}
function dncView(){const rows=EDGES.filter(e=>e.es==="negative_finding").map(e=>`<tr><td><b>${esc(NBYID[e.s].label)} &rarr; ${esc(NBYID[e.t].label)}</b><div class="muted">${esc(e.claim)}</div></td><td>${cites(e.cites)||'<span class="muted">cites the absence</span>'}</td></tr>`).join("");
  return `<h2 class="big">What we do NOT claim (${META.counts.dnc})</h2>
   <p class="muted" style="max-width:1000px">These negative findings are kept as data, not hidden. A connection is not a conclusion; a documented event does not verify the interpretation someone might attach to it.</p>
   <table><tr><th>boundary</th><th>source</th></tr>${rows}</table>`;
}
