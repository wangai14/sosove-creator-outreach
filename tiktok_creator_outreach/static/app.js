const state = {
  payload: null,
  selectedId: "",
  activeDraft: "dm",
  activeDetailTab: "profile",
  selectedIds: new Set(),
  pendingCsv: "",
  importPreview: null,
  modelDraft: null,
  replyAnalysis: null,
  filters: { search: "", status: "", tier: "", sort: "score_desc", workflow: "" },
  queue: { active: false, ids: [], index: 0, sent: 0, total: 0 },
};

const $ = (id) => document.getElementById(id);
const dom = {
  refreshBtn: $("refresh-btn"), csvInput: $("csv-input"), importPreviewPanel: $("import-preview-panel"),
  cancelImportBtn: $("cancel-import-btn"), confirmImportBtn: $("confirm-import-btn"), importPreviewSummary: $("import-preview-summary"), importPreviewList: $("import-preview-list"),
  statTotal: $("stat-total"), statReady: $("stat-ready"), statScore: $("stat-score"), statContacted: $("stat-contacted"), statBudget: $("stat-budget"),
  queueCaption: $("queue-caption"), queueCurrent: $("queue-current"), queueProgressFill: $("queue-progress-fill"), queueTargetInput: $("queue-target-input"),
  queueStartBtn: $("queue-start-btn"), queueOpenBtn: $("queue-open-btn"), queueCopyBtn: $("queue-copy-btn"), queueSentBtn: $("queue-sent-btn"), queueSkipBtn: $("queue-skip-btn"), queueStopBtn: $("queue-stop-btn"),
  searchForm: $("search-form"), keywordInput: $("keyword-input"), signalSelect: $("signal-select"), publicSearchKeyword: $("public-search-keyword"), publicSearchEngine: $("public-search-engine"), publicSearchLimit: $("public-search-limit"), publicSearchBtn: $("public-search-btn"), publicSearchOpenLink: $("public-search-open-link"), publicSearchStatus: $("public-search-status"),
  collectorNiche: $("collector-niche"), collectorSource: $("collector-source"), collectorImportBtn: $("collector-import-btn"), hashtagTopic: $("hashtag-topic"), hashtagInput: $("hashtag-input"), hashtagAutoBtn: $("hashtag-auto-btn"), hashtagSuggestions: $("hashtag-suggestions"), hashtagCount: $("hashtag-count"), copyTagsBtn: $("copy-tags-btn"), openTagsBtn: $("open-tags-btn"),
  filterSearch: $("filter-search"), filterStatus: $("filter-status"), filterTier: $("filter-tier"), filterSort: $("filter-sort"), clearFiltersBtn: $("clear-filters-btn"), deleteAllBtn: $("delete-all-btn"), candidateList: $("candidate-list"),
  batchToolbar: $("batch-toolbar"), batchSelectAll: $("batch-select-all"), batchCount: $("batch-count"), batchClearBtn: $("batch-clear-btn"), batchStatus: $("batch-status"), batchStatusBtn: $("batch-status-btn"), batchFollowup: $("batch-followup"), batchFollowupBtn: $("batch-followup-btn"), batchTags: $("batch-tags"), batchTagsBtn: $("batch-tags-btn"), batchDeleteBtn: $("batch-delete-btn"),
  detailTitle: $("detail-title"), detailEmpty: $("detail-empty"), detailContent: $("detail-content"), detailAvatar: $("detail-avatar"), detailName: $("detail-name"), detailUrl: $("detail-url"), detailPinBtn: $("detail-pin-btn"), deleteCandidateBtn: $("delete-candidate-btn"),
  nextActionBox: $("next-action-box"), nextActionTitle: $("next-action-title"), nextActionNote: $("next-action-note"), nextActionBtn: $("next-action-btn"), profileHealth: $("profile-health"), profileHealthPercent: $("profile-health-percent"), profileHealthTrack: $("profile-health-track"), profileHealthFill: $("profile-health-fill"), profileHealthMissing: $("profile-health-missing"),
  detailScore: $("detail-score"), detailTier: $("detail-tier"), detailViews: $("detail-views"), detailMedian: $("detail-median"), detailRatio: $("detail-ratio"), detailEr: $("detail-er"), scoreBreakdown: $("score-breakdown"),
  editFollowers: $("edit-followers"), editViews: $("edit-views"), editMedian: $("edit-median"), editEr: $("edit-er"), editFrequency: $("edit-frequency"), editAvatar: $("edit-avatar"), metricsSaveBtn: $("metrics-save-btn"),
  savedWorkForm: $("saved-work-form"), savedWorkUrl: $("saved-work-url"), savedWorkTitle: $("saved-work-title"), savedWorkNote: $("saved-work-note"), savedWorkAddBtn: $("saved-work-add-btn"), savedWorkCount: $("saved-work-count"), savedWorkList: $("saved-work-list"),
  detailStatus: $("detail-status"), followupDate: $("followup-date"), saveFollowupBtn: $("save-followup-btn"), contactNote: $("contact-note"), quickLogBtn: $("quick-log-btn"), contactHistory: $("contact-history"), manualChecklist: $("manual-checklist"),
  replySource: $("reply-source"), replyGenerateBtn: $("reply-generate-btn"), replyInsights: $("reply-insights"), replyDraft: $("reply-draft"), replyCopyBtn: $("reply-copy-btn"), replySaveBtn: $("reply-save-btn"), replyClearBtn: $("reply-clear-btn"),
  videoFormatSelect: $("video-format-select"), copyToneSelect: $("copy-tone-select"), copyAngleSelect: $("copy-angle-select"), copyDraftBtn: $("copy-draft-btn"), copyLocalBtn: $("copy-local-btn"), copyModelBtn: $("copy-model-btn"),
  copyModelProvider: $("copy-model-provider"), copyModelBaseUrl: $("copy-model-base-url"), copyModelName: $("copy-model-name"), copyModelApiKey: $("copy-model-api-key"), copyModelSaveBtn: $("copy-model-save-btn"), copyModelTestBtn: $("copy-model-test-btn"), copyModelClearBtn: $("copy-model-clear-btn"), copyModelStatus: $("copy-model-status"),
  emailSubjectRow: $("email-subject-row"), emailSubject: $("email-subject"), draftText: $("draft-text"),
  partnershipInvitation: $("partnership-invitation"), partnershipConnection: $("partnership-connection"), partnershipCreatorType: $("partnership-creator-type"), partnershipStage: $("partnership-stage"), partnershipQuote: $("partnership-quote"), partnershipProduct: $("partnership-product"), partnershipFormat: $("partnership-format"), partnershipUsageDays: $("partnership-usage-days"), partnershipSparkStatus: $("partnership-spark-status"), partnershipSparkCode: $("partnership-spark-code"), partnershipSampleStatus: $("partnership-sample-status"), partnershipSampleCost: $("partnership-sample-cost"), partnershipRecipient: $("partnership-recipient"), partnershipPostal: $("partnership-postal"), partnershipAddress: $("partnership-address"), partnershipPhone: $("partnership-phone"), partnershipOrder: $("partnership-order"), partnershipTracking: $("partnership-tracking"), partnershipShipped: $("partnership-shipped"), partnershipReceived: $("partnership-received"), partnershipProgress: $("partnership-progress"), partnershipScriptDue: $("partnership-script-due"), partnershipDraftDue: $("partnership-draft-due"), partnershipPostDate: $("partnership-post-date"), partnershipPostUrl: $("partnership-post-url"), partnershipCoupon: $("partnership-coupon"), partnershipOrders: $("partnership-orders"), partnershipRevenue: $("partnership-revenue"), partnershipSaveBtn: $("partnership-save-btn"), partnershipSummary: $("partnership-summary"),
  candidateForm: $("candidate-form"), sourceCaption: $("source-caption"), scrollTopBtn: $("scroll-top-btn"), toast: $("toast"),
};

const MODEL_KEY = "sosove.tiktokOutreach.copyModel.v1";
const DISCOVERY_KEY = "sosove.tiktokOutreach.discoveryPanels.v1";
let toastTimer;
let hashtagTimer;
let hashtagComposing = false;

