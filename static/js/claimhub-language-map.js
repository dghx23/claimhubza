(() => {
  const q = (s, root=document) => root.querySelector(s);
  const qa = (s, root=document) => [...root.querySelectorAll(s)];

  const story = [
    {
      label:"Everyday language",
      title:"What does it feel like?",
      copy:"Everyday words describe the person’s lived experience. They matter, but they do not by themselves establish the policy test.",
      question:"What is happening to me?",
      quote:"“I’m exhausted and I can’t keep up at work.”"
    },
    {
      label:"Medical language",
      title:"What condition or impairment is present?",
      copy:"Clinical language identifies diagnosis, symptoms, treatment and prognosis. It explains health, not automatically work incapacity.",
      question:"What is the clinical picture?",
      quote:"“Major depressive disorder with impaired concentration and sleep disturbance.”"
    },
    {
      label:"Functional language",
      title:"What can the person actually do?",
      copy:"Functional language translates symptoms into observable limits: concentration, stamina, attendance, travel, supervision, pace and error risk.",
      question:"Which activities are limited, and by how much?",
      quote:"“Can sustain focused work for 20–30 minutes before needing a break.”"
    },
    {
      label:"Policy language",
      title:"Does that functional impact meet the insured test?",
      copy:"Policy language applies the contract: material duties, own occupation, waiting period, exclusions and evidence requirements.",
      question:"Can the material duties of the insured occupation be performed?",
      quote:"“Unable to perform the material duties of own occupation throughout the waiting period.”"
    }
  ];

  function setStory(i) {
    const item = story[i] || story[0];
    qa("[data-story-step]").forEach((b, idx) => {
      b.classList.toggle("is-active", idx === i);
      b.setAttribute("aria-selected", idx === i ? "true" : "false");
    });
    const map = {
      "[data-story-label]": item.label,
      "[data-story-title]": item.title,
      "[data-story-copy]": item.copy,
      "[data-story-question]": item.question,
      "[data-story-quote]": item.quote
    };
    Object.entries(map).forEach(([sel, val]) => { const el=q(sel); if(el) el.textContent=val; });
  }
  qa("[data-story-step]").forEach((b,i)=>b.addEventListener("click",()=>setStory(i)));
  setStory(0);

  qa("[data-lane-jump]").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.laneJump;
      const target = q("#lane-" + CSS.escape(id));
      if (target) target.scrollIntoView({behavior:"smooth", block:"start"});
    });
  });

  qa("[data-ladder-rung]").forEach(btn => {
    const toggleRung = (e) => {
      if (e && e.target && e.target.closest && e.target.closest("a")) return;
      const open = btn.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      const toggle=q(".clm-rung-toggle",btn); if(toggle) toggle.textContent=open ? "−" : "+";
    };
    btn.addEventListener("click", toggleRung);
    btn.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleRung(e); }
    });
  });

  qa("[data-confusion-card]").forEach(card => {
    const btn=q("[data-confusion-toggle]",card);
    const back=q(".clm-confusion-back",card);
    if(!btn||!back) return;
    btn.addEventListener("click",()=>{
      const open=!back.hidden;
      back.hidden=open;
      btn.setAttribute("aria-expanded", open ? "false":"true");
      const hint=q("small",btn); if(hint) hint.textContent=open ? "Tap to unpack ↓":"Close comparison ↑";
    });
  });

  qa("[data-term-expand]").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const card=btn.closest("[data-term-card]");
      const detail=q(".clm-term-detail",card);
      if(!detail) return;
      const open=!detail.hidden;
      detail.hidden=open;
      btn.setAttribute("aria-expanded", open ? "false":"true");
      btn.firstChild.textContent=open ? "See what this means " : "Show less ";
      const sign=q("span",btn); if(sign) sign.textContent=open ? "+":"−";
    });
  });

  const search=q("#clm-term-search");
  const filters=qa("[data-lane-filter]");
  let lane="all";

  function applyFilters(){
    const needle=(search?.value||"").trim().toLowerCase();
    let visible=0;
    qa("[data-term-card]").forEach(card=>{
      const laneOk=lane==="all" || card.dataset.lane===lane;
      const searchOk=!needle || (card.dataset.search||"").includes(needle);
      const show=laneOk && searchOk;
      card.hidden=!show;
      if(show) visible++;
    });
    qa("[data-lane-section]").forEach(section=>{
      const any=qa("[data-term-card]",section).some(c=>!c.hidden);
      section.hidden=!any;
    });
    const count=q("#clm-result-count");
    if(count) count.textContent=visible + (visible===1 ? " term shown" : " terms shown");
    const empty=q("#clm-empty"); if(empty) empty.hidden=visible!==0;
  }

  filters.forEach(btn=>btn.addEventListener("click",()=>{
    lane=btn.dataset.laneFilter||"all";
    filters.forEach(b=>b.classList.toggle("is-active",b===btn));
    applyFilters();
  }));
  search?.addEventListener("input",applyFilters);
  applyFilters();
})();