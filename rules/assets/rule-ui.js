/* Editorial Workbench UI & Difficulty Router for HTML Branching Rule System */
(function () {
  "use strict";

  const THEME_KEY = "html-rule-harness-theme";
  const TIER_ORDER = { low: 0, mid: 1, high: 2 };
  const TIER_NAMES = ["low", "mid", "high"];
  const EFFORT_BY_TIER = { low: "low", mid: "medium", high: "high" };
  const ASCII_SHORT_KW = /^[a-z0-9_-]{1,4}$/;
  const GENERIC_STEM_STOPWORDS = new Set([
    "생성", "요약", "작업", "모델", "분석", "규칙", "설계", "기반", "검증", "방법", "결과", "시스템"
  ]);
  const ARGUMENT_NUANCE_CUES = ["다각도", "세부 비교", "조건별", "예외 사례", "tradeoff", "nuance"];
  const PILLAR_SIGNALS = {
    prompt: ["prompt", "few-shot", "json schema", "pydantic", "dspy", "프롬프트", "스키마"],
    context: ["context", "rag", "graphrag", "mem0", "memory", "compaction", "컨텍스트", "메모리", "검색"],
    harness: ["harness", "sandbox", "hook", "guardrail", "eval", "하네스", "샌드박스", "훅", "가드레일", "테스트 게이트"],
    loop: ["loop", "react", "reflexion", "evaluator-optimizer", "retry", "루프", "반복", "자가수정"],
    graph: ["graph", "langgraph", "adk", "workflow", "multi-agent", "hitl", "그래프", "멀티에이전트", "상태 전이"]
  };

  function escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function ico(name, extraClass = "") {
    const raw = (window.LUCIDE_ICONS && window.LUCIDE_ICONS[name]) || "";
    if (!raw) return "";
    return `<span class="ico ${extraClass}" aria-hidden="true">${raw}</span>`;
  }

  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY) || "light";
    document.documentElement.setAttribute("data-theme", saved);
  }

  function toggleTheme(btn) {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    const next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem(THEME_KEY, next);
    if (btn) updateThemeButton(btn, next);
  }

  function updateThemeButton(btn, theme) {
    const t = theme || document.documentElement.getAttribute("data-theme") || "light";
    btn.innerHTML = t === "dark"
      ? `${ico("sun", "ico-sm")}<span>Light</span>`
      : `${ico("moon", "ico-sm")}<span>Dark</span>`;
  }

  function loadScriptOnce(src, checkGlobal, cb) {
    if (checkGlobal()) {
      cb(checkGlobal());
      return;
    }
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => cb(checkGlobal() || null);
    s.onerror = () => cb(null);
    document.head.appendChild(s);
  }

  function relPrefixForDepth(depth) {
    if (!depth || depth <= 0) return "";
    return "../".repeat(depth);
  }

  function approxTokens(bytes) {
    return Math.max(1, Math.round(bytes / 3.6));
  }

  function buildChain(nodes, id) {
    const chain = [];
    const seen = new Set();
    let cur = nodes[id];
    while (cur && !seen.has(cur.rule_id)) {
      seen.add(cur.rule_id);
      chain.push(cur);
      cur = cur.parent ? nodes[cur.parent] : null;
    }
    return chain.reverse();
  }

  function keywordMatches(kw, queryLower) {
    if (ASCII_SHORT_KW.test(kw)) {
      const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      return new RegExp(`(?<![a-z0-9_])${escaped}(?![a-z0-9_])`).test(queryLower);
    }
    return queryLower.includes(kw);
  }

  function tokenize(text) {
    return new Set(((text || "").toLowerCase().match(/[a-z0-9가-힣_]+/g) || []));
  }

  function scoreNode(queryLower, qTokenSet, link, node) {
    let score = 0;
    (node.keywords || []).forEach((kw) => {
      if (keywordMatches(kw, queryLower)) {
        score += kw.includes(" ") || kw.length >= 4 ? 4.0 : 2.5;
      }
    });
    const text = `${link.when || ""} ${link.label || ""} ${node.title} ${node.summary}`.toLowerCase();
    const whenTokens = tokenize(text);
    const overlap = new Set();
    qTokenSet.forEach((qt) => {
      if (whenTokens.has(qt)) {
        overlap.add(qt);
        score += 2.2;
      }
    });
    qTokenSet.forEach((qt) => {
      if (overlap.has(qt) || qt.length < 2 || GENERIC_STEM_STOPWORDS.has(qt)) return;
      for (const wt of whenTokens) {
        if (wt.length < 2 || GENERIC_STEM_STOPWORDS.has(wt)) continue;
        if (qt.startsWith(wt) || wt.startsWith(qt)) {
          score += 1.6;
          break;
        }
      }
    });
    return score;
  }

  function routeTask(nodes, task) {
    const qLower = (task || "").toLowerCase();
    const qTokens = tokenize(task);
    let cur = nodes.root;
    const chain = [cur];
    while (cur && cur.children && cur.children.length) {
      let best = null;
      let bestScore = 0;
      for (const link of cur.children) {
        const child = nodes[link.target];
        if (!child) continue;
        let sc = scoreNode(qLower, qTokens, link, child);
        if (child.children && child.children.length) {
          let deepBest = 0;
          for (const gc of child.children) {
            if (nodes[gc.target]) {
              deepBest = Math.max(deepBest, scoreNode(qLower, qTokens, gc, nodes[gc.target]));
            }
          }
          sc += 0.75 * deepBest;
        }
        if (sc > bestScore) {
          bestScore = sc;
          best = child;
        }
      }
      if (!best || bestScore <= 0) break;
      chain.push(best);
      cur = best;
    }
    return chain;
  }

  function resolveAdaptationProfile(leaf) {
    const rid = leaf.rule_id || "";
    let policy = leaf.escalation_policy || "";
    if (!policy) {
      if (rid === "reasoning.root" || rid === "reasoning.simple-argument" || rid === "ai-systems.prompt-opt" || rid === "meta.model-policy") {
        policy = "overthinking-guard-low";
      } else if (rid.startsWith("research.") || rid === "ai-systems.context-rag") {
        policy = "grounding-over-thinking";
      } else if (leaf.tier === "high" || rid === "reasoning.structured-argument" || rid === "meta.skill-security") {
        policy = "capacity-switch-sensitive";
      } else {
        policy = "effort-first-with-verifier";
      }
    }
    let workload = leaf.workload || "";
    if (!workload) {
      if (rid === "reasoning.structured-argument") workload = "balanced_debate_reasoning";
      else if (policy === "grounding-over-thinking") workload = leaf.tier !== "low" ? "long_context_rag" : "fast_extraction";
      else if (leaf.tier === "high") workload = "frontier_architecture_visual";
      else if (leaf.tier === "low") workload = "fast_extraction";
      else workload = "verified_coding";
    }
    return { policy, workload };
  }

  function evaluateTier(leaf, signals) {
    const { policy, workload } = resolveAdaptationProfile(leaf);
    const hasVerifier = signals.hasVerifier !== false;
    let score = { low: 20, mid: 50, high: 80 }[leaf.tier] || 50;
    const reasons = [];
    if (signals.files >= 4) { score += 22; reasons.push(`결합 파일 ${signals.files}개 (+22)`); }
    else if (signals.files >= 2) { score += 10; reasons.push(`복수 파일 ${signals.files}개 (+10)`); }
    if (signals.attempts >= 2) { score += 25; reasons.push(`이전 실패 ${signals.attempts}회 (+25)`); }
    else if (signals.attempts === 1) { score += 12; reasons.push("이전 실패 1회 (+12)"); }
    if (signals.concurrency) { score += 30; reasons.push("동시성/비동기 (+30)"); }
    if (signals.security) { score += 25; reasons.push("보안/인증 경계 (+25)"); }
    if (signals.ambiguity) { score += 15; reasons.push("모호성 높음 (+15)"); }

    const tLow = (signals.task || "").toLowerCase();
    if (leaf.rule_id === "reasoning.simple-argument" && ARGUMENT_NUANCE_CUES.some((c) => tLow.includes(c))) {
      score += 10;
      reasons.push("조건·다각 비교 논증 (+10)");
    }

    score = Math.max(0, Math.min(100, score));
    let idx = TIER_ORDER[leaf.tier] ?? 1;
    if (signals.attempts >= 2 || signals.files >= 4) idx = Math.min(2, idx + 1);
    if (signals.concurrency || signals.security) idx = 2;

    const modalCeilingHit =
      !hasVerifier &&
      policy === "effort-first-with-verifier" &&
      (signals.attempts >= 1 || signals.files >= 2 || signals.ambiguity);
    if (modalCeilingHit) {
      idx = Math.min(2, Math.max(idx, (TIER_ORDER[leaf.tier] ?? 1) + 1));
      reasons.push("검증기 부재 Modal Ceiling (모델 전환)");
    }

    const groundingOnly =
      policy === "grounding-over-thinking" &&
      signals.ambiguity &&
      signals.attempts < 2 &&
      signals.files < 4 &&
      !signals.concurrency &&
      !signals.security;
    if (!groundingOnly) {
      if (score >= 75) idx = Math.max(idx, 2);
      else if (score >= 42) idx = Math.max(idx, 1);
    }

    const recTier = TIER_NAMES[idx];
    const escalated = recTier !== leaf.tier;
    let recEffort = leaf.effort;
    let decisionAction = "keep_optimal";
    let actionReason = "";

    if (escalated) {
      recEffort = (recTier === "high" || score >= 60) ? "high" : EFFORT_BY_TIER[recTier];
      decisionAction = "switch_model_up";
      actionReason = modalCeilingHit
        ? "외부 검증기(테스트/린터) 부재로 Modal Ceiling에 걸려 동일 모델 재시도 대신 상위 모델로 즉시 전환합니다."
        : `역량·결합도 임계 초과(${leaf.tier} → ${recTier})로 모델 자체를 변경하고 Effort(${recEffort})를 배정합니다.`;
    } else if (groundingOnly) {
      recEffort = leaf.effort;
      decisionAction = "ground_before_think";
      reasons.push("내부 추론 대신 검색·리랭킹 우선");
      actionReason = "내부 thinking 토큰을 늘려도 사실 확신 보정이 악화되므로(arXiv:2508.15050) 외부 검색 및 강력한 리랭커 전환(+7.5 NDCG@10)을 우선합니다.";
    } else {
      if (recTier === "low" && score >= 28 && leaf.effort === "low") {
        recEffort = "medium";
        reasons.push("동일 티어 Effort 조정 (low → medium)");
      } else if (recTier === "mid" && score >= 60 && leaf.effort !== "high") {
        recEffort = "high";
        reasons.push("동일 티어 Effort 조정 (medium → high)");
      }
      if (recEffort !== leaf.effort) {
        decisionAction = "raise_effort";
        actionReason = "외부 검증기(테스트/린터) 또는 경미한 조건 상승 구간 — 모델 변경 없이 동일 티어 내 Effort만 먼저 상향합니다.";
      } else {
        decisionAction = "keep_optimal";
        actionReason = policy === "overthinking-guard-low"
          ? "단순 과제 과잉 숙고 역전 방지(arXiv:2504.13367)를 위해 기본 티어·Effort를 유지합니다."
          : "현재 작업 난이도·정책 기준 최적 모델 티어와 Effort를 유지합니다.";
      }
    }
    const effortAdjusted = recEffort !== leaf.effort && !escalated;

    const skills = [...(leaf.skills || [])];
    if (recTier === "high" && !skills.includes("architecture-rfc")) skills.push("architecture-rfc");
    if (!skills.length && recTier === "mid") skills.push("targeted-debug");

    const pillars = [...(leaf.pillars || [])];
    if (!pillars.length) {
      if (recTier === "low") pillars.push("prompt");
      else if (recTier === "mid") pillars.push("harness", "loop");
      else pillars.push("context", "harness", "graph");
    }
    if (tLow) {
      for (const [pname, kws] of Object.entries(PILLAR_SIGNALS)) {
        if (kws.some((k) => tLow.includes(k)) && !pillars.includes(pname)) pillars.push(pname);
      }
    }
    if (signals.concurrency && !pillars.includes("graph")) pillars.push("graph");
    if (decisionAction === "ground_before_think" && !pillars.includes("context")) pillars.push("context");

    return {
      score, recTier, recEffort, effortAdjusted, decisionAction, actionReason,
      policy, workload, hasVerifier, skills, pillars, escalated, reasons
    };
  }

  function orderSkillPipeline(skills, hierarchy) {
    const meta = (hierarchy && hierarchy.skills) || {};
    const phases = (hierarchy && hierarchy.phases) || ["gate", "plan", "execute", "verify"];
    const pIdx = Object.fromEntries(phases.map((p, i) => [p, i]));
    const expanded = [...(skills || [])];
    for (const sk of [...expanded]) {
      for (const req of (meta[sk]?.requires || [])) {
        if (!expanded.includes(req)) expanded.push(req);
      }
    }
    const depDepth = (sk, seen = new Set()) => {
      if (seen.has(sk)) return 0;
      const reqs = meta[sk]?.requires || [];
      if (!reqs.length) return 0;
      const next = new Set(seen);
      next.add(sk);
      return 1 + Math.max(...reqs.map((r) => depDepth(r, next)));
    };
    const sorted = [...new Set(expanded)].sort((a, b) => {
      const ta = meta[a]?.hierarchy_tier ?? 9;
      const tb = meta[b]?.hierarchy_tier ?? 9;
      if (ta !== tb) return ta - tb;
      const pa = pIdx[meta[a]?.phase || "execute"] ?? 9;
      const pb = pIdx[meta[b]?.phase || "execute"] ?? 9;
      if (pa !== pb) return pa - pb;
      const da = depDepth(a);
      const db = depDepth(b);
      return da !== db ? da - db : a.localeCompare(b);
    });
    const blocked = new Set();
    const pipeline = [];
    for (const sk of sorted) {
      if (blocked.has(sk)) continue;
      (meta[sk]?.conflicts_with || []).forEach((c) => blocked.add(c));
      pipeline.push({
        name: sk,
        tier: meta[sk]?.hierarchy_tier ?? 2,
        phase: meta[sk]?.phase || "execute",
        trust: meta[sk]?.trust || "unverified"
      });
    }
    return pipeline;
  }

  function renderPillarBar(activePillars) {
    const all = ["prompt", "context", "harness", "loop", "graph"];
    const set = new Set(activePillars || []);
    return `<div class="rule-badges" style="margin-top:8px;">` +
      all.map((p) => `<span class="badge pillar-chip ${set.has(p) ? "on" : ""}">${p.toUpperCase()}</span>`).join("") +
      `</div>`;
  }

  function buildPacketXml(chain, rec, data, totalFileBytes) {
    const leaf = chain[chain.length - 1];
    const tierInfo = (data.catalog?.tiers || {})[rec.recTier] || {};
    const models = (tierInfo.candidates || []).map((c) => c.model).join(", ") || rec.recTier;
    const pipe = orderSkillPipeline(rec.skills, data.skill_hierarchy);
    const pipeNames = pipe.map((p) => p.name);
    const pipeStr = pipe.map((p) => `T${p.tier}:${p.phase}:${p.name}`).join(" -> ");
    const rulesXml = chain
      .flatMap((n) => (n.rules || []).map((r) => `    <r src="${n.rule_id}">${r}</r>`))
      .join("\n");
    const draft = [
      `<active_rule_packet branch="${leaf.rule_id}" depth="${leaf.depth}" tier="${rec.recTier}" effort="${rec.recEffort}" skills="${pipeNames.join(",")}" pillars="${rec.pillars.join(",")}" escalated="${rec.escalated}" saved_pct="0%">`,
      `  <path>${chain.map((n) => n.rule_id).join(" -> ")}</path>`,
      `  <adaptation action="${rec.decisionAction}" policy="${rec.policy}" workload="${rec.workload}">${rec.actionReason}</adaptation>`,
      `  <model_candidates role="reference_examples" note="Map tier/effort to actual models available in user runtime">${models}</model_candidates>`,
      pipeStr ? `  <skill_pipeline>${pipeStr}</skill_pipeline>` : null,
      rec.reasons.length ? `  <escalation_reasons>${rec.reasons.join("; ")}</escalation_reasons>` : null,
      `  <rules>`,
      rulesXml,
      `  </rules>`,
      leaf.escalation_note ? `  <escalate_if>${leaf.escalation_note}</escalate_if>` : null,
      `</active_rule_packet>`
    ].filter(Boolean).join("\n");

    const pktBytes = new Blob([draft]).size;
    const savedPct = totalFileBytes > 0 ? ((1 - pktBytes / totalFileBytes) * 100).toFixed(1) : "0.0";
    const finalXml = draft.replace('saved_pct="0%"', `saved_pct="${savedPct}%"`);
    return { xml: finalXml, pktBytes, pktTokens: approxTokens(pktBytes), savedPct, pipeline: pipe };
  }

  function enhanceBranchNode(main) {
    const id = main.dataset.ruleId;
    const depth = parseInt(main.dataset.depth || "0", 10);
    const tier = main.dataset.tier || "mid";
    const effort = main.dataset.effort || "medium";
    const skills = (main.dataset.skills || "").split(",").map((s) => s.trim()).filter(Boolean);
    const prefix = relPrefixForDepth(depth);

    const bar = document.createElement("header");
    bar.className = "topbar";
    bar.innerHTML = `
      <div class="topbar-inner">
        <div class="topbar-left">
          <a class="brand-pill" href="${prefix}index.html">Harness² Explorer</a>
          <nav class="crumbs" id="dynamic-crumbs"><span>${escapeHtml(id)}</span></nav>
        </div>
        <div class="topbar-actions">
          <span class="badge effort-low" id="node-token-pill">AI Context: loading...</span>
          <button class="btn" id="copy-ai-btn" type="button">Copy XML Packet</button>
          <button class="btn" id="theme-btn" type="button"></button>
        </div>
      </div>
    `;
    document.body.prepend(bar);
    const themeBtn = bar.querySelector("#theme-btn");
    updateThemeButton(themeBtn);
    themeBtn.addEventListener("click", () => toggleTheme(themeBtn));

    const head = main.querySelector("header.rule-head");
    if (head && !head.querySelector(".rule-eyebrow")) {
      const eb = document.createElement("div");
      eb.className = "rule-eyebrow";
      eb.textContent = `Depth ${depth} · ${id}`;
      head.prepend(eb);
    }
    if (head && !head.querySelector(".rule-badges")) {
      const tierKo = { low: "하위 모델", mid: "중위 모델", high: "상위 모델" }[tier] || tier;
      const pillars = (main.dataset.pillars || "").split(",").map((s) => s.trim()).filter(Boolean);
      const badges = document.createElement("div");
      badges.className = "rule-badges";
      badges.innerHTML = `
        <span class="badge tier-${tier}">Model Tier: ${tier} (${tierKo})</span>
        <span class="badge effort-${effort}">Effort: ${effort}</span>
        ${skills.map((s) => `<span class="badge skill-chip">${escapeHtml(s)}</span>`).join("")}
      `;
      head.appendChild(badges);
      if (pillars.length) {
        const pWrap = document.createElement("div");
        pWrap.innerHTML = renderPillarBar(pillars);
        head.appendChild(pWrap.firstElementChild);
      }
    }
    main.querySelectorAll("a.branch-link").forEach((a) => {
      if (!a.querySelector("span")) {
        const t = a.dataset.tier || "mid";
        const sp = document.createElement("span");
        sp.textContent = `기본 권장 티어: ${t}`;
        a.appendChild(sp);
      }
    });

    loadScriptOnce(prefix + "assets/lucide-icons.js", () => window.LUCIDE_ICONS, () => {
      updateThemeButton(themeBtn);
    });

    loadScriptOnce(prefix + "assets/tree-data.js", () => window.RULE_TREE_DATA, (data) => {
      if (!data || !data.nodes || !data.nodes[id]) {
        const bytes = new Blob([main.outerHTML]).size;
        bar.querySelector("#node-token-pill").textContent = `Node ~${approxTokens(bytes)} tok (${bytes} B)`;
        return;
      }
      const nodes = data.nodes;
      const totalFileBytes = Object.values(nodes).reduce((a, b) => a + b.file_bytes, 0);
      const chain = buildChain(nodes, id);
      const leaf = chain[chain.length - 1];
      const rec = evaluateTier(leaf, { files: 1, attempts: 0 });
      const pkt = buildPacketXml(chain, rec, data, totalFileBytes);

      bar.querySelector("#node-token-pill").textContent =
        `Packet ~${pkt.pktTokens} tok (${pkt.savedPct}% saved)`;

      const crumbs = bar.querySelector("#dynamic-crumbs");
      crumbs.innerHTML = `<a href="${prefix}index.html">Explorer</a>` +
        chain.map((n) => ` / <a href="${prefix}${n.rel_path}">${escapeHtml(n.rule_id)}</a>`).join("");

      const copyBtn = bar.querySelector("#copy-ai-btn");
      copyBtn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(pkt.xml);
          copyBtn.textContent = "Copied!";
          setTimeout(() => (copyBtn.textContent = "Copy XML Packet"), 1600);
        } catch {
          alert(pkt.xml);
        }
      });

      if (leaf.skills && leaf.skills.length && data.skills) {
        const pipe = orderSkillPipeline(leaf.skills, data.skill_hierarchy);
        const sec = document.createElement("section");
        sec.className = "rule-card";
        sec.innerHTML = `<h2>연계 Skill 파이프라인 (.agents/skills)</h2>` +
          pipe.map((p) => `<div class="skill-card"><strong>[T${p.tier} · ${p.phase}] ${escapeHtml(p.name)}</strong> <code>${escapeHtml(p.trust)}</code> — ${escapeHtml(data.skills[p.name] || "")}</div>`).join("");
        main.appendChild(sec);
      }
    });
  }

  function enhanceExplorer(rootEl) {
    const bar = document.createElement("header");
    bar.className = "topbar";
    bar.innerHTML = `
      <div class="topbar-inner">
        <div class="topbar-left">
          <span class="brand-pill" id="brand-pill">${ico("git-branch", "ico-sm")}<span>Google Harness² · HTML Rule Explorer</span></span>
          <a class="btn subtle" href="router.html">${ico("compass", "ico-sm")}<span>Minimal Root (router.html)</span></a>
        </div>
        <div class="topbar-actions">
          <button class="btn" id="theme-btn" type="button"></button>
        </div>
      </div>
    `;
    document.body.prepend(bar);
    const themeBtn = bar.querySelector("#theme-btn");
    updateThemeButton(themeBtn);
    themeBtn.addEventListener("click", () => toggleTheme(themeBtn));

    loadScriptOnce("assets/tree-data.js", () => window.RULE_TREE_DATA, (data) => {
      if (!data || !data.nodes) {
        rootEl.innerHTML = `<div class="panel"><code>rules/assets/tree-data.js</code>를 로드하지 못했습니다. <code>python scripts/validate_harness.py</code>를 실행하세요.</div>`;
        return;
      }
      renderExplorerUI(rootEl, data);
      loadScriptOnce("assets/lucide-icons.js", () => window.LUCIDE_ICONS, () => {
        const bp = document.getElementById("brand-pill");
        if (bp) bp.innerHTML = `${ico("git-branch", "ico-sm")}<span>Google Harness² · HTML Rule Explorer</span>`;
        updateThemeButton(themeBtn);
      });
    });
  }

  function renderExplorerUI(rootEl, data) {
    const nodes = data.nodes;
    const allList = Object.values(nodes);
    const totalFileBytes = allList.reduce((a, n) => a + n.file_bytes, 0);
    const totalAiBytes = allList.reduce((a, n) => a + n.ai_bytes, 0);

    const presets = [
      { label: "단순 논증 (하위)", task: "간단한 논증으로 핵심 장단점 3줄 요약 생성해줘", files: 1, attempts: 0, concurrency: false, security: false, ambiguity: false, hasVerifier: true },
      { label: "모호한 단순 논증 (Effort↑)", task: "간단한 논증으로 핵심 장단점 3줄 요약 생성해줘", files: 1, attempts: 0, concurrency: false, security: false, ambiguity: true, hasVerifier: true },
      { label: "찬반·반론 논증 (중위)", task: "원격근무 의무화 찬반 양측 논거와 반론을 균형있게 논증해줘", files: 1, attempts: 0, concurrency: false, security: false, ambiguity: false, hasVerifier: true },
      { label: "심층 교차 논증 (상위)", task: "상충하는 학술 논문 근거를 대조해 장기 전략을 심층 논증해줘", files: 2, attempts: 0, concurrency: false, security: false, ambiguity: false, hasVerifier: true },
      { label: "디버깅·1회실패+테스트 (Effort↑)", task: "TypeError 스택 트레이스 디버깅하고 버그 코드 수정해줘", files: 1, attempts: 1, concurrency: false, security: false, ambiguity: false, hasVerifier: true },
      { label: "디버깅·검증기없음 (모델전환)", task: "TypeError 스택 트레이스 디버깅하고 버그 코드 수정해줘", files: 1, attempts: 1, concurrency: false, security: false, ambiguity: false, hasVerifier: false },
      { label: "RAG·모호성 (검색·리랭킹)", task: "장기 메모리 Mem0와 Compaction으로 RAG Context Rot 방지", files: 1, attempts: 0, concurrency: false, security: false, ambiguity: true, hasVerifier: true },
      { label: "구조화 출력 [Prompt]", task: "Prompt Chaining과 Pydantic JSON 스키마로 데이터 추출", files: 1, attempts: 0, concurrency: false, security: false, ambiguity: false, hasVerifier: true },
      { label: "멀티에이전트 [Graph+Combo]", task: "LangGraph 상태 그래프와 기법 조합으로 장기 HITL 워크플로우 구축", files: 5, attempts: 0, concurrency: false, security: true, ambiguity: false, hasVerifier: true },
      { label: "탁월한 비주얼 UI [Frontier]", task: "최상위 모델로 Anti-Slop 디자인 시스템과 스크린샷 루프 기반 뛰어난 UI 생성", files: 3, attempts: 0, concurrency: false, security: false, ambiguity: false, hasVerifier: true },
      { label: "악성 스킬 검역 [Security]", task: "외부 SKILL.md 프롬프트 인젝션과 크리덴셜 유출 차단 악성 스킬 검역", files: 1, attempts: 0, concurrency: false, security: false, ambiguity: false, hasVerifier: true }
    ];

    let state = {
      task: presets[0].task,
      branchOverride: null,
      files: 1,
      attempts: 0,
      concurrency: false,
      security: false,
      ambiguity: false,
      hasVerifier: true,
      treeFilter: "",
      collapsedIds: new Set(["coding.root", "research.root", "ai-systems.root", "meta.root"]),
      activePresetIdx: 0
    };

    rootEl.innerHTML = `
      <section class="hero-band">
        <div class="panel hero-panel">
          <div>
            <div class="rule-eyebrow">${ico("layers", "ico-sm")}<span>Progressive Disclosure · Difficulty-Aware Routing</span></div>
            <h1>HTML 분기형 AI 규칙 · 모델 라우팅 Explorer</h1>
            <p class="rule-summary">작업 의도와 실증 난이도 신호에 따라 <strong>단일 분기 체인</strong>만 탐색해 컨텍스트를 94%+ 절감하고, 동일 티어 내 Effort 우선 보정(<code>arXiv:2510.27042</code>)과 모델 티어·Skill 파이프라인을 결정적으로 산출합니다.</p>
            <aside class="hero-advisory" aria-label="모델 매핑 및 일반 규칙 유의사항">
              <div class="advisory-row">${ico("info", "ico-sm")}<div><strong>모델명 · Effort 참고 기준:</strong> 아래 표기된 모델명은 AI 모델·도구가 참고할 수 있는 티어 예시이며, 실제 실행 시에는 <strong>사용자 환경에서 호출 가능한 최신 모델과 Effort 파라미터</strong>에 맞춰 적용해야 합니다.</div></div>
              <div class="advisory-row">${ico("triangle-alert", "ico-sm")}<div><strong>일반 규칙 한계:</strong> 본 규칙과 임계치는 일반적인 기준선(Baseline)을 담은 것으로, <strong>작업자의 실행 환경(과금·검증기 유무·지연)과 작업 세부사항</strong>에 따라 기대한 성능 향상 및 비용 절감 효과를 얻지 못할 수 있습니다.</div></div>
            </aside>
          </div>
          <div class="sim-presets" id="preset-row" aria-label="대표 시나리오 프리셋"></div>
        </div>

        <div class="panel metrics-grid" aria-label="트리 요약 지표">
          <div class="metric-box"><div class="val">${allList.length}</div><div class="lbl">HTML 분기 노드</div></div>
          <div class="metric-box"><div class="val">${Object.keys(data.skills || {}).length}</div><div class="lbl">On-Demand Skills</div></div>
          <div class="metric-box"><div class="val">${approxTokens(totalFileBytes)} tok</div><div class="lbl">전체 로드 비용</div></div>
          <div class="metric-box"><div class="val accent" id="metric-saved">-</div><div class="lbl">활성 체인 절감률</div></div>
        </div>
      </section>

      <section class="workspace-grid">
        <div class="panel">
          <div class="panel-head-row">
            <h2>${ico("folder-tree")}<span>1. 계층형 분기 트리</span></h2>
            <button class="btn xs subtle" id="toggle-collapse-all" type="button">모두 펼치기</button>
          </div>
          <div class="tree-toolbar">
            <div class="search-wrap">
              <span class="search-ico">${ico("search", "ico-sm")}</span>
              <input id="tree-filter" type="text" placeholder="분기·키워드 검색 (예: 반론, loop, security)..." aria-label="분기 검색">
              <span class="kbd-hint">/</span>
            </div>
          </div>
          <div class="tree-scroll" id="tree-view"></div>
        </div>

        <div class="panel sim-controls">
          <div class="panel-head-row">
            <h2>${ico("sliders-horizontal")}<span>2. 작업 난이도 · 모델 · Effort 시뮬레이터</span></h2>
          </div>

          <div class="mode-banner" id="mode-banner"></div>

          <input id="task-input" type="text" value="${escapeHtml(state.task)}" placeholder="수행할 작업을 자연어로 입력해 보세요..." aria-label="작업 입력">

          <div class="signal-grid">
            <div class="signal-box">
              <span>결합 파일</span>
              <select id="sig-files" aria-label="결합 파일 수">
                <option value="1">1개</option>
                <option value="2">2~3개 (+10)</option>
                <option value="4">4개+ (+22, 승격)</option>
              </select>
            </div>
            <div class="signal-box">
              <span>이전 실패</span>
              <select id="sig-attempts" aria-label="이전 실패 횟수">
                <option value="0">0회</option>
                <option value="1">1회 (+12)</option>
                <option value="2">2회+ (+25, 승격)</option>
              </select>
            </div>
            <div class="signal-box"><label><input id="sig-verifier" type="checkbox" checked><span>외부 검증기(테스트)</span></label></div>
            <div class="signal-box"><label><input id="sig-amb" type="checkbox"><span>모호/다각 조건 (+15)</span></label></div>
            <div class="signal-box"><label><input id="sig-conc" type="checkbox"><span>동시성/비동기 (+30)</span></label></div>
            <div class="signal-box"><label><input id="sig-sec" type="checkbox"><span>보안/인증 경계 (+25)</span></label></div>
          </div>

          <div id="sim-result"></div>
        </div>
      </section>

      <details class="builder-drawer">
        <summary>
          <span style="display:inline-flex;align-items:center;gap:8px;">${ico("file-code")}<span>3. 커스텀 작업 분기 HTML 노드 템플릿 빌더 (Propose–Probe–Compose)</span></span>
          <span class="badge effort-low">클릭해 열기/닫기</span>
        </summary>
        <div class="builder-body">
          <p class="rule-summary" style="margin:0;">새 도메인·난이도 전용 HTML 규칙 노드를 생성해 <code>rules/branches/&lt;domain&gt;/</code>에 저장하고 <code>python scripts/validate_harness.py</code>로 동기화합니다.</p>
          <div class="input-row">
            <input id="cb-id" type="text" placeholder="rule_id (예: coding.sql-tuning)" value="coding.sql-tuning">
            <input id="cb-title" type="text" placeholder="제목" value="SQL 쿼리 성능 튜닝">
            <select id="cb-tier"><option value="low">low (하위)</option><option value="mid" selected>mid (중위)</option><option value="high">high (상위)</option></select>
            <select id="cb-effort"><option value="low">effort: low</option><option value="medium" selected>effort: medium</option><option value="high">effort: high</option></select>
            <input id="cb-skill" type="text" placeholder="skill" value="targeted-debug">
            <button class="btn primary" id="cb-copy" type="button">${ico("copy", "ico-sm")}<span>HTML 템플릿 복사</span></button>
          </div>
          <div class="packet-wrap">
            <div class="packet-head"><span>new-rule-node.html (Preview)</span></div>
            <pre class="packet-box" id="cb-preview"></pre>
          </div>
        </div>
      </details>

      <footer class="credits-footer" aria-label="오픈소스 스톡 라이선스 및 참고 문헌 크레딧">
        <div class="panel-head-row" style="margin:0;">
          <h2>${ico("award")}<span>Credits &amp; Commercially-Free Open-Source Assets</span></h2>
          <a class="btn xs" href="../reference/ui-ux-and-stock-credits.md" target="_blank" rel="noopener">${ico("book-open", "ico-sm")}<span>전체 크레딧·HCI 근거 문서</span></a>
        </div>
        <div class="credits-grid">
          <div class="credit-card">
            <strong><span>Lucide Icons v0.460.0</span><span class="credit-lic">ISC / MIT</span></strong>
            <p>Lucide Contributors &amp; Cole Bemis(Feather). 본 Explorer 전체 SVG UI 아이콘. <a href="assets/licenses/lucide-LICENSE.txt" target="_blank">LICENSE</a></p>
          </div>
          <div class="credit-card">
            <strong><span>Pretendard Variable v1.3.9</span><span class="credit-lic">SIL OFL 1.1</span></strong>
            <p>Kil Hyung-jin(orioncactus). 한글·영문 가변 산세리프 UI 본문 서체. <a href="assets/licenses/pretendard-OFL.txt" target="_blank">OFL 1.1</a></p>
          </div>
          <div class="credit-card">
            <strong><span>IBM Plex Sans KR</span><span class="credit-lic">SIL OFL 1.1</span></strong>
            <p>IBM Corp. &amp; Sandoll. 에디토리얼 가독성 보조 산세리프 서체. <a href="assets/licenses/ibm-plex-OFL.txt" target="_blank">OFL 1.1</a></p>
          </div>
          <div class="credit-card">
            <strong><span>JetBrains Mono</span><span class="credit-lic">SIL OFL 1.1</span></strong>
            <p>JetBrains s.r.o. XML 패킷·노드 ID·토큰 수치 고정폭 서체. <a href="assets/licenses/jetbrains-mono-OFL.txt" target="_blank">OFL 1.1</a></p>
          </div>
        </div>
      </footer>
    `;

    const presetRow = rootEl.querySelector("#preset-row");
    function renderPresets() {
      presetRow.innerHTML = "";
      presets.forEach((p, idx) => {
        const b = document.createElement("button");
        b.className = `preset-btn ${state.activePresetIdx === idx && !state.branchOverride ? "active" : ""}`;
        b.type = "button";
        b.textContent = p.label;
        b.addEventListener("click", () => {
          state.task = p.task;
          state.branchOverride = null;
          state.files = p.files;
          state.attempts = p.attempts;
          state.concurrency = p.concurrency;
          state.security = p.security;
          state.ambiguity = p.ambiguity;
          state.hasVerifier = p.hasVerifier !== false;
          state.activePresetIdx = idx;
          rootEl.querySelector("#task-input").value = p.task;
          rootEl.querySelector("#sig-files").value = String(p.files);
          rootEl.querySelector("#sig-attempts").value = String(p.attempts);
          rootEl.querySelector("#sig-conc").checked = p.concurrency;
          rootEl.querySelector("#sig-sec").checked = p.security;
          rootEl.querySelector("#sig-amb").checked = p.ambiguity;
          rootEl.querySelector("#sig-verifier").checked = state.hasVerifier;
          update();
        });
        presetRow.appendChild(b);
      });
    }

    function matchesFilter(node, q) {
      if (!q) return true;
      const hay = `${node.rule_id} ${node.title} ${node.summary} ${(node.keywords || []).join(" ")} ${(node.skills || []).join(" ")}`.toLowerCase();
      return hay.includes(q);
    }

    function subtreeMatches(nodeId, q) {
      const n = nodes[nodeId];
      if (!n) return false;
      if (matchesFilter(n, q)) return true;
      return (n.children || []).some((c) => subtreeMatches(c.target, q));
    }

    function renderTree(parentId, pathSet, selectedId) {
      const children = allList.filter((n) => n.parent === parentId);
      if (!children.length) return "";
      const fq = state.treeFilter.trim().toLowerCase();

      return children.map((n) => {
        if (fq && !subtreeMatches(n.rule_id, fq)) return "";
        const childNodes = allList.filter((c) => c.parent === n.rule_id);
        const hasKids = childNodes.length > 0;
        const onPath = pathSet.has(n.rule_id);
        const collapsed = !fq && !onPath && state.collapsedIds.has(n.rule_id);

        return `
          <div>
            <div class="tree-node-card ${n.rule_id === selectedId ? "selected" : ""} ${onPath ? "on-path" : ""}" data-pick="${escapeHtml(n.rule_id)}">
              <div class="tree-row-top">
                <div class="tree-title-wrap">
                  ${hasKids ? `<button class="tree-toggle" type="button" data-toggle="${escapeHtml(n.rule_id)}" aria-label="하위 분기 접기/펼치기">${ico(collapsed ? "chevron-right" : "chevron-down", "ico-sm")}</button>` : ""}
                  <span class="tree-title">${escapeHtml(n.title)}</span>
                </div>
                <div class="rule-badges" style="flex-shrink:0;">
                  <span class="badge tier-${n.tier}">${n.tier}</span>
                  <span class="badge effort-${n.effort}">${n.effort}</span>
                </div>
              </div>
              <div class="tree-meta">
                <span><code>${escapeHtml(n.rule_id)}</code> · ~${approxTokens(n.ai_bytes)} tok</span>
                <a class="btn xs" href="${escapeHtml(n.rel_path)}" onclick="event.stopPropagation();">${ico("external-link", "ico-sm")}<span>HTML</span></a>
              </div>
            </div>
            ${hasKids ? `<div class="tree-children ${collapsed ? "collapsed" : ""}">${renderTree(n.rule_id, pathSet, selectedId)}</div>` : ""}
          </div>
        `;
      }).join("");
    }

    function renderModeBanner(leaf) {
      const banner = rootEl.querySelector("#mode-banner");
      if (state.branchOverride) {
        banner.className = "mode-banner manual";
        banner.innerHTML = `
          <span class="mode-banner-text">${ico("triangle-alert", "ico-sm")}<span><strong>트리 항목 직접 선택 중:</strong> <code>${escapeHtml(leaf.rule_id)}</code> (아래 입력창 기준 자동 분류가 일시 정지되었습니다)</span></span>
          <button class="btn xs primary" id="reset-auto-btn" type="button">${ico("rotate-ccw", "ico-sm")}<span>수동 선택 해제 · 입력값으로 자동 분류</span></button>
        `;
        banner.querySelector("#reset-auto-btn").addEventListener("click", () => {
          state.branchOverride = null;
          update();
        });
      } else {
        banner.className = "mode-banner";
        banner.innerHTML = `
          <span class="mode-banner-text">${ico("zap", "ico-sm")}<span><strong>자동 분류 모드:</strong> 아래 입력 작업과 난이도 신호에 맞춰 분기·모델·Effort가 자동 선택됩니다</span></span>
        `;
      }
    }

    function update() {
      const chain = state.branchOverride ? buildChain(nodes, state.branchOverride) : routeTask(nodes, state.task);
      const leaf = chain[chain.length - 1];
      const rec = evaluateTier(leaf, state);
      const pkt = buildPacketXml(chain, rec, data, totalFileBytes);
      const pathSet = new Set(chain.map((n) => n.rule_id));

      renderPresets();
      renderModeBanner(leaf);
      rootEl.querySelector("#metric-saved").textContent = `${pkt.savedPct}%`;

      const treeView = rootEl.querySelector("#tree-view");
      treeView.innerHTML = renderTree("", pathSet, leaf.rule_id) || `<div style="padding:12px;color:var(--text-muted);font-size:0.84rem;">일치하는 분기가 없습니다.</div>`;

      treeView.querySelectorAll("[data-toggle]").forEach((btn) => {
        btn.addEventListener("click", (ev) => {
          ev.stopPropagation();
          const tid = btn.getAttribute("data-toggle");
          if (state.collapsedIds.has(tid)) state.collapsedIds.delete(tid);
          else state.collapsedIds.add(tid);
          update();
        });
      });

      treeView.querySelectorAll("[data-pick]").forEach((el) => {
        el.addEventListener("click", () => {
          const id = el.getAttribute("data-pick");
          state.collapsedIds.delete(id);
          if (nodes[id]?.parent) state.collapsedIds.delete(nodes[id].parent);
          state.branchOverride = id;
          update();
        });
      });

      const tierInfo = (data.catalog?.tiers || {})[rec.recTier] || {};
      const modelsHtml = (tierInfo.candidates || [])
        .map((c) => `
          <li class="candidate-item">
            <div class="prov">${escapeHtml(c.provider)}</div>
            <div class="mod">${escapeHtml(c.model)}</div>
            <div style="color:var(--text-muted);margin-top:2px;">${escapeHtml(c.note)}</div>
          </li>
        `).join("");

      const skillChipsHtml = pkt.pipeline.length
        ? pkt.pipeline.map((p) => `<span class="badge skill-chip"><span class="phase">T${p.tier}:${escapeHtml(p.phase)}</span><span>${escapeHtml(p.name)}</span></span>`).join("")
        : `<span class="badge effort-low">Skills: none</span>`;

      const actionMeta = {
        keep_optimal: { label: "최적 모델·Effort 유지", cls: "effort-low" },
        raise_effort: { label: "모델 유지 → Effort 우선 상향", cls: "adjusted" },
        switch_model_up: { label: "모델 자체 변경 (티어 승격)", cls: "tier-high" },
        ground_before_think: { label: "내부 사고 대신 검색·리랭커 전환", cls: "tier-mid" }
      }[rec.decisionAction] || { label: rec.decisionAction, cls: "effort-low" };

      const policyInfo = (data.catalog?.adaptation_policies || {})[rec.policy] || {};
      const workloadInfo = (data.catalog?.workload_specialists || {})[rec.workload] || {};

      rootEl.querySelector("#sim-result").innerHTML = `
        <div class="rule-badges">
          <span class="badge tier-${rec.recTier}">${ico("cpu", "ico-sm")}<span>추천 모델: ${rec.recTier.toUpperCase()} (${escapeHtml(tierInfo.label || "")})</span></span>
          <span class="badge effort-${rec.recEffort}">Effort: ${rec.recEffort}</span>
          <span class="badge ${actionMeta.cls}">${escapeHtml(actionMeta.label)}</span>
          ${rec.effortAdjusted ? `<span class="badge adjusted">Effort 상향 (${escapeHtml(leaf.effort)} → ${rec.recEffort})</span>` : ""}
          ${rec.escalated ? `<span class="badge tier-high">모델 전환 (${escapeHtml(leaf.tier)} → ${rec.recTier})</span>` : ""}
        </div>

        <div class="calibration-note" style="margin-top:4px;">
          <strong>[정책: ${escapeHtml(policyInfo.label || rec.policy)}]</strong> ${escapeHtml(rec.actionReason)}
          ${workloadInfo.switch_note ? `<div style="margin-top:4px;color:var(--text);"><strong>프로바이더/특화 전환 기준:</strong> ${escapeHtml(workloadInfo.switch_note)}</div>` : ""}
        </div>

        <div class="rule-badges" style="margin-top:4px;">
          ${skillChipsHtml}
        </div>
        ${renderPillarBar(rec.pillars)}

        <div class="score-track-card">
          <div class="score-meta-row">
            <span>경로: <code>${chain.map((n) => escapeHtml(n.rule_id)).join(" → ")}</code></span>
            <strong>난이도 ${rec.score}/100</strong>
          </div>
          <div class="score-bar"><div class="score-fill tier-${rec.recTier}" style="width:${rec.score}%"></div></div>
          <div class="score-legend">
            <span>0–41 LOW (28+ Effort↑)</span>
            <span>42–74 MID (60+ Effort↑)</span>
            <span>75–100 HIGH</span>
          </div>
          <div style="font-size:0.78rem;color:var(--text-muted);">
            활성 패킷 <strong>~${pkt.pktTokens} tok</strong> (${pkt.pktBytes} B) / 전체 ${approxTokens(totalFileBytes)} tok → <strong style="color:var(--accent);">${pkt.savedPct}% 컨텍스트 절감</strong>
            (원본 AI 블록 합계 ${totalAiBytes} B)
          </div>
        </div>

        <div class="candidate-caption">참고용 모델 예시 (실제 호출은 사용자 도구·환경에 맞는 동급 모델 및 Effort 사용 · 환경에 따라 편차 가능)</div>
        <ul class="candidate-list">${modelsHtml}</ul>

        <div class="packet-wrap">
          <div class="packet-head">
            <span>&lt;active_rule_packet&gt; · AI Minimal Injection (${pkt.pktBytes} B)</span>
            <button class="btn xs primary" id="copy-sim-pkt" type="button">${ico("copy", "ico-sm")}<span>XML 복사</span></button>
          </div>
          <pre class="packet-box">${escapeHtml(pkt.xml)}</pre>
        </div>
      `;

      const copySimBtn = rootEl.querySelector("#copy-sim-pkt");
      copySimBtn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(pkt.xml);
          copySimBtn.innerHTML = `${ico("check", "ico-sm")}<span>복사됨</span>`;
          setTimeout(() => {
            copySimBtn.innerHTML = `${ico("copy", "ico-sm")}<span>XML 복사</span>`;
          }, 1500);
        } catch {
          alert(pkt.xml);
        }
      });
    }

    function updateCustomBuilder() {
      const id = rootEl.querySelector("#cb-id").value.trim() || "custom.task";
      const title = rootEl.querySelector("#cb-title").value.trim() || "Custom Rule";
      const tier = rootEl.querySelector("#cb-tier").value;
      const effort = rootEl.querySelector("#cb-effort").value;
      const skill = rootEl.querySelector("#cb-skill").value.trim();
      const parent = id.includes(".") ? id.split(".")[0] + ".root" : "root";
      const tpl = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>${title}</title>
  <link rel="stylesheet" href="../../assets/rule-ui.css">
</head>
<body>
<!-- AI-RULE-START -->
<main class="rule-node" data-rule-id="${id}" data-parent="${parent}" data-depth="2"
      data-title="${title}" data-tier="${tier}" data-effort="${effort}"
      data-skills="${skill}" data-keywords="${id},${title}" data-escalate-when="attempts>=2|coupled_files>=4">
  <header class="rule-head">
    <h1>${title}</h1>
    <p class="rule-summary">커스텀 작업 전용 규칙 노드입니다.</p>
  </header>
  <section class="rule-card" data-rules>
    <h2>적용 규칙</h2>
    <ul>
      <li>여기에 최소 실행 지침을 작성하세요.</li>
    </ul>
  </section>
</main>
<!-- AI-RULE-END -->
<script src="../../assets/rule-ui.js" defer></script>
</body>
</html>`;
      rootEl.querySelector("#cb-preview").textContent = tpl;
    }

    rootEl.querySelector("#task-input").addEventListener("input", (e) => {
      state.task = e.target.value;
      state.branchOverride = null;
      state.activePresetIdx = -1;
      update();
    });
    rootEl.querySelector("#tree-filter").addEventListener("input", (e) => {
      state.treeFilter = e.target.value;
      update();
    });
    rootEl.querySelector("#toggle-collapse-all").addEventListener("click", (e) => {
      const trunks = allList.filter((n) => n.depth === 1).map((n) => n.rule_id);
      if (state.collapsedIds.size > 0) {
        state.collapsedIds.clear();
        e.currentTarget.textContent = "활성 외 접기";
      } else {
        state.collapsedIds = new Set(trunks);
        e.currentTarget.textContent = "모두 펼치기";
      }
      update();
    });

    document.addEventListener("keydown", (ev) => {
      if ((ev.key === "/" || ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "k")) &&
          !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) {
        ev.preventDefault();
        rootEl.querySelector("#tree-filter")?.focus();
      }
    });

    rootEl.querySelector("#sig-files").addEventListener("change", (e) => { state.files = Number(e.target.value); update(); });
    rootEl.querySelector("#sig-attempts").addEventListener("change", (e) => { state.attempts = Number(e.target.value); update(); });
    rootEl.querySelector("#sig-conc").addEventListener("change", (e) => { state.concurrency = e.target.checked; update(); });
    rootEl.querySelector("#sig-sec").addEventListener("change", (e) => { state.security = e.target.checked; update(); });
    rootEl.querySelector("#sig-amb").addEventListener("change", (e) => { state.ambiguity = e.target.checked; update(); });
    rootEl.querySelector("#sig-verifier").addEventListener("change", (e) => { state.hasVerifier = e.target.checked; update(); });

    ["#cb-id", "#cb-title", "#cb-tier", "#cb-effort", "#cb-skill"].forEach((sel) => {
      rootEl.querySelector(sel).addEventListener("input", updateCustomBuilder);
      rootEl.querySelector(sel).addEventListener("change", updateCustomBuilder);
    });
    rootEl.querySelector("#cb-copy").addEventListener("click", async () => {
      const txt = rootEl.querySelector("#cb-preview").textContent;
      try { await navigator.clipboard.writeText(txt); } catch {}
    });

    update();
    updateCustomBuilder();
  }

  initTheme();
  document.addEventListener("DOMContentLoaded", () => {
    const branchMain = document.querySelector("main.rule-node[data-rule-id]");
    const explorerRoot = document.getElementById("explorer-app");
    if (explorerRoot) enhanceExplorer(explorerRoot);
    else if (branchMain) enhanceBranchNode(branchMain);
  });
})();