const TIKTOK_HASHTAG_PRESETS = [
  { pattern: /fashion|ファッション|コーデ|服|女装|レディース|style|ootd|穿搭/i, tags: ["tiktokfashion", "japanesefashion", "ootdjapan", "tiktokコーデ", "大人女子コーデ"] },
  { pattern: /40代|アラフォー|中年|四十/i, tags: ["40代ファッション", "アラフォーコーデ", "40代コーデ", "大人カジュアル"] },
  { pattern: /30代|アラサー|三十/i, tags: ["30代ファッション", "アラサーコーデ", "30代コーデ", "大人女子コーデ"] },
  { pattern: /通勤|オフィス|仕事|职场|上班/i, tags: ["通勤コーデ", "オフィスカジュアル", "きれいめコーデ", "お仕事コーデ"] },
  { pattern: /低身長|小个子|小柄|150cm|155cm/i, tags: ["低身長コーデ", "低身長ファッション", "小柄コーデ", "スタイルアップコーデ"] },
  { pattern: /ワンピース|连衣裙|ドレス/i, tags: ["ワンピースコーデ", "大人ワンピース", "きれいめワンピース", "着回しコーデ"] },
  { pattern: /着痩せ|显瘦|体型|ぽっちゃり|プラスサイズ/i, tags: ["着痩せコーデ", "体型カバーコーデ", "ぽっちゃりコーデ", "細見えコーデ"] },
  { pattern: /春|spring|春装/i, tags: ["春コーデ", "春ファッション", "春服", "新作コーデ"] },
  { pattern: /夏|summer|夏装/i, tags: ["夏コーデ", "夏ファッション", "夏服", "涼しげコーデ"] },
  { pattern: /ママ|妈妈|主婦|育児|mama|mom/i, tags: ["ママコーデ", "ママファッション", "大人カジュアル", "着回しコーデ"] },
];
const TIKTOK_FALLBACK_HASHTAGS = ["tiktokfashion", "ootdjapan", "japanesefashion", "tokyofashion", "tiktokコーデ", "大人女子コーデ"];

function escapeHtml(value) { return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;"); }
function safeUrl(value) { const clean = String(value || "").trim(); return /^https?:\/\//i.test(clean) ? clean : ""; }
function isTikTokUrl(value) { try { const host = new URL(value).hostname.toLowerCase(); return ["tiktok.com", "tiktok.jp"].some((domain) => host === domain || host.endsWith(`.${domain}`)); } catch { return false; } }
function compactUrl(value) { try { const url = new URL(value); return `${url.hostname.replace(/^www\./, "")}${url.pathname}`; } catch { return value; } }
function formatNumber(value) { return new Intl.NumberFormat("ja-JP").format(Number(value || 0)); }
function formatCompact(value) { return new Intl.NumberFormat("ja-JP", { notation: "compact", maximumFractionDigits: 1 }).format(Number(value || 0)); }
function formatCurrency(value) { return new Intl.NumberFormat("ja-JP", { style: "currency", currency: "JPY", maximumFractionDigits: 0 }).format(Number(value || 0)); }
function initials(value) { return String(value || "TK").replace(/^@/, "").trim().slice(0, 2).toUpperCase() || "TK"; }
function localDate(days = 0) { const d = new Date(); d.setDate(d.getDate() + days); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; }
function parseLocalDate(value) { const match = String(value || "").slice(0, 10).match(/^(\d{4})-(\d{2})-(\d{2})$/); return match ? new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3])) : null; }
function daysUntil(value) { const target = parseLocalDate(value); const today = parseLocalDate(localDate()); return target && today ? Math.round((target - today) / 86400000) : null; }
function shortDate(value) { const clean = String(value || "").slice(0, 10); return /^\d{4}-\d{2}-\d{2}$/.test(clean) ? clean.slice(5).replace("-", "/") : clean; }
function relativeDate(value) { const days = daysUntil(value); if (days === null) return ""; if (days === 0) return "今天"; if (days === -1) return "昨天"; if (days < 0) return `${Math.abs(days)}天前`; if (days === 1) return "明天"; return shortDate(value); }
function latestContactDate(row) { return row.lastContacted || row.contactHistory?.[0]?.date || row.connectionAt || row.invitationSentAt || ""; }
function profileCompleteness(row) {
  const checks = [
    ["名称", Boolean(row.name && row.name !== row.handle), 10],
    ["赛道", Boolean(row.niche && row.niche !== "待判断"), 10],
    ["粉丝数", Number(row.followers) > 0, 15],
    ["平均播放", Number(row.avgViews) > 0, 15],
    ["中位播放", Number(row.medianViews) > 0, 10],
    ["互动率", Number(row.engagementRate) > 0, 10],
    ["更新频率", Number(row.videoFrequency) > 0, 10],
    ["邮箱", Boolean(row.email), 10],
    ["头像", Boolean(safeUrl(row.avatarUrl)), 5],
    ["参考作品", Boolean(row.savedWorks?.length), 5],
  ];
  const score = checks.reduce((total, [, ok, weight]) => total + (ok ? weight : 0), 0);
  return { score, missing: checks.filter(([, ok]) => !ok).map(([label]) => label), level: score >= 80 ? "good" : score >= 55 ? "medium" : "low" };
}
function candidateTiming(row) {
  const due = daysUntil(row.followUpDate); let primary = "尚未建联"; let tone = "neutral";
  if (due !== null) {
    if (due < 0) { primary = `超期 ${Math.abs(due)} 天`; tone = "overdue"; }
    else if (due === 0) { primary = "今天跟进"; tone = "today"; }
    else if (due === 1) { primary = "明天跟进"; tone = "upcoming"; }
    else { primary = `${shortDate(row.followUpDate)} 跟进`; tone = "upcoming"; }
  } else if (["contacted", "replied", "negotiating"].includes(row.status)) { primary = "未设置跟进"; tone = "warning"; }
  else if (["approved"].includes(row.status)) { primary = "合作推进中"; tone = "active"; }
  else if (row.status === "rejected") { primary = "已停止跟进"; tone = "quiet"; }
  const contacted = latestContactDate(row); const updated = String(row.updatedAt || "").slice(0, 10);
  const secondary = contacted ? `最近联系 ${relativeDate(contacted)}` : updated ? `更新 ${relativeDate(updated)}` : "暂无时间记录";
  return { primary, secondary, tone, due };
}
function nextActionFor(row) {
  const completeness = profileCompleteness(row); const timing = candidateTiming(row);
  if (row.status === "rejected") return { title: "无需继续跟进", note: "该达人已标记为不匹配", tone: "quiet", tab: "", focus: "", button: "" };
  const stageActions = {
    pricing: ["确认报价与合作方案", "核对报价、产品和素材使用范围", "partnership", ".partnership-box"],
    sample_pending: ["确认收货信息并安排寄样", row.shippingAddress ? "收货信息已记录，可以继续安排样品" : "还缺少完整收货地址", "partnership", ".partnership-box"],
    sample_sent: ["跟踪物流与签收", row.receivedAt ? "样品已签收，继续确认内容排期" : "检查物流单号和预计签收时间", "partnership", ".partnership-box"],
    content_scheduled: ["确认内容排期", "核对脚本、初稿和发布时间", "partnership", ".partnership-box"],
    draft_review: ["审核脚本或视频初稿", "记录审核结果和需要修改的内容", "partnership", ".partnership-box"],
    posted: ["记录发布表现", "补充视频链接、订单和收入数据", "partnership", ".partnership-box"],
    measured: ["完成合作复盘", "合作数据已进入复盘阶段", "partnership", ".partnership-box"],
  };
  const stageAction = stageActions[row.partnershipStage];
  if (stageAction) return { title: stageAction[0], note: stageAction[1], tone: row.partnershipStage === "measured" ? "success" : "active", tab: stageAction[2], focus: stageAction[3], button: "打开合作" };
  if (row.status === "approved") return { title: "建立合作追踪", note: "确认报价、合作产品和交付节点", tone: "success", tab: "partnership", focus: ".partnership-box", button: "打开合作" };
  if (row.status === "negotiating") return { title: "推进报价确认", note: "记录报价和双方确认的合作条件", tone: "warning", tab: "partnership", focus: ".partnership-box", button: "处理报价" };
  if (row.status === "replied") return { title: "处理达人回复", note: "生成回复建议并更新当前状态", tone: "active", tab: "outreach", focus: ".reply-assistant-box", button: "处理回复" };
  if (row.status === "contacted") {
    const urgent = timing.due !== null && timing.due <= 0;
    return { title: urgent ? "今天跟进达人" : "等待回复并按计划跟进", note: timing.due === null ? "尚未设置下次跟进日期" : `${shortDate(row.followUpDate)} 跟进`, tone: urgent ? "danger" : "warning", tab: "outreach", focus: ".contact-log-box", button: "打开建联" };
  }
  if (row.status === "ready") return { title: "发送首轮 TikTok DM", note: "打开主页复核后使用个性化建联文案", tone: "active", tab: "outreach", focus: ".template-library", button: "打开建联" };
  if (completeness.score < 70) return { title: "先补全关键资料", note: `优先补充：${completeness.missing.slice(0, 3).join("、")}`, tone: "warning", tab: "profile", focus: ".enrichment-box", button: "补全资料" };
  return { title: "审核达人并确认可建联", note: "资料基本齐全，可以完成最后审核", tone: "neutral", tab: "profile", focus: ".score-breakdown", button: "查看资料" };
}
function mergeTags(value) { return String(value || "").split(/[,;、|\n]+/).map((item) => item.trim()).filter(Boolean).slice(0, 10); }
function appendNote(existing, next) { return [...new Set([String(existing || "").trim(), String(next || "").trim()].filter(Boolean))].join("\n"); }
function showToast(message) { clearTimeout(toastTimer); dom.toast.textContent = message; dom.toast.classList.add("is-visible"); toastTimer = setTimeout(() => dom.toast.classList.remove("is-visible"), 2500); }
function mergeUnique(...lists) { const seen = new Set(); return lists.flat().filter((item) => { const clean = String(item || "").trim(); const key = clean.toLowerCase(); if (!clean || seen.has(key)) return false; seen.add(key); return true; }); }
function cleanHashtag(value) { return String(value || "").trim().replace(/^#+/, "").replace(/https?:\/\/\S+/gi, "").replace(/[@#＃]/g, "").replace(/[^\p{L}\p{N}_ー]+/gu, "").slice(0, 42); }
function hashtagsFromText(value) { const source = String(value || ""); const direct = Array.from(source.matchAll(/#([\p{L}\p{N}_ー-]{2,42})/gu)).map((match) => match[1]); const chunks = source.replace(/[()"']/g, " ").split(/[\r\n,，、;；|]+/).map((chunk) => chunk.trim()).filter(Boolean); const phrases = chunks.flatMap((chunk) => [chunk, ...chunk.split(/\s+/).filter((part) => part.length > 1)]); return mergeUnique(direct, phrases).map(cleanHashtag).filter((tag) => tag.length >= 2); }
function parseHashtagInput() { return hashtagsFromText(dom.hashtagInput.value); }
function formatHashtags(tags) { return tags.map(cleanHashtag).filter(Boolean).slice(0, 12).map((tag) => `#${tag}`).join("\n"); }
function buildHashtagSuggestions() { const row = selectedCandidate(); const source = [dom.hashtagTopic.value, dom.collectorNiche.value, row?.niche || "", ...(row?.tags || [])].join("\n"); const presetTags = TIKTOK_HASHTAG_PRESETS.filter((preset) => preset.pattern.test(source)).flatMap((preset) => preset.tags); return mergeUnique(hashtagsFromText(dom.hashtagTopic.value), presetTags, TIKTOK_FALLBACK_HASHTAGS).map(cleanHashtag).filter(Boolean).slice(0, 18); }
function renderHashtagSuggestions(tags = buildHashtagSuggestions()) { const selected = new Set(parseHashtagInput().map((tag) => tag.toLowerCase())); dom.hashtagSuggestions.innerHTML = tags.slice(0, 14).map((tag) => { const clean = cleanHashtag(tag); const active = selected.has(clean.toLowerCase()) ? " is-active" : ""; return `<button class="hashtag-chip${active}" type="button" data-tag="${escapeHtml(clean)}">#${escapeHtml(clean)}</button>`; }).join(""); dom.hashtagCount.textContent = `${parseHashtagInput().length} 个`; }
function fillHashtagInput() { const tags = buildHashtagSuggestions(); dom.hashtagInput.value = formatHashtags(tags); renderHashtagSuggestions(tags); return tags; }
function toggleHashtag(tag) { const clean = cleanHashtag(tag); const tags = parseHashtagInput(); const exists = tags.some((item) => item.toLowerCase() === clean.toLowerCase()); dom.hashtagInput.value = formatHashtags(exists ? tags.filter((item) => item.toLowerCase() !== clean.toLowerCase()) : [clean, ...tags]); renderHashtagSuggestions(); }
function openHashtagPages(tags) { const cleanTags = tags.map(cleanHashtag).filter(Boolean).slice(0, 4); if (!cleanTags.length) return showToast("没有可打开的 Hashtag"); cleanTags.forEach((tag, index) => setTimeout(() => window.open(`https://www.tiktok.com/tag/${encodeURIComponent(tag)}`, "_blank", "noopener"), index * 180)); }

async function apiJson(path, options = {}) {
  const response = await fetch(`/tiktok/api${path}`, { cache: "no-store", headers: { "Content-Type": "application/json", ...(options.headers || {}) }, ...options });
  let payload = {}; try { payload = await response.json(); } catch { payload = {}; }
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}

async function copyText(value, message) {
  try { await navigator.clipboard.writeText(value); showToast(message); }
  catch { showToast("浏览器阻止复制，请手动选择文案"); }
}

async function loadWorkspace({ silent = false } = {}) {
  try {
    state.payload = await apiJson("/workspace");
    const availableIds = new Set(state.payload.candidates.map((row) => row.id));
    state.selectedIds = new Set([...state.selectedIds].filter((id) => availableIds.has(id)));
    if (!state.selectedId && state.payload.candidates.length) state.selectedId = state.payload.candidates[0].id;
    if (state.selectedId && !state.payload.candidates.some((row) => row.id === state.selectedId)) state.selectedId = state.payload.candidates[0]?.id || "";
    render();
    if (!silent) showToast("TikTok 候选池已刷新");
  } catch (error) { showToast(`加载失败：${error.message}`); }
}

function selectedCandidate() { return state.payload?.candidates.find((row) => row.id === state.selectedId) || null; }
function workflowIds() { return state.filters.workflow ? new Set(state.payload?.tasks?.[state.filters.workflow] || []) : null; }
function filteredCandidates() {
  const search = state.filters.search.toLowerCase(); const ids = workflowIds();
  const rows = (state.payload?.candidates || []).filter((row) => {
    if (ids && !ids.has(row.id)) return false;
    if (state.filters.status && row.status !== state.filters.status) return false;
    if (state.filters.tier && row.tier !== state.filters.tier) return false;
    return !search || [row.handle, row.name, row.niche, row.location, ...(row.tags || [])].join(" ").toLowerCase().includes(search);
  });
  const sorters = {
    score_desc: (a, b) => b.score - a.score, views_desc: (a, b) => b.avgViews - a.avgViews,
    median_desc: (a, b) => b.medianViews - a.medianViews, ratio_desc: (a, b) => b.viewFollowerRatio - a.viewFollowerRatio,
    engagement_desc: (a, b) => b.engagementRate - a.engagementRate, followers_desc: (a, b) => b.followers - a.followers,
    updated_desc: (a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)),
  };
  rows.sort((a, b) => Number(b.pinned) - Number(a.pinned) || (sorters[state.filters.sort] || sorters.score_desc)(a, b));
  return rows;
}

function render() {
  if (!state.payload) return;
  renderStats(); renderImportPreview(); renderStatusOptions(); renderTaskBoard(); renderQueue(); renderPublicSearchLink(); renderCandidates(); renderDetail();
  dom.sourceCaption.textContent = `TikTok 数据：${state.payload.source.candidatePath}`;
}

function renderStats() {
  const s = state.payload.stats; dom.statTotal.textContent = formatNumber(s.total); dom.statReady.textContent = formatNumber(s.ready); dom.statScore.textContent = s.avgScore; dom.statContacted.textContent = formatNumber(s.contacted); dom.statBudget.textContent = formatCurrency(s.estimatedCostJpy);
}

function renderImportPreview() {
  dom.importPreviewPanel.hidden = !state.importPreview;
  if (!state.importPreview) return;
  const s = state.importPreview.summary;
  dom.importPreviewSummary.innerHTML = [["新增", s.add], ["更新", s.update], ["重复", s.duplicate], ["跳过", s.skip]].map(([label, value]) => `<span class="mini-pill">${label} · ${value || 0}</span>`).join("");
  dom.importPreviewList.innerHTML = state.importPreview.rows.map((item) => `<article class="preview-row"><strong>#${item.row} @${escapeHtml(item.candidate.handle || "-")}</strong><span>${escapeHtml(item.action)} · ${escapeHtml(item.candidate.niche)}</span></article>`).join("");
}

function renderStatusOptions() {
  const all = `<option value="">全部</option>` + Object.entries(state.payload.statusLabels).map(([key, label]) => `<option value="${key}">${escapeHtml(label)}</option>`).join("");
  dom.filterStatus.innerHTML = all; dom.filterStatus.value = state.filters.status;
  dom.batchStatus.innerHTML = `<option value="">批量状态</option>` + Object.entries(state.payload.statusLabels).map(([key, label]) => `<option value="${key}">${escapeHtml(label)}</option>`).join("");
  dom.detailStatus.innerHTML = Object.entries(state.payload.statusLabels).map(([key, label]) => `<option value="${key}">${escapeHtml(label)}</option>`).join("");
  dom.partnershipStage.innerHTML = Object.entries(state.payload.partnershipStages).map(([key, label]) => `<option value="${key}">${escapeHtml(label)}</option>`).join("");
  dom.partnershipProgress.innerHTML = Object.entries(state.payload.videoProgressLabels).map(([key, label]) => `<option value="${key}">${escapeHtml(label)}</option>`).join("");
}

function taskRows(key) { const ids = new Set(state.payload.tasks?.[key] || []); return state.payload.candidates.filter((row) => ids.has(row.id)); }
function renderTaskBoard() {
  document.querySelectorAll("[data-workflow]").forEach((button) => {
    const key = button.dataset.workflow; const rows = taskRows(key); button.classList.toggle("is-active", state.filters.workflow === key);
    const handles = rows.map((row) => `@${row.handle}`);
    const preview = handles.slice(0, 5).join(" / ");
    const more = rows.length > 5 ? ` / +${rows.length - 5}` : "";
    const list = $(`task-${key}-list`);
    $(`task-${key}`).textContent = rows.length;
    list.textContent = rows.length ? `${preview}${more}` : "暂无";
    list.title = handles.join(" / ");
  });
}

function queueRows() { return filteredCandidates().filter((row) => !["contacted", "replied", "negotiating", "approved", "rejected"].includes(row.status)); }
function currentQueueRow() { const id = state.queue.ids[state.queue.index]; return state.payload?.candidates.find((row) => row.id === id) || null; }
function renderQueue() {
  const available = queueRows(); const current = currentQueueRow(); const target = Math.max(1, Number(dom.queueTargetInput.value || 20));
  dom.queueCaption.textContent = state.queue.active ? `今日已记录 ${state.queue.sent}/${target}` : `当前筛选下有 ${available.length} 个可进入队列的候选`;
  dom.queueCurrent.textContent = current ? `${state.queue.index + 1}/${state.queue.total} · @${current.handle}` : state.queue.active ? "队列已完成" : "未开始";
  dom.queueProgressFill.style.width = `${state.queue.total ? Math.min(100, (state.queue.index / state.queue.total) * 100) : 0}%`;
  const hasCurrent = Boolean(current); dom.queueOpenBtn.disabled = !hasCurrent; dom.queueCopyBtn.disabled = !hasCurrent; dom.queueSentBtn.disabled = !hasCurrent; dom.queueSkipBtn.disabled = !hasCurrent; dom.queueStopBtn.disabled = !state.queue.active; dom.queueStartBtn.disabled = state.queue.active || !available.length;
}

function startQueue() { const rows = queueRows(); state.queue = { active: true, ids: rows.map((row) => row.id), index: 0, sent: 0, total: rows.length }; if (rows.length) state.selectedId = rows[0].id; renderCandidates(); renderDetail(); renderQueue(); }
function stopQueue() { state.queue = { active: false, ids: [], index: 0, sent: 0, total: 0 }; renderQueue(); }
function advanceQueue(sent = false) { if (sent) state.queue.sent += 1; state.queue.index += 1; const next = currentQueueRow(); if (next) state.selectedId = next.id; else state.queue.active = false; renderCandidates(); renderDetail(); renderQueue(); }

function avatarHtml(row, className = "candidate-avatar") { const url = safeUrl(row.avatarUrl); const label = escapeHtml(initials(row.name || row.handle)); return `<div class="${className} ${url ? "has-image" : "is-fallback"}"><span>${label}</span>${url ? `<img src="${escapeHtml(url)}" alt="${escapeHtml(row.name || row.handle)}" loading="lazy" referrerpolicy="no-referrer" onerror="this.hidden=true">` : ""}</div>`; }
function partnershipChips(row) { const chips = []; if (row.partnershipStage !== "none") chips.push(state.payload.partnershipStages[row.partnershipStage]); if (row.sparkAdsStatus === "approved") chips.push("Spark 已授权"); if (row.videoProgress !== "not_started") chips.push(state.payload.videoProgressLabels[row.videoProgress]); if (row.orders) chips.push(`${row.orders} orders`); return chips.filter(Boolean); }
function renderCandidateCard(row) {
  const active = row.id === state.selectedId ? "is-active" : ""; const label = state.payload.statusLabels[row.status] || row.status;
  const profileLine = [row.name, row.niche, row.location].filter(Boolean).join(" · "); const completeness = profileCompleteness(row); const timing = candidateTiming(row);
  return `<article class="candidate-card ${active}" data-platform="tiktok" data-id="${escapeHtml(row.id)}" data-status="${escapeHtml(row.status)}" data-tier="${escapeHtml(row.tier)}" data-pinned="${row.pinned ? "true" : "false"}">
    <div class="candidate-top"><label class="candidate-select" title="选择 @${escapeHtml(row.handle)}"><input data-batch-select="${escapeHtml(row.id)}" type="checkbox" aria-label="选择 @${escapeHtml(row.handle)}" ${state.selectedIds.has(row.id) ? "checked" : ""}></label><div class="candidate-identity">${avatarHtml(row)}<div class="candidate-main"><h3 title="@${escapeHtml(row.handle)}">@${escapeHtml(row.handle)}</h3><p title="${escapeHtml(profileLine)}">${escapeHtml(profileLine)}</p></div></div><div class="score-badge" data-tier="${row.tier}">${row.score}<small>${row.tier}</small></div></div>
    <div class="candidate-meta tk-performance"><span class="mini-pill">${formatCompact(row.avgViews)} avg views</span><span class="mini-pill">${formatCompact(row.medianViews)} median</span><span class="mini-pill">${Number(row.viewFollowerRatio || 0).toFixed(2)}x V/F</span><span class="mini-pill">${Number(row.engagementRate || 0).toFixed(1)}% ER</span><span class="mini-pill">${escapeHtml(label)}</span>${row.savedWorks?.length ? `<span class="mini-pill">作品 ${row.savedWorks.length}</span>` : ""}${row.featuredWorkId ? '<span class="mini-pill mini-pill--reference">文案参考</span>' : ""}${row.pinned ? '<span class="mini-pill mini-pill--pinned">已置顶</span>' : ""}${partnershipChips(row).map((chip) => `<span class="mini-pill">${escapeHtml(chip)}</span>`).join("")}</div>
    <div class="candidate-ops-line"><span class="candidate-timing" data-tone="${timing.tone}">${escapeHtml(timing.primary)}</span><span>${escapeHtml(timing.secondary)}</span><span class="completion-chip" data-level="${completeness.level}">资料 ${completeness.score}%</span></div>
    <div class="candidate-actions"><button data-action="select" data-id="${row.id}" type="button">查看</button><button data-action="pin" data-id="${row.id}" class="pin-button ${row.pinned ? "is-pinned" : ""}" type="button">${row.pinned ? "取消置顶" : "置顶"}</button><a href="${escapeHtml(row.tiktokUrl)}" target="_blank" rel="noreferrer">TK</a><button data-action="copy" data-id="${row.id}" type="button">复制 DM</button><button data-action="delete" data-id="${row.id}" class="danger-text" type="button">删除</button></div>
  </article>`;
}
function renderBatchToolbar() { const rows = filteredCandidates(); const visibleSelected = rows.filter((row) => state.selectedIds.has(row.id)).length; const count = state.selectedIds.size; dom.batchCount.textContent = `已选择 ${count}`; dom.batchSelectAll.checked = Boolean(rows.length) && visibleSelected === rows.length; dom.batchSelectAll.indeterminate = visibleSelected > 0 && visibleSelected < rows.length; [dom.batchStatusBtn, dom.batchFollowupBtn, dom.batchTagsBtn, dom.batchDeleteBtn, dom.batchClearBtn].forEach((button) => { button.disabled = !count; }); dom.batchToolbar.classList.toggle("has-selection", Boolean(count)); }
function renderCandidates() { const rows = filteredCandidates(); dom.candidateList.innerHTML = rows.length ? rows.map(renderCandidateCard).join("") : '<div class="empty-state"><strong>没有符合条件的 TikTok 候选</strong><span>调整筛选或导入 CSV。</span></div>'; renderBatchToolbar(); }

function renderDetailAvatar(row) { const replacement = document.createElement("div"); replacement.innerHTML = avatarHtml(row, "avatar"); const next = replacement.firstElementChild; next.id = "detail-avatar"; dom.detailAvatar.replaceWith(next); dom.detailAvatar = next; }
function renderScoreBreakdown(row) { dom.scoreBreakdown.innerHTML = (row.scoreBreakdownItems || []).map((item) => `<div class="score-row"><span>${escapeHtml(item.label)}</span><div class="score-track"><i class="score-fill" style="--pct:${Number(item.pct || 0)}%"></i></div><strong>${item.value}/${item.max}</strong></div>`).join(""); }
function renderContactHistory(row) { dom.contactHistory.innerHTML = row.contactHistory?.length ? row.contactHistory.map((item) => `<article class="history-item"><strong>${escapeHtml(item.type)} · ${escapeHtml(item.date)}</strong><span>${escapeHtml(item.note || "-")}</span><small>${item.followUpDate ? `下次跟进：${escapeHtml(item.followUpDate)}` : ""}</small></article>`).join("") : '<div class="history-item"><span>暂无联系记录</span></div>'; }
function renderReply() { const a = state.replyAnalysis; dom.replyInsights.innerHTML = a ? `<span class="mini-pill">${escapeHtml(a.label)}</span><span class="mini-pill">建议状态 · ${escapeHtml(state.payload.statusLabels[a.status] || a.status)}</span>` : ""; dom.replyDraft.textContent = a?.draft || ""; dom.replyCopyBtn.disabled = !a; dom.replySaveBtn.disabled = !a; }
function renderSavedWorks(row) {
  const works = row.savedWorks || [];
  dom.savedWorkCount.textContent = `${works.length} 个`;
  dom.savedWorkList.innerHTML = works.length ? works.map((item) => {
    const url = safeUrl(item.url); const title = item.title || "TikTok 作品"; const featured = item.id === row.featuredWorkId;
    return `<article class="saved-work-item ${featured ? "is-featured" : ""}"><div class="saved-work-main"><div class="saved-work-title-row"><a href="${escapeHtml(url)}" target="_blank" rel="noreferrer" title="${escapeHtml(item.url)}">${escapeHtml(title)}</a>${featured ? '<span class="reference-badge">文案参考</span>' : ""}</div><span>${escapeHtml(compactUrl(item.url))}</span>${item.note ? `<p>${escapeHtml(item.note)}</p>` : ""}</div><div class="saved-work-actions"><small>${escapeHtml(String(item.createdAt || "").slice(0, 10))}</small><button type="button" data-saved-work-feature="${escapeHtml(item.id)}">${featured ? "取消参考" : "设为参考"}</button><button type="button" class="danger-text" data-saved-work-delete="${escapeHtml(item.id)}" title="删除这条收藏">删除</button></div></article>`;
  }).join("") : '<div class="saved-work-empty">还没有收藏作品</div>';
}

function renderDetailTabs() { document.querySelectorAll("[data-detail-tab]").forEach((button) => { const active = button.dataset.detailTab === state.activeDetailTab; button.classList.toggle("is-active", active); button.setAttribute("aria-selected", String(active)); }); document.querySelectorAll("[data-detail-panel]").forEach((panel) => { panel.hidden = panel.dataset.detailPanel !== state.activeDetailTab; }); }

function renderPartnership(row) {
  dom.partnershipInvitation.value = row.invitationSentAt || ""; dom.partnershipConnection.value = row.connectionAt || ""; dom.partnershipCreatorType.value = row.creatorType || ""; dom.partnershipStage.value = row.partnershipStage || "none"; dom.partnershipQuote.value = row.quoteJpy || ""; dom.partnershipProduct.value = row.collabProduct || ""; dom.partnershipFormat.value = row.videoFormat || "short_video"; dom.partnershipUsageDays.value = row.usageRightsDays || ""; dom.partnershipSparkStatus.value = row.sparkAdsStatus || "not_requested"; dom.partnershipSparkCode.value = row.sparkAuthorizationCode || ""; dom.partnershipSampleStatus.value = row.sampleStatus || "none"; dom.partnershipSampleCost.value = row.sampleCostJpy || ""; dom.partnershipRecipient.value = row.recipientName || ""; dom.partnershipPostal.value = row.postalCode || ""; dom.partnershipAddress.value = row.shippingAddress || ""; dom.partnershipPhone.value = row.phoneNumber || ""; dom.partnershipOrder.value = row.orderNumber || ""; dom.partnershipTracking.value = row.shippingTracking || ""; dom.partnershipShipped.value = row.shippedAt || ""; dom.partnershipReceived.value = row.receivedAt || ""; dom.partnershipProgress.value = row.videoProgress || "not_started"; dom.partnershipScriptDue.value = row.scriptDueDate || ""; dom.partnershipDraftDue.value = row.draftDueDate || ""; dom.partnershipPostDate.value = row.postDate || ""; dom.partnershipPostUrl.value = row.postUrl || ""; dom.partnershipCoupon.value = row.couponCode || ""; dom.partnershipOrders.value = row.orders || ""; dom.partnershipRevenue.value = row.revenueJpy || "";
  const cost = Number(row.quoteJpy || 0) + Number(row.sampleCostJpy || 0); const roi = cost ? ((Number(row.revenueJpy || 0) - cost) / cost) * 100 : null;
  dom.partnershipSummary.innerHTML = [["阶段", state.payload.partnershipStages[row.partnershipStage]], ["Spark", row.sparkAdsStatus], ["视频", state.payload.videoProgressLabels[row.videoProgress]], ["成本", formatCurrency(cost)], ["收入", formatCurrency(row.revenueJpy)], ["ROI", roi === null ? "-" : `${roi.toFixed(1)}%`]].map(([label, value]) => `<span class="mini-pill">${escapeHtml(label)} · ${escapeHtml(value || "-")}</span>`).join("");
}

function renderDraft(row) { const useModel = state.modelDraft?.candidateId === row.id && state.modelDraft?.mode === state.activeDraft; const text = useModel ? state.modelDraft.text : row.drafts?.[state.activeDraft] || ""; dom.draftText.textContent = text; dom.emailSubjectRow.hidden = state.activeDraft !== "email"; dom.emailSubject.textContent = useModel ? state.modelDraft.subject || row.drafts.emailSubject : row.drafts?.emailSubject || "-"; document.querySelectorAll("[data-draft]").forEach((button) => button.classList.toggle("is-active", button.dataset.draft === state.activeDraft)); }

function renderActionBrief(row) {
  const completeness = profileCompleteness(row); const action = nextActionFor(row); const missing = completeness.missing;
  dom.nextActionBox.dataset.tone = action.tone; dom.nextActionTitle.textContent = action.title; dom.nextActionNote.textContent = action.note;
  dom.nextActionBtn.hidden = !action.button; dom.nextActionBtn.textContent = action.button || ""; dom.nextActionBtn.dataset.tab = action.tab || ""; dom.nextActionBtn.dataset.focus = action.focus || "";
  dom.profileHealth.dataset.level = completeness.level; dom.profileHealthPercent.textContent = `${completeness.score}%`; dom.profileHealthFill.style.width = `${completeness.score}%`; dom.profileHealthTrack.setAttribute("aria-valuenow", String(completeness.score));
  dom.profileHealthMissing.textContent = missing.length ? `待补：${missing.slice(0, 3).join("、")}${missing.length > 3 ? ` 等 ${missing.length} 项` : ""}` : "关键资料已齐全";
}

function renderDetail() {
  const row = selectedCandidate(); if (!row) { dom.detailTitle.textContent = "选择一个达人"; dom.detailEmpty.hidden = false; dom.detailContent.hidden = true; return; }
  const detailName = [row.name || row.handle, row.niche].filter(Boolean).join(" · ");
  dom.detailEmpty.hidden = true; dom.detailContent.hidden = false; dom.detailTitle.textContent = `@${row.handle}`; dom.detailTitle.title = `@${row.handle}`; renderDetailAvatar(row); dom.detailName.textContent = detailName; dom.detailName.title = detailName; dom.detailUrl.href = row.tiktokUrl; dom.detailUrl.textContent = row.tiktokUrl.replace("https://www.", ""); dom.detailUrl.title = row.tiktokUrl; dom.detailPinBtn.textContent = row.pinned ? "取消置顶" : "置顶"; renderActionBrief(row);
  dom.detailScore.textContent = row.score; dom.detailTier.textContent = row.tier; dom.detailViews.textContent = formatCompact(row.avgViews); dom.detailMedian.textContent = formatCompact(row.medianViews); dom.detailRatio.textContent = `${Number(row.viewFollowerRatio || 0).toFixed(2)}x`; dom.detailEr.textContent = `${Number(row.engagementRate || 0).toFixed(1)}%`; renderScoreBreakdown(row);
  dom.editFollowers.value = row.followers || ""; dom.editViews.value = row.avgViews || ""; dom.editMedian.value = row.medianViews || ""; dom.editEr.value = row.engagementRate || ""; dom.editFrequency.value = row.videoFrequency || ""; dom.editAvatar.value = row.avatarUrl || ""; dom.detailStatus.value = row.status; dom.followupDate.value = row.followUpDate || ""; renderSavedWorks(row); renderContactHistory(row); renderReply();
  dom.manualChecklist.innerHTML = (row.manualChecklist || []).map((item) => `<label class="check-item"><input type="checkbox"><span>${escapeHtml(item.label)}</span></label>`).join(""); renderDraft(row); renderPartnership(row); renderDetailTabs();
}

function renderPublicSearchLink() { const q = `site:tiktok.com/@ "${dom.publicSearchKeyword.value.split(/\r?\n/).filter(Boolean).join('" OR "')}"`; dom.publicSearchOpenLink.href = `https://www.google.com/search?q=${encodeURIComponent(q)}`; }
function setDiscoveryToolOpen(tool, open) { const toggle = tool.querySelector(".discovery-toggle"); const body = tool.querySelector(".discovery-tool-body"); tool.classList.toggle("is-open", open); toggle?.setAttribute("aria-expanded", String(open)); if (body) body.hidden = !open; }
function saveDiscoveryTools() { try { const openIds = [...document.querySelectorAll(".discovery-tool.is-open")].map((tool) => tool.id); localStorage.setItem(DISCOVERY_KEY, JSON.stringify(openIds)); } catch { /* ignore storage limits */ } }
function initDiscoveryTools() {
  const tools = [...document.querySelectorAll(".discovery-tool")];
  try { const saved = JSON.parse(localStorage.getItem(DISCOVERY_KEY) || "null"); if (Array.isArray(saved)) tools.forEach((tool) => setDiscoveryToolOpen(tool, saved.includes(tool.id))); } catch { /* keep HTML defaults */ }
}
function loadModelConfig() { try { const saved = JSON.parse(localStorage.getItem(MODEL_KEY) || "{}"); dom.copyModelProvider.value = saved.provider || "local"; dom.copyModelBaseUrl.value = saved.baseUrl || ""; dom.copyModelName.value = saved.model || ""; dom.copyModelStatus.textContent = saved.provider && saved.provider !== "local" ? `已保存 ${saved.model || "模型"} 配置` : "默认使用 TikTok 本地模板"; } catch { /* ignore */ } }
function modelPayload() { return { provider: dom.copyModelProvider.value, apiBaseUrl: dom.copyModelBaseUrl.value.trim(), model: dom.copyModelName.value.trim(), apiKey: dom.copyModelApiKey.value.trim(), authMode: "bearer" }; }

async function saveCandidate(payload, message) { const result = await apiJson("/candidates", { method: "POST", body: JSON.stringify(payload) }); if (!result.ok) throw new Error(result.error || "保存失败"); state.selectedId = result.candidate.id; await loadWorkspace({ silent: true }); showToast(message); }
async function togglePin(row) { const result = await apiJson("/candidates/pin", { method: "POST", body: JSON.stringify({ id: row.id, pinned: !row.pinned }) }); if (!result.ok) throw new Error("置顶失败"); await loadWorkspace({ silent: true }); showToast(row.pinned ? "已取消置顶" : "已置顶达人"); }
async function deleteCandidate(row) { if (!row || !confirm(`确认删除 @${row.handle}？`)) return; const result = await apiJson("/candidates/delete", { method: "POST", body: JSON.stringify({ id: row.id }) }); if (!result.ok) throw new Error(result.error || "删除失败"); state.selectedIds.delete(row.id); state.selectedId = ""; await loadWorkspace({ silent: true }); showToast("已删除 TikTok 达人"); }
async function runBatchAction(action, value = "", confirmToken = "") { if (!state.selectedIds.size) return showToast("请先选择达人"); const result = await apiJson("/candidates/batch", { method: "POST", body: JSON.stringify({ ids: [...state.selectedIds], action, value, confirm: confirmToken }) }); if (!result.ok) throw new Error(result.error || "批量操作失败"); const count = result.updated || 0; if (action === "delete") { state.selectedIds.clear(); state.selectedId = ""; } await loadWorkspace({ silent: true }); showToast(action === "delete" ? `已删除 ${count} 个达人` : `已更新 ${count} 个达人`); }

dom.refreshBtn.addEventListener("click", () => loadWorkspace());
dom.filterSearch.addEventListener("input", (e) => { state.filters.search = e.target.value.trim(); renderCandidates(); renderQueue(); });
dom.filterStatus.addEventListener("change", (e) => { state.filters.status = e.target.value; renderCandidates(); renderQueue(); });
dom.filterTier.addEventListener("change", (e) => { state.filters.tier = e.target.value; renderCandidates(); renderQueue(); });
dom.filterSort.addEventListener("change", (e) => { state.filters.sort = e.target.value; renderCandidates(); renderQueue(); });
dom.clearFiltersBtn.addEventListener("click", () => { state.filters = { search: "", status: "", tier: "", sort: "score_desc", workflow: "" }; dom.filterSearch.value = ""; dom.filterStatus.value = ""; dom.filterTier.value = ""; dom.filterSort.value = "score_desc"; renderTaskBoard(); renderCandidates(); renderQueue(); });
document.querySelectorAll("[data-workflow]").forEach((button) => button.addEventListener("click", () => { state.filters.workflow = state.filters.workflow === button.dataset.workflow ? "" : button.dataset.workflow; const rows = filteredCandidates(); if (rows.length) state.selectedId = rows[0].id; renderTaskBoard(); renderCandidates(); renderDetail(); renderQueue(); }));
document.querySelectorAll("[data-detail-tab]").forEach((button) => button.addEventListener("click", () => { state.activeDetailTab = button.dataset.detailTab; renderDetailTabs(); }));
document.addEventListener("click", (event) => { const toggle = event.target.closest(".discovery-toggle"); const tool = toggle?.closest(".discovery-tool"); if (!tool) return; setDiscoveryToolOpen(tool, !tool.classList.contains("is-open")); saveDiscoveryTools(); });
dom.nextActionBtn.addEventListener("click", () => { const tab = dom.nextActionBtn.dataset.tab; const focus = dom.nextActionBtn.dataset.focus; if (!tab) return; state.activeDetailTab = tab; renderDetailTabs(); requestAnimationFrame(() => { const target = focus ? document.querySelector(focus) : null; target?.scrollIntoView({ behavior: "smooth", block: "start" }); }); });

dom.batchSelectAll.addEventListener("change", () => { filteredCandidates().forEach((row) => { if (dom.batchSelectAll.checked) state.selectedIds.add(row.id); else state.selectedIds.delete(row.id); }); renderCandidates(); });
dom.batchClearBtn.addEventListener("click", () => { state.selectedIds.clear(); renderCandidates(); });
dom.batchStatusBtn.addEventListener("click", async () => { if (!dom.batchStatus.value) return showToast("请选择批量状态"); try { await runBatchAction("status", dom.batchStatus.value); } catch (error) { showToast(error.message); } });
dom.batchFollowupBtn.addEventListener("click", async () => { if (!dom.batchFollowup.value) return showToast("请选择跟进日期"); try { await runBatchAction("followup", dom.batchFollowup.value); dom.batchFollowup.value = ""; } catch (error) { showToast(error.message); } });
dom.batchTagsBtn.addEventListener("click", async () => { const tags = dom.batchTags.value.trim(); if (!tags) return showToast("请输入要追加的标签"); try { await runBatchAction("tags", tags); dom.batchTags.value = ""; } catch (error) { showToast(error.message); } });
dom.batchDeleteBtn.addEventListener("click", async () => { const count = state.selectedIds.size; if (!count || !confirm(`确认删除选中的 ${count} 个达人？系统会先自动备份。`)) return; try { await runBatchAction("delete", "", "DELETE_SELECTED"); } catch (error) { showToast(error.message); } });

dom.queueStartBtn.addEventListener("click", startQueue); dom.queueStopBtn.addEventListener("click", stopQueue); dom.queueOpenBtn.addEventListener("click", () => { const row = currentQueueRow(); if (row) window.open(row.tiktokUrl, "_blank", "noopener"); }); dom.queueCopyBtn.addEventListener("click", () => { const row = currentQueueRow(); if (row) copyText(row.drafts.dm, `@${row.handle} 的 DM 已复制`); }); dom.queueSkipBtn.addEventListener("click", () => advanceQueue(false)); dom.queueSentBtn.addEventListener("click", async () => { const row = currentQueueRow(); if (!row) return; await apiJson("/candidates/contact", { method: "POST", body: JSON.stringify({ id: row.id, followUpDate: localDate(3) }) }); await loadWorkspace({ silent: true }); advanceQueue(true); }); dom.queueTargetInput.addEventListener("input", renderQueue);

dom.searchForm.addEventListener("submit", (e) => { e.preventDefault(); const query = `site:tiktok.com/@ "${dom.keywordInput.value.trim()}" "${dom.signalSelect.value}"`; window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, "_blank", "noopener"); });
dom.publicSearchKeyword.addEventListener("input", renderPublicSearchLink);
dom.publicSearchBtn.addEventListener("click", async () => { const keyword = dom.publicSearchKeyword.value.trim(); dom.publicSearchBtn.disabled = true; dom.publicSearchStatus.textContent = "正在读取公开搜索结果..."; try { const result = await apiJson("/public-search/preview", { method: "POST", body: JSON.stringify({ keyword, engine: dom.publicSearchEngine.value, limit: Number(dom.publicSearchLimit.value || 10) }) }); if (!result.configured) { dom.publicSearchStatus.textContent = "未配置搜索 API，已生成手动搜索链接。"; window.open(result.searchUrl, "_blank", "noopener"); return; } if (result.error) throw new Error(result.error); if (result.sourceText) await apiJson("/discovery/import", { method: "POST", body: JSON.stringify({ sourceText: result.sourceText, niche: dom.collectorNiche.value.trim() }) }); await loadWorkspace({ silent: true }); dom.publicSearchStatus.textContent = `搜索源 ${result.engine} · 结果 ${result.resultCount} · 识别账号 ${result.handles.length}`; showToast(`已识别 ${result.handles.length} 个 TikTok 账号`); } catch (error) { dom.publicSearchStatus.textContent = `搜索失败：${error.message}`; } finally { dom.publicSearchBtn.disabled = false; } });
dom.collectorImportBtn.addEventListener("click", async () => { const sourceText = dom.collectorSource.value.trim(); if (!sourceText) return showToast("请粘贴 TikTok 主页链接或 @handle"); try { const result = await apiJson("/discovery/import", { method: "POST", body: JSON.stringify({ sourceText, niche: dom.collectorNiche.value.trim() }) }); dom.collectorSource.value = ""; await loadWorkspace({ silent: true }); showToast(`新增 ${result.added}，更新 ${result.updated}`); } catch (error) { showToast(`导入失败：${error.message}`); } });
dom.hashtagTopic.addEventListener("compositionstart", () => { hashtagComposing = true; });
dom.hashtagTopic.addEventListener("compositionend", () => { hashtagComposing = false; fillHashtagInput(); });
dom.hashtagTopic.addEventListener("input", () => { if (hashtagComposing) return; clearTimeout(hashtagTimer); hashtagTimer = setTimeout(() => fillHashtagInput(), 220); });
dom.hashtagInput.addEventListener("input", () => renderHashtagSuggestions());
dom.hashtagAutoBtn.addEventListener("click", () => { const tags = fillHashtagInput(); showToast(tags.length ? "TikTok 关键词已生成" : "没有可生成的关键词"); });
dom.copyTagsBtn.addEventListener("click", () => { const value = dom.hashtagInput.value.trim(); if (value) copyText(value, "Hashtag 已复制"); else showToast("没有可复制的 Hashtag"); });
dom.openTagsBtn.addEventListener("click", () => openHashtagPages(parseHashtagInput().length ? parseHashtagInput() : buildHashtagSuggestions()));
dom.hashtagSuggestions.addEventListener("click", (e) => { const button = e.target.closest("[data-tag]"); if (button) toggleHashtag(button.dataset.tag); });

dom.candidateList.addEventListener("change", (e) => { const checkbox = e.target.closest("[data-batch-select]"); if (!checkbox) return; if (checkbox.checked) state.selectedIds.add(checkbox.dataset.batchSelect); else state.selectedIds.delete(checkbox.dataset.batchSelect); renderBatchToolbar(); });
dom.candidateList.addEventListener("click", async (e) => { if (e.target.closest(".candidate-select")) return; const action = e.target.closest("[data-action]"); const card = e.target.closest(".candidate-card"); if (!action && card) { state.selectedId = card.dataset.id; state.activeDetailTab = "profile"; renderCandidates(); renderDetail(); return; } if (!action) return; const row = state.payload.candidates.find((item) => item.id === action.dataset.id); if (!row) return; try { if (action.dataset.action === "select") { state.selectedId = row.id; state.activeDetailTab = "profile"; renderCandidates(); renderDetail(); } if (action.dataset.action === "pin") await togglePin(row); if (action.dataset.action === "copy") await copyText(row.drafts.dm, `@${row.handle} 的 DM 已复制`); if (action.dataset.action === "delete") await deleteCandidate(row); } catch (error) { showToast(error.message); } });
dom.detailPinBtn.addEventListener("click", async () => { const row = selectedCandidate(); if (row) await togglePin(row); }); dom.deleteCandidateBtn.addEventListener("click", async () => { try { await deleteCandidate(selectedCandidate()); } catch (error) { showToast(error.message); } });
dom.metricsSaveBtn.addEventListener("click", async () => { const row = selectedCandidate(); if (!row) return; try { await saveCandidate({ ...row, followers: dom.editFollowers.value, avgViews: dom.editViews.value, medianViews: dom.editMedian.value, engagementRate: dom.editEr.value, videoFrequency: dom.editFrequency.value, avatarUrl: dom.editAvatar.value.trim() }, "TikTok 指标已保存，评分已重算"); } catch (error) { showToast(`保存失败：${error.message}`); } });
dom.savedWorkForm.addEventListener("submit", async (e) => { e.preventDefault(); const row = selectedCandidate(); const url = dom.savedWorkUrl.value.trim(); if (!row) return; if (!isTikTokUrl(url)) return showToast("请输入有效的 TikTok 作品链接"); const works = row.savedWorks || []; if (works.some((item) => item.url?.replace(/\/$/, "").toLowerCase() === url.replace(/\/$/, "").toLowerCase())) return showToast("这个作品已经收藏过了"); dom.savedWorkAddBtn.disabled = true; try { await saveCandidate({ ...row, savedWorks: [{ url, title: dom.savedWorkTitle.value.trim(), note: dom.savedWorkNote.value.trim(), createdAt: localDate() }, ...works] }, "作品已收藏"); dom.savedWorkForm.reset(); } catch (error) { showToast(`收藏失败：${error.message}`); } finally { dom.savedWorkAddBtn.disabled = false; } });
dom.savedWorkList.addEventListener("click", async (e) => { const featureButton = e.target.closest("[data-saved-work-feature]"); const deleteButton = e.target.closest("[data-saved-work-delete]"); const row = selectedCandidate(); if (!row) return; if (featureButton) { const nextId = row.featuredWorkId === featureButton.dataset.savedWorkFeature ? "" : featureButton.dataset.savedWorkFeature; state.modelDraft = null; try { await saveCandidate({ ...row, featuredWorkId: nextId }, nextId ? "已设为建联文案参考" : "已取消文案参考"); } catch (error) { showToast(`设置失败：${error.message}`); } return; } if (!deleteButton || !confirm("确认删除这条作品收藏？")) return; try { await saveCandidate({ ...row, savedWorks: (row.savedWorks || []).filter((item) => item.id !== deleteButton.dataset.savedWorkDelete) }, "作品收藏已删除"); } catch (error) { showToast(`删除失败：${error.message}`); } });
dom.detailStatus.addEventListener("change", async (e) => { const row = selectedCandidate(); if (!row) return; await apiJson("/candidates/status", { method: "POST", body: JSON.stringify({ id: row.id, status: e.target.value }) }); await loadWorkspace({ silent: true }); showToast("状态已更新"); });
dom.saveFollowupBtn.addEventListener("click", async () => { const row = selectedCandidate(); if (!row) return; await apiJson("/candidates/followup", { method: "POST", body: JSON.stringify({ id: row.id, followUpDate: dom.followupDate.value }) }); await loadWorkspace({ silent: true }); showToast("跟进日期已保存"); });
dom.quickLogBtn.addEventListener("click", async () => { const row = selectedCandidate(); if (!row) return; await apiJson("/candidates/contact", { method: "POST", body: JSON.stringify({ id: row.id, note: dom.contactNote.value.trim(), followUpDate: dom.followupDate.value || localDate(3) }) }); dom.contactNote.value = ""; await loadWorkspace({ silent: true }); showToast("TikTok 建联已记录"); });

dom.replyGenerateBtn.addEventListener("click", async () => { const row = selectedCandidate(); const replyText = dom.replySource.value.trim(); if (!row || !replyText) return showToast("请先粘贴达人回复"); const result = await apiJson("/reply/generate", { method: "POST", body: JSON.stringify({ candidate: row, replyText }) }); if (!result.ok) return showToast(result.error || "生成失败"); state.replyAnalysis = result; renderReply(); showToast("回复建议已生成"); });
dom.replyCopyBtn.addEventListener("click", () => state.replyAnalysis && copyText(state.replyAnalysis.draft, "回复文案已复制"));
dom.replySaveBtn.addEventListener("click", async () => { const row = selectedCandidate(); const a = state.replyAnalysis; if (!row || !a) return; await apiJson("/candidates/status", { method: "POST", body: JSON.stringify({ id: row.id, status: a.status }) }); await saveCandidate({ ...row, status: a.status, notes: appendNote(row.notes, a.note) }, "达人回复已记录"); state.replyAnalysis = null; dom.replySource.value = ""; renderReply(); });
dom.replyClearBtn.addEventListener("click", () => { state.replyAnalysis = null; dom.replySource.value = ""; renderReply(); });

document.querySelectorAll("[data-draft]").forEach((button) => button.addEventListener("click", () => { state.activeDraft = button.dataset.draft; state.modelDraft = null; const row = selectedCandidate(); if (row) renderDraft(row); }));
dom.copyDraftBtn.addEventListener("click", () => { const row = selectedCandidate(); if (row) copyText(dom.draftText.textContent, "当前建联文案已复制"); }); dom.copyLocalBtn.addEventListener("click", () => { state.modelDraft = null; const row = selectedCandidate(); if (row) renderDraft(row); showToast("已恢复 TikTok 本地模板"); });
dom.copyModelSaveBtn.addEventListener("click", () => { localStorage.setItem(MODEL_KEY, JSON.stringify({ provider: dom.copyModelProvider.value, baseUrl: dom.copyModelBaseUrl.value.trim(), model: dom.copyModelName.value.trim() })); dom.copyModelStatus.textContent = "TikTok 模型配置已保存"; showToast("模型配置已保存"); });
dom.copyModelClearBtn.addEventListener("click", () => { localStorage.removeItem(MODEL_KEY); dom.copyModelProvider.value = "local"; dom.copyModelBaseUrl.value = ""; dom.copyModelName.value = ""; dom.copyModelApiKey.value = ""; dom.copyModelStatus.textContent = "默认使用 TikTok 本地模板"; showToast("模型配置已清空"); });
dom.copyModelTestBtn.addEventListener("click", async () => { try { const result = await apiJson("/copy/test", { method: "POST", body: JSON.stringify(modelPayload()) }); if (!result.ok) throw new Error(result.error || "测试失败"); dom.copyModelStatus.textContent = `接口正常 · ${result.model || result.provider}`; showToast("模型接口测试通过"); } catch (error) { dom.copyModelStatus.textContent = `测试失败：${error.message}`; } });
dom.copyModelBtn.addEventListener("click", async () => { const row = selectedCandidate(); if (!row) return; dom.copyModelBtn.disabled = true; try { const result = await apiJson("/copy/generate", { method: "POST", body: JSON.stringify({ ...modelPayload(), candidate: { ...row, videoFormat: dom.videoFormatSelect.value }, options: { tone: dom.copyToneSelect.value, angle: dom.copyAngleSelect.value, videoFormat: dom.videoFormatSelect.value } }) }); state.modelDraft = { candidateId: row.id, mode: state.activeDraft, text: result.text, subject: result.subject }; renderDraft(row); dom.copyModelStatus.textContent = result.configured ? `模型生成 · ${result.model || "API"}` : result.warnings?.[0] || "已使用本地模板"; showToast("TikTok 建联文案已生成"); } catch (error) { showToast(`生成失败：${error.message}`); } finally { dom.copyModelBtn.disabled = false; } });

dom.partnershipSaveBtn.addEventListener("click", async () => { const row = selectedCandidate(); if (!row) return; const payload = { ...row, invitationSentAt: dom.partnershipInvitation.value, connectionAt: dom.partnershipConnection.value, creatorType: dom.partnershipCreatorType.value.trim(), partnershipStage: dom.partnershipStage.value, quoteJpy: dom.partnershipQuote.value, collabProduct: dom.partnershipProduct.value.trim(), videoFormat: dom.partnershipFormat.value, usageRightsDays: dom.partnershipUsageDays.value, sparkAdsStatus: dom.partnershipSparkStatus.value, sparkAuthorizationCode: dom.partnershipSparkCode.value.trim(), sampleStatus: dom.partnershipSampleStatus.value, sampleCostJpy: dom.partnershipSampleCost.value, recipientName: dom.partnershipRecipient.value.trim(), postalCode: dom.partnershipPostal.value.trim(), shippingAddress: dom.partnershipAddress.value.trim(), phoneNumber: dom.partnershipPhone.value.trim(), orderNumber: dom.partnershipOrder.value.trim(), shippingTracking: dom.partnershipTracking.value.trim(), shippedAt: dom.partnershipShipped.value, receivedAt: dom.partnershipReceived.value, videoProgress: dom.partnershipProgress.value, scriptDueDate: dom.partnershipScriptDue.value, draftDueDate: dom.partnershipDraftDue.value, postDate: dom.partnershipPostDate.value, postUrl: dom.partnershipPostUrl.value.trim(), couponCode: dom.partnershipCoupon.value.trim(), orders: dom.partnershipOrders.value, revenueJpy: dom.partnershipRevenue.value }; try { await saveCandidate(payload, "TikTok 合作追踪已保存"); } catch (error) { showToast(`保存失败：${error.message}`); } });

dom.candidateForm.addEventListener("submit", async (e) => { e.preventDefault(); const payload = Object.fromEntries(new FormData(dom.candidateForm).entries()); try { await saveCandidate(payload, "TikTok 达人已加入候选池"); dom.candidateForm.reset(); } catch (error) { showToast(`新增失败：${error.message}`); } });
dom.deleteAllBtn.addEventListener("click", async () => { if (prompt("输入 DELETE 确认清空 TikTok 候选池") !== "DELETE") return; const result = await apiJson("/candidates/delete-all", { method: "POST", body: JSON.stringify({ confirm: "DELETE" }) }); state.selectedId = ""; await loadWorkspace({ silent: true }); showToast(`已删除 ${result.deleted} 个 TikTok 达人`); });

dom.csvInput.addEventListener("change", async (e) => { const file = e.target.files?.[0]; e.target.value = ""; if (!file) return; state.pendingCsv = await file.text(); try { state.importPreview = await apiJson("/import/preview", { method: "POST", body: JSON.stringify({ csvText: state.pendingCsv }) }); renderImportPreview(); } catch (error) { showToast(`预览失败：${error.message}`); } });
dom.cancelImportBtn.addEventListener("click", () => { state.pendingCsv = ""; state.importPreview = null; renderImportPreview(); });
dom.confirmImportBtn.addEventListener("click", async () => { if (!state.pendingCsv) return; const result = await apiJson("/import", { method: "POST", body: JSON.stringify({ csvText: state.pendingCsv }) }); state.pendingCsv = ""; state.importPreview = null; await loadWorkspace({ silent: true }); showToast(`CSV 已导入：新增 ${result.added}，更新 ${result.updated}`); });

window.addEventListener("scroll", () => dom.scrollTopBtn.classList.toggle("is-visible", window.scrollY > 520), { passive: true }); dom.scrollTopBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
initDiscoveryTools(); loadModelConfig(); renderPublicSearchLink(); fillHashtagInput(); loadWorkspace({ silent: true });
