const state = {
  payload: null,
  selectedId: "",
  activeDraft: "dm",
  previewMode: "",
  pendingImportCsv: "",
  pendingCollector: null,
  pendingWebsite: null,
  importPreview: null,
  skillPrompt: "",
  queue: {
    active: false,
    ids: [],
    index: 0,
    sent: 0,
    total: 0,
  },
  profileCandidateId: "",
  profileSuggestion: null,
  templateKey: "",
  copyMode: "default",
  copyTone: "warm",
  copyLength: "standard",
  copyHook: "",
  copyModelProvider: "local",
  copyModelBaseUrl: "",
  copyModelName: "",
  copyModelAuthMode: "bearer",
  copyModelApiKey: "",
  copyModelSaveKey: false,
  modelDraft: null,
  productKey: "auto",
  replyAnalysis: null,
  hashtagInputEdited: false,
  filters: {
    search: "",
    status: "",
    tier: "",
    workflow: "",
    sort: "score_desc",
  },
};

const dom = {
  refreshBtn: document.getElementById("refresh-btn"),
  csvInput: document.getElementById("csv-input"),
  importPreviewPanel: document.getElementById("import-preview-panel"),
  importPreviewTitle: document.getElementById("import-preview-title"),
  importPreviewSummary: document.getElementById("import-preview-summary"),
  importPreviewList: document.getElementById("import-preview-list"),
  cancelImportBtn: document.getElementById("cancel-import-btn"),
  confirmImportBtn: document.getElementById("confirm-import-btn"),
  statTotal: document.getElementById("stat-total"),
  statReady: document.getElementById("stat-ready"),
  statScore: document.getElementById("stat-score"),
  statContacted: document.getElementById("stat-contacted"),
  statBudget: document.getElementById("stat-budget"),
  queueCaption: document.getElementById("queue-caption"),
  queueCurrent: document.getElementById("queue-current"),
  queueProgressFill: document.getElementById("queue-progress-fill"),
  queueTargetInput: document.getElementById("queue-target-input"),
  queueStartBtn: document.getElementById("queue-start-btn"),
  queueOpenBtn: document.getElementById("queue-open-btn"),
  queueCopyBtn: document.getElementById("queue-copy-btn"),
  queueSentNextBtn: document.getElementById("queue-sent-next-btn"),
  queueSkipBtn: document.getElementById("queue-skip-btn"),
  queueStopBtn: document.getElementById("queue-stop-btn"),
  taskDueToday: document.getElementById("task-due-today"),
  taskDueTodayList: document.getElementById("task-due-today-list"),
  taskOverdue: document.getElementById("task-overdue"),
  taskOverdueList: document.getElementById("task-overdue-list"),
  taskReplied: document.getElementById("task-replied"),
  taskRepliedList: document.getElementById("task-replied-list"),
  taskNegotiating: document.getElementById("task-negotiating"),
  taskNegotiatingList: document.getElementById("task-negotiating-list"),
  taskNeedsData: document.getElementById("task-needs-data"),
  taskNeedsDataList: document.getElementById("task-needs-data-list"),
  taskSamplePending: document.getElementById("task-sample-pending"),
  taskSamplePendingList: document.getElementById("task-sample-pending-list"),
  taskShipping: document.getElementById("task-shipping"),
  taskShippingList: document.getElementById("task-shipping-list"),
  taskShooting: document.getElementById("task-shooting"),
  taskShootingList: document.getElementById("task-shooting-list"),
  taskPublish: document.getElementById("task-publish"),
  taskPublishList: document.getElementById("task-publish-list"),
  hashtagList: document.getElementById("hashtag-list"),
  hashtagInput: document.getElementById("hashtag-input"),
  hashtagSuggestions: document.getElementById("hashtag-suggestions"),
  hashtagAutoBtn: document.getElementById("hashtag-auto-btn"),
  openInputTagsBtn: document.getElementById("open-input-tags-btn"),
  copyTagsBtn: document.getElementById("copy-tags-btn"),
  queryList: document.getElementById("query-list"),
  marketplaceList: document.getElementById("marketplace-list"),
  openTagsBtn: document.getElementById("open-tags-btn"),
  searchForm: document.getElementById("search-form"),
  keywordInput: document.getElementById("keyword-input"),
  signalSelect: document.getElementById("signal-select"),
  publicSearchKeyword: document.getElementById("public-search-keyword"),
  publicSearchEngine: document.getElementById("public-search-engine"),
  publicSearchLimit: document.getElementById("public-search-limit"),
  publicSearchBtn: document.getElementById("public-search-btn"),
  publicSearchStatus: document.getElementById("public-search-status"),
  publicSearchOpenLink: document.getElementById("public-search-open-link"),
  skillSourceMode: document.getElementById("skill-source-mode"),
  skillMarket: document.getElementById("skill-market"),
  skillMinFollowers: document.getElementById("skill-min-followers"),
  skillMaxFollowers: document.getElementById("skill-max-followers"),
  skillPerTermLimit: document.getElementById("skill-per-term-limit"),
  skillTopTarget: document.getElementById("skill-top-target"),
  skillRawTarget: document.getElementById("skill-raw-target"),
  skillLanguage: document.getElementById("skill-language"),
  skillNiche: document.getElementById("skill-niche"),
  skillSeeds: document.getElementById("skill-seeds"),
  skillExclusions: document.getElementById("skill-exclusions"),
  skillFullAngle: document.getElementById("skill-full-angle"),
  skillStrictFilter: document.getElementById("skill-strict-filter"),
  skillGeneratePromptBtn: document.getElementById("skill-generate-prompt-btn"),
  skillCreatePlanBtn: document.getElementById("skill-create-plan-btn"),
  skillCopyPromptBtn: document.getElementById("skill-copy-prompt-btn"),
  skillPromptOutput: document.getElementById("skill-prompt-output"),
  skillPanelStatus: document.getElementById("skill-panel-status"),
  skillRunList: document.getElementById("skill-run-list"),
  skillRefreshRunsBtn: document.getElementById("skill-refresh-runs-btn"),
  collectorKeyword: document.getElementById("collector-keyword"),
  collectorSource: document.getElementById("collector-source"),
  collectorPreviewBtn: document.getElementById("collector-preview-btn"),
  websiteKeyword: document.getElementById("website-keyword"),
  websiteSource: document.getElementById("website-source"),
  websitePreviewBtn: document.getElementById("website-preview-btn"),
  websiteStatus: document.getElementById("website-status"),
  filterSearch: document.getElementById("filter-search"),
  filterStatus: document.getElementById("filter-status"),
  filterTier: document.getElementById("filter-tier"),
  filterSort: document.getElementById("filter-sort"),
  clearFiltersBtn: document.getElementById("clear-filters-btn"),
  deleteAllCandidatesBtn: document.getElementById("delete-all-candidates-btn"),
  candidateList: document.getElementById("candidate-list"),
  detailTitle: document.getElementById("detail-title"),
  detailEmpty: document.getElementById("detail-empty"),
  detailContent: document.getElementById("detail-content"),
  detailAvatar: document.getElementById("detail-avatar"),
  detailName: document.getElementById("detail-name"),
  detailUrl: document.getElementById("detail-url"),
  detailScore: document.getElementById("detail-score"),
  detailTier: document.getElementById("detail-tier"),
  detailFollowers: document.getElementById("detail-followers"),
  detailEr: document.getElementById("detail-er"),
  detailStatus: document.getElementById("detail-status"),
  deleteCandidateBtn: document.getElementById("delete-candidate-btn"),
  scoreBreakdown: document.getElementById("score-breakdown"),
  followupDate: document.getElementById("followup-date"),
  saveFollowupBtn: document.getElementById("save-followup-btn"),
  contactNote: document.getElementById("contact-note"),
  quickLogBtn: document.getElementById("quick-log-btn"),
  contactHistory: document.getElementById("contact-history"),
  manualChecklist: document.getElementById("manual-checklist"),
  instagramEnrichBtn: document.getElementById("instagram-enrich-btn"),
  instagramEnrichStatus: document.getElementById("instagram-enrich-status"),
  profileExtractBtn: document.getElementById("profile-extract-btn"),
  profileSource: document.getElementById("profile-source"),
  profilePreview: document.getElementById("profile-preview"),
  profileApplyBtn: document.getElementById("profile-apply-btn"),
  emailSubjectRow: document.getElementById("email-subject-row"),
  emailSubject: document.getElementById("email-subject"),
  draftText: document.getElementById("draft-text"),
  copyDraftBtn: document.getElementById("copy-draft-btn"),
  templateSelect: document.getElementById("template-select"),
  templateCopyBtn: document.getElementById("template-copy-btn"),
  productSelect: document.getElementById("product-select"),
  productPoints: document.getElementById("product-points"),
  copyToneSelect: document.getElementById("copy-tone-select"),
  copyLengthSelect: document.getElementById("copy-length-select"),
  copyHookInput: document.getElementById("copy-hook-input"),
  copyInsights: document.getElementById("copy-insights"),
  copyRecommendBtn: document.getElementById("copy-recommend-btn"),
  copyOptimizeBtn: document.getElementById("copy-optimize-btn"),
  copyModelBtn: document.getElementById("copy-model-btn"),
  copyDefaultBtn: document.getElementById("copy-default-btn"),
  copyModelProvider: document.getElementById("copy-model-provider"),
  copyModelBaseUrl: document.getElementById("copy-model-base-url"),
  copyModelName: document.getElementById("copy-model-name"),
  copyModelAuthMode: document.getElementById("copy-model-auth-mode"),
  copyModelApiKey: document.getElementById("copy-model-api-key"),
  copyModelSaveKey: document.getElementById("copy-model-save-key"),
  copyModelSaveBtn: document.getElementById("copy-model-save-btn"),
  copyModelTestBtn: document.getElementById("copy-model-test-btn"),
  copyModelClearBtn: document.getElementById("copy-model-clear-btn"),
  copyModelStatus: document.getElementById("copy-model-status"),
  replyAnalyzeBtn: document.getElementById("reply-analyze-btn"),
  replyModelBtn: document.getElementById("reply-model-btn"),
  replySource: document.getElementById("reply-source"),
  replyInsights: document.getElementById("reply-insights"),
  replyDraft: document.getElementById("reply-draft"),
  replyCopyBtn: document.getElementById("reply-copy-btn"),
  replyLogBtn: document.getElementById("reply-log-btn"),
  replyClearBtn: document.getElementById("reply-clear-btn"),
  partnershipInvitationSentAt: document.getElementById("partnership-invitation-sent-at"),
  partnershipConnectionAt: document.getElementById("partnership-connection-at"),
  partnershipBloggerId: document.getElementById("partnership-blogger-id"),
  partnershipCreatorType: document.getElementById("partnership-creator-type"),
  partnershipFollowers: document.getElementById("partnership-followers"),
  partnershipProfileUrl: document.getElementById("partnership-profile-url"),
  partnershipStage: document.getElementById("partnership-stage"),
  partnershipQuote: document.getElementById("partnership-quote"),
  partnershipCollabProduct: document.getElementById("partnership-collab-product"),
  partnershipSampleStatus: document.getElementById("partnership-sample-status"),
  partnershipSampleCost: document.getElementById("partnership-sample-cost"),
  partnershipRecipientName: document.getElementById("partnership-recipient-name"),
  partnershipPostalCode: document.getElementById("partnership-postal-code"),
  partnershipShippingAddress: document.getElementById("partnership-shipping-address"),
  partnershipPhoneNumber: document.getElementById("partnership-phone-number"),
  partnershipOrderNumber: document.getElementById("partnership-order-number"),
  partnershipTracking: document.getElementById("partnership-tracking"),
  partnershipShippedAt: document.getElementById("partnership-shipped-at"),
  partnershipReceivedAt: document.getElementById("partnership-received-at"),
  partnershipVideoProgress: document.getElementById("partnership-video-progress"),
  partnershipPostDate: document.getElementById("partnership-post-date"),
  partnershipPostUrl: document.getElementById("partnership-post-url"),
  partnershipCoupon: document.getElementById("partnership-coupon"),
  partnershipOrders: document.getElementById("partnership-orders"),
  partnershipRevenue: document.getElementById("partnership-revenue"),
  partnershipSummary: document.getElementById("partnership-summary"),
  partnershipSaveBtn: document.getElementById("partnership-save-btn"),
  candidateForm: document.getElementById("candidate-form"),
  sourceCaption: document.getElementById("source-caption"),
  scrollTopBtn: document.getElementById("scroll-top-btn"),
  toast: document.getElementById("toast"),
};

let toastTimer;

const HASHTAG_PRESETS = [
  {
    pattern: /fashion|ファッション|コーデ|服|style|ootd|穿搭|大人女子|tokyo|東京/i,
    tags: ["fashionbloggerjapan", "japanesefashion", "tokyofashion", "ootdjapan", "japanesestyle", "大人女子コーデ", "きれいめコーデ"],
  },
  {
    pattern: /美容|beauty|cosme|makeup|skin|健康|ライフスタイル/i,
    tags: ["japanesebeauty", "beautycreator", "skincarejapan", "lifestylejapan", "美容好きな人と繋がりたい"],
  },
  {
    pattern: /ママ|mama|mom|主婦|育児/i,
    tags: ["ママコーデ", "mamagirl", "mamafashion", "30代ファッション", "40代ファッション"],
  },
  {
    pattern: /低身長|骨格|体型|着回し|通勤|オフィス|淡色/i,
    tags: ["低身長コーデ", "骨格ウェーブ", "着回しコーデ", "通勤コーデ", "オフィスコーデ", "淡色コーデ"],
  },
];

const FALLBACK_HASHTAGS = ["fashionbloggerjapan", "japanesefashion", "tokyofashion", "ootdjapan", "japanesestyle", "大人女子コーデ"];

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function safeImageUrl(value) {
  const url = String(value || "").trim();
  return /^https?:\/\//i.test(url) ? url : "";
}

function renderCreatorAvatar(row, className = "candidate-avatar") {
  const label = escapeHtml(initials(row.name || row.handle));
  const imageUrl = safeImageUrl(row.avatarUrl);
  if (!imageUrl) {
    return `<div class="${className} is-fallback"><span>${label}</span></div>`;
  }
  const alt = escapeHtml(row.name || row.handle || "creator");
  return `
    <div class="${className} has-image">
      <span>${label}</span>
      <img src="${escapeHtml(imageUrl)}" alt="${alt}" loading="lazy" referrerpolicy="no-referrer" onerror="this.hidden=true;">
    </div>
  `;
}

function renderDetailAvatar(row) {
  const imageUrl = safeImageUrl(row.avatarUrl);
  dom.detailAvatar.classList.toggle("has-image", Boolean(imageUrl));
  dom.detailAvatar.classList.toggle("is-fallback", !imageUrl);
  dom.detailAvatar.innerHTML = imageUrl
    ? `<span>${escapeHtml(initials(row.name || row.handle))}</span><img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(row.name || row.handle || "creator")}" referrerpolicy="no-referrer" onerror="this.hidden=true;">`
    : `<span>${escapeHtml(initials(row.name || row.handle))}</span>`;
}

function formatNumber(value) {
  const number = Number(value || 0);
  return new Intl.NumberFormat("ja-JP").format(number);
}

function formatCompact(value) {
  const number = Number(value || 0);
  if (number >= 10000) {
    return `${Math.round(number / 1000) / 10}万`;
  }
  return formatNumber(number);
}

function formatCurrency(value) {
  return new Intl.NumberFormat("ja-JP", {
    style: "currency",
    currency: "JPY",
    maximumFractionDigits: 0,
  }).format(Number(value || 0));
}

function formatSignedPercent(value) {
  if (!Number.isFinite(value)) {
    return "-";
  }
  const prefix = value > 0 ? "+" : "";
  return `${prefix}${Math.round(value)}%`;
}

function showToast(message) {
  dom.toast.textContent = message;
  dom.toast.classList.add("is-visible");
  clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => dom.toast.classList.remove("is-visible"), 2200);
}

function updateScrollTopButton() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop || 0;
  dom.scrollTopBtn.classList.toggle("is-visible", scrollTop > 520);
}

async function apiJson(url, options = {}) {
  const response = await fetch(url, {
    cache: "no-store",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

async function loadWorkspace({ silent = false } = {}) {
  try {
    const payload = await apiJson("/api/workspace");
    state.payload = payload;
    if (!state.selectedId && payload.candidates.length) {
      state.selectedId = payload.candidates[0].id;
    }
    render();
    if (!silent) {
      showToast("本地达人池已刷新");
    }
  } catch (error) {
    showToast(`加载失败：${error.message}`);
  }
}

function render() {
  if (!state.payload) {
    return;
  }
  renderStats();
  renderImportPreview();
  renderStatusOptions();
  renderTaskBoard();
  renderQueue();
  renderPublicSearchLink();
  renderSkillPanel();
  renderDiscovery();
  renderCandidates();
  renderDetail();
  renderSource();
}

function renderStats() {
  const stats = state.payload.stats;
  dom.statTotal.textContent = formatNumber(stats.total);
  dom.statReady.textContent = formatNumber(stats.ready);
  dom.statScore.textContent = stats.avgScore;
  dom.statContacted.textContent = formatNumber(stats.contacted);
  dom.statBudget.textContent = formatCurrency(stats.estimatedCostJpy);
}

function renderImportPreview() {
  const preview = state.importPreview;
  dom.importPreviewPanel.hidden = !preview;
  if (!preview) {
    dom.importPreviewTitle.textContent = "CSV 导入预览";
    dom.importPreviewSummary.innerHTML = "";
    dom.importPreviewList.innerHTML = "";
    return;
  }
  dom.importPreviewTitle.textContent =
    state.previewMode === "collector"
      ? "采集候选预览"
      : state.previewMode === "website"
        ? "达人网站识别预览"
        : "CSV 导入预览";
  const summary = preview.summary || {};
  dom.importPreviewSummary.innerHTML = [
    ["新增", summary.add || 0],
    ["更新", summary.update || 0],
    [state.previewMode === "collector" || state.previewMode === "website" ? "文本重复" : "CSV重复", summary.duplicate_source || summary.duplicate_csv || 0],
    ["跳过", summary.skip || 0],
    ["总行数", summary.rows || 0],
  ]
    .map(([label, value]) => `<span class="mini-pill">${label} ${formatNumber(value)}</span>`)
    .join("");
  dom.importPreviewList.innerHTML = (preview.rows || [])
    .slice(0, 24)
    .map((row) => {
      const candidate = row.candidate || {};
      const issues = (row.issues || []).join(" / ");
      return `
        <article class="preview-row" data-action="${escapeHtml(row.action)}">
          <strong>#${row.row} @${escapeHtml(candidate.handle || candidate.name || "-")}</strong>
          <span>${escapeHtml(actionLabel(row.action))} · ${escapeHtml(candidate.niche || "-")} · ${candidate.score || 0}${escapeHtml(candidate.tier || "")}</span>
          <small>${escapeHtml(issues || "字段看起来正常")}</small>
          ${candidate.matchedText ? `<small>${escapeHtml(candidate.matchedText)}</small>` : ""}
        </article>
      `;
    })
    .join("");
}

function actionLabel(action) {
  return {
    add: "新增",
    update: "更新",
    duplicate_csv: "重复",
    duplicate_source: "重复",
    skip: "跳过",
  }[action] || action;
}

function renderStatusOptions() {
  const labels = state.payload.statusLabels;
  const options = [
    `<option value="">全部</option>`,
    ...Object.entries(labels).map(([value, label]) => `<option value="${value}">${escapeHtml(label)}</option>`),
  ].join("");
  if (!dom.filterStatus.dataset.ready) {
    dom.filterStatus.innerHTML = options;
    dom.filterStatus.dataset.ready = "1";
  }
  const detailOptions = Object.entries(labels)
    .map(([value, label]) => `<option value="${value}">${escapeHtml(label)}</option>`)
    .join("");
  dom.detailStatus.innerHTML = detailOptions;
}


function todayKey() {
  return localDateKey(new Date());
}

function localDateKey(date) {
  const localTime = date.getTime() - date.getTimezoneOffset() * 60000;
  return new Date(localTime).toISOString().slice(0, 10);
}

function isClosed(row) {
  return ["approved", "rejected"].includes(row.status);
}

function isDueToday(row) {
  return Boolean(row.followUpDate) && row.followUpDate === todayKey() && !isClosed(row);
}

function isOverdue(row) {
  return Boolean(row.followUpDate) && row.followUpDate < todayKey() && !isClosed(row);
}

function needsData(row) {
  return (
    !row.followers ||
    !row.engagementRate ||
    !row.notes ||
    (row.contactMethod === "email" && !row.email)
  );
}

function needsSampleSend(row) {
  return (
    !isClosed(row) &&
    (
      row.partnershipStage === "sample_pending" ||
      row.sampleStatus === "requested" ||
      row.sampleStatus === "prepared"
    )
  );
}

function isShipping(row) {
  return (
    !isClosed(row) &&
    row.sampleStatus === "sent" &&
    !row.receivedAt &&
    row.videoProgress !== "posted" &&
    row.videoProgress !== "measured"
  );
}

function needsShooting(row) {
  const sampleArrived = row.sampleStatus === "delivered" || Boolean(row.receivedAt);
  const progress = row.videoProgress || "not_started";
  return (
    !isClosed(row) &&
    sampleArrived &&
    ["not_started", "product_confirming", "sample_sent"].includes(progress)
  );
}

function needsPublish(row) {
  const progress = row.videoProgress || "not_started";
  return (
    !isClosed(row) &&
    ["filming", "draft_review", "revision"].includes(progress) &&
    row.partnershipStage !== "posted" &&
    row.partnershipStage !== "measured" &&
    !row.postUrl
  );
}

function workflowMatches(row, workflow) {
  return {
    due_today: isDueToday(row),
    overdue: isOverdue(row),
    replied: row.status === "replied",
    negotiating: row.status === "negotiating",
    needs_data: needsData(row),
    sample_pending: needsSampleSend(row),
    shipping: isShipping(row),
    shooting: needsShooting(row),
    publish: needsPublish(row),
  }[workflow] ?? true;
}

function taskGroups() {
  const rows = state.payload?.candidates || [];
  return {
    due_today: rows.filter(isDueToday),
    overdue: rows.filter(isOverdue),
    replied: rows.filter((row) => row.status === "replied"),
    negotiating: rows.filter((row) => row.status === "negotiating"),
    needs_data: rows.filter(needsData),
    sample_pending: rows.filter(needsSampleSend),
    shipping: rows.filter(isShipping),
    shooting: rows.filter(needsShooting),
    publish: rows.filter(needsPublish),
  };
}

function taskListText(rows) {
  if (!rows.length) {
    return "暂无";
  }
  return rows
    .slice(0, 3)
    .map((row) => `@${row.handle || row.name}`)
    .join(" / ");
}

function renderTaskBoard() {
  const groups = taskGroups();
  dom.taskDueToday.textContent = formatNumber(groups.due_today.length);
  dom.taskDueTodayList.textContent = taskListText(groups.due_today);
  dom.taskOverdue.textContent = formatNumber(groups.overdue.length);
  dom.taskOverdueList.textContent = taskListText(groups.overdue);
  dom.taskReplied.textContent = formatNumber(groups.replied.length);
  dom.taskRepliedList.textContent = taskListText(groups.replied);
  dom.taskNegotiating.textContent = formatNumber(groups.negotiating.length);
  dom.taskNegotiatingList.textContent = taskListText(groups.negotiating);
  dom.taskNeedsData.textContent = formatNumber(groups.needs_data.length);
  dom.taskNeedsDataList.textContent = taskListText(groups.needs_data);
  dom.taskSamplePending.textContent = formatNumber(groups.sample_pending.length);
  dom.taskSamplePendingList.textContent = taskListText(groups.sample_pending);
  dom.taskShipping.textContent = formatNumber(groups.shipping.length);
  dom.taskShippingList.textContent = taskListText(groups.shipping);
  dom.taskShooting.textContent = formatNumber(groups.shooting.length);
  dom.taskShootingList.textContent = taskListText(groups.shooting);
  dom.taskPublish.textContent = formatNumber(groups.publish.length);
  dom.taskPublishList.textContent = taskListText(groups.publish);
  document.querySelectorAll("[data-workflow]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.workflow === state.filters.workflow);
  });
}

function renderDiscovery() {
  const discovery = state.payload.discovery;
  dom.hashtagList.innerHTML = discovery.hashtags
    .map(
      (item) => `
        <a href="${item.instagramUrl}" target="_blank" rel="noreferrer">${escapeHtml(item.label)}</a>
      `,
    )
    .join("");
  renderHashtagAssistant();
  dom.queryList.innerHTML = discovery.queries
    .slice(0, 8)
    .map(
      (item) => `
        <a class="query-row" href="${item.url}" target="_blank" rel="noreferrer">
          <strong>${escapeHtml(item.label)}</strong>
          <span>${escapeHtml(item.query)}</span>
        </a>
      `,
    )
    .join("");
  dom.marketplaceList.innerHTML = discovery.marketplace
    .map(
      (item) => `
        <a class="marketplace-row" href="${item.url}" target="_blank" rel="noreferrer">
          <strong>${escapeHtml(item.label)}</strong>
          <small>${escapeHtml(item.note)}</small>
        </a>
      `,
    )
    .join("");
}

function cleanHashtag(value) {
  return String(value || "")
    .trim()
    .replace(/^#+/, "")
    .replace(/https?:\/\/\S+/gi, "")
    .replace(/[@#＃]/g, "")
    .replace(/[^\p{L}\p{N}_]+/gu, "")
    .slice(0, 42);
}

function hashtagsFromText(value) {
  const textValue = String(value || "");
  const directTags = Array.from(textValue.matchAll(/#([\p{L}\p{N}_-]{2,42})/gu)).map((match) => match[1]);
  const chunks = textValue
    .replace(/site:instagram\.com/gi, " ")
    .replace(/\bOR\b/gi, "\n")
    .replace(/[()"']/g, " ")
    .split(/[\r\n,，、;；|]+/)
    .map((chunk) => chunk.trim())
    .filter(Boolean);
  const phraseTags = chunks.flatMap((chunk) => {
    const parts = chunk.split(/\s+/).filter((part) => part.length > 1);
    const hasNonAscii = /[^\x00-\x7F]/.test(chunk);
    if (hasNonAscii && parts.length > 1) {
      return parts;
    }
    const usefulParts = hasNonAscii ? parts : [];
    return [chunk, ...usefulParts];
  });
  return mergeUnique(directTags, phraseTags)
    .map(cleanHashtag)
    .filter((tag) => tag.length >= 2 && tag.toLowerCase() !== "instagram");
}

function buildHashtagSuggestions() {
  const row = selectedCandidate();
  const sourceText = [
    dom.keywordInput.value,
    dom.publicSearchKeyword.value,
    dom.collectorSource.value.trim() ? dom.collectorKeyword.value : "",
    dom.websiteSource.value.trim() ? dom.websiteKeyword.value : "",
    row?.niche || "",
    ...(row?.tags || []),
  ].join("\n");
  const presetTags = HASHTAG_PRESETS
    .filter((preset) => preset.pattern.test(sourceText))
    .flatMap((preset) => preset.tags);
  const discoveryTags = (state.payload?.discovery?.hashtags || []).map((item) => item.label);
  return mergeUnique(hashtagsFromText(sourceText), presetTags, discoveryTags, FALLBACK_HASHTAGS)
    .map(cleanHashtag)
    .filter(Boolean)
    .slice(0, 18);
}

function parseHashtagInput() {
  return hashtagsFromText(dom.hashtagInput.value);
}

function formatHashtags(tags) {
  return tags
    .map(cleanHashtag)
    .filter(Boolean)
    .slice(0, 12)
    .map((tag) => `#${tag}`)
    .join(" ");
}

function fillHashtagInput({ force = false } = {}) {
  const tags = buildHashtagSuggestions();
  if ((force || !state.hashtagInputEdited || !dom.hashtagInput.value.trim()) && tags.length) {
    dom.hashtagInput.value = formatHashtags(tags);
    if (force) {
      state.hashtagInputEdited = false;
    }
  }
  renderHashtagSuggestions(tags);
  return tags;
}

function renderHashtagAssistant() {
  fillHashtagInput();
}

function renderHashtagSuggestions(tags = buildHashtagSuggestions()) {
  const selected = new Set(parseHashtagInput().map((tag) => tag.toLowerCase()));
  dom.hashtagSuggestions.innerHTML = tags
    .slice(0, 12)
    .map((tag) => {
      const clean = cleanHashtag(tag);
      const active = selected.has(clean.toLowerCase()) ? " is-active" : "";
      return `<button class="hashtag-chip${active}" type="button" data-tag="${escapeHtml(clean)}">#${escapeHtml(clean)}</button>`;
    })
    .join("");
}

function addHashtagToInput(tag) {
  const tags = mergeUnique(parseHashtagInput(), [cleanHashtag(tag)]).slice(0, 12);
  dom.hashtagInput.value = formatHashtags(tags);
  state.hashtagInputEdited = true;
  renderHashtagSuggestions();
}

function openHashtagPages(tags) {
  const cleanTags = tags.map(cleanHashtag).filter(Boolean).slice(0, 8);
  if (!cleanTags.length) {
    showToast("没有可打开的 Hashtag");
    return;
  }
  cleanTags.forEach((tag, index) => {
    const url = `https://www.instagram.com/explore/tags/${encodeURIComponent(tag)}/`;
    window.setTimeout(() => window.open(url, "_blank", "noopener,noreferrer"), index * 120);
  });
}

function filteredCandidates() {
  const rows = state.payload?.candidates || [];
  const filtered = rows.filter((row) => {
    if (state.filters.status && row.status !== state.filters.status) {
      return false;
    }
    if (state.filters.tier && row.tier !== state.filters.tier) {
      return false;
    }
    if (state.filters.workflow && !workflowMatches(row, state.filters.workflow)) {
      return false;
    }
    if (state.filters.search) {
      const blob = [
        row.handle,
        row.name,
        row.niche,
        row.location,
        row.notes,
        ...(row.tags || []),
      ]
        .join(" ")
        .toLowerCase();
      if (!blob.includes(state.filters.search.toLowerCase())) {
        return false;
      }
    }
    return true;
  });
  return sortedCandidates(filtered);
}

function numericSortValue(row, key) {
  const value = Number(row[key] || 0);
  return Number.isFinite(value) && value > 0 ? value : null;
}

function dateSortValue(row, ...keys) {
  for (const key of keys) {
    const raw = row[key];
    if (!raw) {
      continue;
    }
    const time = Date.parse(raw);
    if (Number.isFinite(time)) {
      return time;
    }
  }
  return null;
}

function compareNullable(a, b, direction = "desc") {
  const aEmpty = a === null || a === undefined || a === "";
  const bEmpty = b === null || b === undefined || b === "";
  if (aEmpty && bEmpty) {
    return 0;
  }
  if (aEmpty) {
    return 1;
  }
  if (bEmpty) {
    return -1;
  }
  return direction === "asc" ? a - b : b - a;
}

function videoProgressRank(row) {
  return {
    not_started: 0,
    product_confirming: 1,
    sample_sent: 2,
    filming: 3,
    draft_review: 4,
    revision: 5,
    posted: 6,
    measured: 7,
  }[row.videoProgress || "not_started"] ?? 0;
}

function sortedCandidates(rows) {
  const sortKey = state.filters.sort || "score_desc";
  const withIndex = rows.map((row, index) => ({ row, index }));
  withIndex.sort((a, b) => {
    if (Boolean(a.row.pinned) !== Boolean(b.row.pinned)) {
      return a.row.pinned ? -1 : 1;
    }
    let result = 0;
    if (sortKey === "updated_desc") {
      result = compareNullable(
        dateSortValue(a.row, "updatedAt", "createdAt"),
        dateSortValue(b.row, "updatedAt", "createdAt"),
        "desc",
      );
    } else if (sortKey === "followers_desc") {
      result = compareNullable(numericSortValue(a.row, "followers"), numericSortValue(b.row, "followers"), "desc");
    } else if (sortKey === "followers_asc") {
      result = compareNullable(numericSortValue(a.row, "followers"), numericSortValue(b.row, "followers"), "asc");
    } else if (sortKey === "quote_asc") {
      result = compareNullable(numericSortValue(a.row, "quoteJpy"), numericSortValue(b.row, "quoteJpy"), "asc");
    } else if (sortKey === "quote_desc") {
      result = compareNullable(numericSortValue(a.row, "quoteJpy"), numericSortValue(b.row, "quoteJpy"), "desc");
    } else if (sortKey === "connection_desc") {
      result = compareNullable(
        dateSortValue(a.row, "connectionAt", "lastContacted", "invitationSentAt"),
        dateSortValue(b.row, "connectionAt", "lastContacted", "invitationSentAt"),
        "desc",
      );
    } else if (sortKey === "shipped_desc") {
      result = compareNullable(dateSortValue(a.row, "shippedAt"), dateSortValue(b.row, "shippedAt"), "desc");
    } else if (sortKey === "received_desc") {
      result = compareNullable(dateSortValue(a.row, "receivedAt"), dateSortValue(b.row, "receivedAt"), "desc");
    } else if (sortKey === "video_progress_desc") {
      result = compareNullable(videoProgressRank(a.row), videoProgressRank(b.row), "desc");
    } else {
      result = compareNullable(numericSortValue(a.row, "score"), numericSortValue(b.row, "score"), "desc");
    }
    if (result !== 0) {
      return result;
    }
    const scoreFallback = compareNullable(numericSortValue(a.row, "score"), numericSortValue(b.row, "score"), "desc");
    return scoreFallback || a.index - b.index;
  });
  return withIndex.map((item) => item.row);
}

function isQueueEligible(row) {
  return Boolean(row.handle) && !["contacted", "replied", "negotiating", "approved", "rejected"].includes(row.status);
}

function queueEligibleRows() {
  return filteredCandidates().filter(isQueueEligible);
}

function currentQueueRow() {
  if (!state.queue.active) {
    return null;
  }
  const id = state.queue.ids[state.queue.index];
  return (state.payload?.candidates || []).find((row) => row.id === id) || null;
}

function queueProgressText(row) {
  if (!row) {
    return "队列已完成";
  }
  const label = state.payload.statusLabels[row.status] || row.status;
  return `第 ${state.queue.index + 1}/${state.queue.total || state.queue.ids.length} 个 · @${row.handle} · ${row.score}${row.tier} · ${label}`;
}

function contactedTodayCount() {
  const today = todayKey();
  return (state.payload?.candidates || []).filter((row) => {
    if (row.lastContacted === today) {
      return true;
    }
    return (row.contactHistory || []).some((item) => item.type === "contacted" && item.date === today);
  }).length;
}

function renderQueue() {
  const active = state.queue.active;
  const row = currentQueueRow();
  const pendingCount = queueEligibleRows().length;
  const target = Math.max(1, Number(dom.queueTargetInput.value || 20));
  const todayDone = contactedTodayCount();
  const pct = Math.min(100, Math.round((todayDone / target) * 100));
  dom.queueStartBtn.textContent = active ? "重新开始" : "开始队列";
  dom.queueCaption.textContent = active
    ? `当前队列剩余 ${formatNumber(Math.max(0, state.queue.ids.length - state.queue.index))} 个；今日已记录 ${formatNumber(todayDone)}/${formatNumber(target)}。`
    : `当前筛选下有 ${formatNumber(pendingCount)} 个可进入队列的候选。今日已记录 ${formatNumber(todayDone)}/${formatNumber(target)}。`;
  dom.queueCurrent.textContent = active ? queueProgressText(row) : `未开始 · 可处理 ${formatNumber(pendingCount)} 个`;
  dom.queueProgressFill.style.width = `${pct}%`;
  dom.queueOpenBtn.disabled = !row;
  dom.queueCopyBtn.disabled = !row;
  dom.queueSentNextBtn.disabled = !row;
  dom.queueSkipBtn.disabled = !row;
  dom.queueStopBtn.disabled = !active;
}

function renderCandidates() {
  const rows = filteredCandidates();
  if (!rows.length) {
    dom.candidateList.innerHTML = `<div class="empty-state"><strong>没有符合条件的候选</strong><span>调整筛选或导入 CSV。</span></div>`;
    return;
  }
  dom.candidateList.innerHTML = rows.map(renderCandidateCard).join("");
}

function partnershipStageLabel(stage) {
  return {
    none: "未开始",
    pricing: "报价确认",
    sample_pending: "待寄样",
    sample_sent: "已寄样",
    content_scheduled: "待发帖",
    posted: "已发帖",
    measured: "已复盘",
  }[stage || "none"] || stage || "未开始";
}

function sampleStatusLabel(status) {
  return {
    none: "未安排",
    requested: "已索要信息",
    prepared: "备货中",
    sent: "已发货",
    delivered: "已签收",
  }[status || "none"] || status || "未安排";
}

function videoProgressLabel(progress) {
  return {
    not_started: "未开始",
    product_confirming: "选品中",
    sample_sent: "已寄样",
    filming: "拍摄中",
    draft_review: "初稿待审",
    revision: "修改中",
    posted: "已发布",
    measured: "已复盘",
  }[progress || "not_started"] || progress || "未开始";
}

function campaignCost(row) {
  return Number(row.quoteJpy || 0) + Number(row.sampleCostJpy || 0);
}

function campaignRoi(row) {
  const cost = campaignCost(row);
  if (!cost) {
    return null;
  }
  return ((Number(row.revenueJpy || 0) - cost) / cost) * 100;
}

function partnershipCardChips(row) {
  const chips = [];
  if (row.partnershipStage && row.partnershipStage !== "none") {
    chips.push(partnershipStageLabel(row.partnershipStage));
  }
  if (row.postDate) {
    chips.push(`Post ${row.postDate}`);
  }
  if (row.videoProgress && row.videoProgress !== "not_started") {
    chips.push(videoProgressLabel(row.videoProgress));
  }
  if (row.orderNumber) {
    chips.push(`订单 ${row.orderNumber}`);
  }
  if (Number(row.orders || 0) > 0) {
    chips.push(`${formatNumber(row.orders)} orders`);
  }
  const roi = campaignRoi(row);
  if (roi !== null) {
    chips.push(`ROI ${formatSignedPercent(roi)}`);
  }
  return chips;
}

function renderCandidateCard(row) {
  const active = row.id === state.selectedId ? "is-active" : "";
  const label = state.payload.statusLabels[row.status] || row.status;
  const pinnedChip = row.pinned ? `<span class="mini-pill mini-pill--pinned">已置顶</span>` : "";
  const pinLabel = row.pinned ? "取消置顶" : "置顶";
  const pinClass = row.pinned ? "pin-button is-pinned" : "pin-button";
  const partnershipChips = partnershipCardChips(row)
    .map((chip) => `<span class="mini-pill">${escapeHtml(chip)}</span>`)
    .join("");
  return `
    <article class="candidate-card ${active}" data-id="${escapeHtml(row.id)}" data-status="${escapeHtml(row.status)}" data-tier="${escapeHtml(row.tier)}" data-pinned="${row.pinned ? "true" : "false"}">
      <div class="candidate-top">
        <div class="candidate-identity">
          ${renderCreatorAvatar(row)}
          <div class="candidate-main">
            <h3>@${escapeHtml(row.handle || row.name)}</h3>
            <p>${escapeHtml(row.name)} · ${escapeHtml(row.niche)} · ${escapeHtml(row.location)}</p>
          </div>
        </div>
        <div class="score-badge" data-tier="${escapeHtml(row.tier)}">${row.score}<small>${escapeHtml(row.tier)}</small></div>
      </div>
      <div class="candidate-meta">
        <span class="mini-pill">${formatCompact(row.followers)} followers</span>
        <span class="mini-pill">${Number(row.engagementRate || 0).toFixed(1)}% ER</span>
        <span class="mini-pill">${escapeHtml(label)}</span>
        <span class="mini-pill">${escapeHtml(row.contactMethod)}</span>
        ${pinnedChip}
        ${partnershipChips}
      </div>
      <div class="candidate-actions">
        <button type="button" data-action="select" data-id="${escapeHtml(row.id)}">查看</button>
        <button class="${pinClass}" type="button" data-action="pin" data-id="${escapeHtml(row.id)}" data-pinned="${row.pinned ? "true" : "false"}">${pinLabel}</button>
        <a href="${escapeHtml(row.instagramUrl)}" target="_blank" rel="noreferrer">IG</a>
        <button type="button" data-action="copy-dm" data-id="${escapeHtml(row.id)}">复制 DM</button>
        <button class="danger-text" type="button" data-action="delete" data-id="${escapeHtml(row.id)}">删除</button>
      </div>
    </article>
  `;
}

function selectedCandidate() {
  return (state.payload?.candidates || []).find((row) => row.id === state.selectedId) || null;
}

function renderDetail() {
  const row = selectedCandidate();
  renderHashtagAssistant();
  if (!row) {
    dom.detailTitle.textContent = "选择一个达人";
    dom.detailEmpty.hidden = false;
    dom.detailContent.hidden = true;
    return;
  }
  dom.detailTitle.textContent = `@${row.handle || row.name}`;
  dom.detailEmpty.hidden = true;
  dom.detailContent.hidden = false;
  renderDetailAvatar(row);
  dom.detailName.textContent = `${row.name || row.handle} · ${row.niche}`;
  dom.detailUrl.href = row.instagramUrl;
  dom.detailUrl.textContent = row.instagramUrl.replace("https://www.", "");
  dom.detailScore.textContent = row.score;
  dom.detailTier.textContent = row.tier;
  dom.detailFollowers.textContent = formatCompact(row.followers);
  dom.detailEr.textContent = `${Number(row.engagementRate || 0).toFixed(1)}%`;
  dom.detailStatus.value = row.status;
  dom.followupDate.value = row.followUpDate || "";
  renderInstagramEnrichStatus(row);
  if (state.profileCandidateId !== row.id) {
    state.profileCandidateId = row.id;
    state.profileSuggestion = null;
    dom.profileSource.value = "";
    state.copyHook = "";
    state.replyAnalysis = null;
    dom.copyHookInput.value = "";
    dom.replySource.value = "";
    renderReplyAssistant();
  }
  renderProfilePreview();
  renderScoreBreakdown(row);
  renderContactHistory(row);
  renderPartnershipTracker(row);
  dom.manualChecklist.innerHTML = row.manualChecklist
    .map(
      (item) => `
        <label class="check-item">
          <input type="checkbox">
          <span>${escapeHtml(item.label)}</span>
        </label>
      `,
    )
    .join("");
  renderDraft(row);
}

function instagramGraphSetup() {
  return state.payload?.integrations?.instagramGraph || {};
}

function renderInstagramEnrichStatus(row) {
  if (!dom.instagramEnrichBtn || !dom.instagramEnrichStatus) {
    return;
  }
  const setup = instagramGraphSetup();
  const hasHandle = Boolean(row?.handle);
  dom.instagramEnrichBtn.disabled = !hasHandle || !setup.configured || !setup.canEnrichCandidates;
  dom.instagramEnrichBtn.textContent = "Instagram API 补全";
  if (setup.mode === "instagram_login") {
    dom.instagramEnrichStatus.textContent = "当前是 Instagram Login token，只能读取授权账号自己；要补全达人候选池，请换 Facebook/Page token 并配置 META_IG_USER_ID。";
    return;
  }
  if (!hasHandle) {
    dom.instagramEnrichStatus.textContent = "当前达人缺少 Instagram handle，先补 handle 或主页链接。";
    return;
  }
  if (!setup.accessToken || !setup.ownUserId) {
    if (setup.mode === "instagram_login" && setup.accessToken) {
      dom.instagramEnrichStatus.textContent = "已配置 Instagram Login token：只能补授权账号自己，不能补其他达人。";
      return;
    }
    dom.instagramEnrichStatus.textContent = "未配置：在服务器 .env 填 META_ACCESS_TOKEN 和 META_IG_USER_ID 后重启服务。";
    return;
  }
  if (setup.mode === "instagram_login") {
    dom.instagramEnrichStatus.textContent = "已配置 Instagram Login token：只能补授权账号自己，不能补其他达人。";
    return;
  }
  dom.instagramEnrichStatus.textContent = `已配置 ${setup.version || "Graph API"}，可补全头像、粉丝数、简介和网站。`;
}

function renderScoreBreakdown(row) {
  const items = row.scoreBreakdownItems || [];
  dom.scoreBreakdown.innerHTML = items
    .map(
      (item) => `
        <div class="score-row">
          <span>${escapeHtml(item.label)}</span>
          <div class="score-track"><i class="score-fill" style="--pct: ${Number(item.pct || 0)}%;"></i></div>
          <strong>${Number(item.value || 0)}/${Number(item.max || 0)}</strong>
        </div>
      `,
    )
    .join("");
}

function renderContactHistory(row) {
  const history = row.contactHistory || [];
  if (!history.length) {
    dom.contactHistory.innerHTML = `<div class="history-item"><span>暂无联系记录</span><small>点击“记录建联”后会自动写入一条记录。</small></div>`;
    return;
  }
  dom.contactHistory.innerHTML = history
    .map(
      (item) => `
        <article class="history-item">
          <strong>${escapeHtml(historyTypeLabel(item.type))} · ${escapeHtml(item.date || "-")}</strong>
          <span>${escapeHtml(item.note || "-")}</span>
          <small>${item.followUpDate ? `下次跟进：${escapeHtml(item.followUpDate)}` : ""}</small>
        </article>
      `,
    )
    .join("");
}

function historyTypeLabel(type) {
  return {
    contacted: "建联",
    followup: "跟进",
    reply: "回复",
    note: "备注",
    price: "报价",
    sample: "寄样",
  }[type] || "记录";
}

function renderPartnershipTracker(row) {
  dom.partnershipInvitationSentAt.value = row.invitationSentAt || "";
  dom.partnershipConnectionAt.value = row.connectionAt || "";
  dom.partnershipBloggerId.value = row.bloggerId || row.handle || "";
  dom.partnershipCreatorType.value = row.creatorType || row.niche || "";
  dom.partnershipFollowers.value = row.followers || "";
  dom.partnershipProfileUrl.value = row.instagramUrl || "";
  dom.partnershipStage.value = row.partnershipStage || "none";
  dom.partnershipQuote.value = row.quoteJpy || "";
  dom.partnershipCollabProduct.value = row.collabProduct || "";
  dom.partnershipSampleStatus.value = row.sampleStatus || "none";
  dom.partnershipSampleCost.value = row.sampleCostJpy || "";
  dom.partnershipRecipientName.value = row.recipientName || "";
  dom.partnershipPostalCode.value = row.postalCode || "";
  dom.partnershipShippingAddress.value = row.shippingAddress || "";
  dom.partnershipPhoneNumber.value = row.phoneNumber || "";
  dom.partnershipOrderNumber.value = row.orderNumber || "";
  dom.partnershipTracking.value = row.shippingTracking || "";
  dom.partnershipShippedAt.value = row.shippedAt || "";
  dom.partnershipReceivedAt.value = row.receivedAt || "";
  dom.partnershipVideoProgress.value = row.videoProgress || "not_started";
  dom.partnershipPostDate.value = row.postDate || "";
  dom.partnershipPostUrl.value = row.postUrl || "";
  dom.partnershipCoupon.value = row.couponCode || "";
  dom.partnershipOrders.value = row.orders || "";
  dom.partnershipRevenue.value = row.revenueJpy || "";

  const cost = campaignCost(row);
  const revenue = Number(row.revenueJpy || 0);
  const roi = campaignRoi(row);
  const summary = [
    ["阶段", partnershipStageLabel(row.partnershipStage)],
    ["建联", row.connectionAt || row.invitationSentAt || "-"],
    ["粉丝", formatCompact(row.followers || 0)],
    ["类型", row.creatorType || row.niche || "-"],
    ["产品", row.collabProduct || "-"],
    ["样品", sampleStatusLabel(row.sampleStatus)],
    ["视频", videoProgressLabel(row.videoProgress)],
    ["总成本", formatCurrency(cost)],
    ["收入", formatCurrency(revenue)],
    ["ROI", roi === null ? "-" : formatSignedPercent(roi)],
  ];
  if (row.orderNumber) {
    summary.push(["订单", row.orderNumber]);
  }
  if (row.shippedAt || row.receivedAt) {
    summary.push(["物流", [row.shippedAt && `发 ${row.shippedAt}`, row.receivedAt && `收 ${row.receivedAt}`].filter(Boolean).join(" / ")]);
  }
  if (row.recipientName || row.postalCode || row.phoneNumber) {
    summary.push(["收货", [row.recipientName, row.postalCode, row.phoneNumber].filter(Boolean).join(" / ")]);
  }
  if (row.couponCode) {
    summary.push(["优惠码", row.couponCode]);
  }
  if (row.postUrl) {
    summary.push(["帖子", "已记录"]);
  }
  dom.partnershipSummary.innerHTML = summary
    .map(([label, value]) => `<span class="mini-pill">${escapeHtml(label)} · ${escapeHtml(value)}</span>`)
    .join("");
}

function currentPartnershipPayload(row) {
  return {
    ...row,
    invitationSentAt: dom.partnershipInvitationSentAt.value,
    connectionAt: dom.partnershipConnectionAt.value,
    bloggerId: dom.partnershipBloggerId.value.trim(),
    creatorType: dom.partnershipCreatorType.value.trim(),
    followers: Number(dom.partnershipFollowers.value || 0),
    instagramUrl: dom.partnershipProfileUrl.value.trim(),
    partnershipStage: dom.partnershipStage.value,
    quoteJpy: Number(dom.partnershipQuote.value || 0),
    collabProduct: dom.partnershipCollabProduct.value.trim(),
    sampleStatus: dom.partnershipSampleStatus.value,
    sampleCostJpy: Number(dom.partnershipSampleCost.value || 0),
    recipientName: dom.partnershipRecipientName.value.trim(),
    postalCode: dom.partnershipPostalCode.value.trim(),
    shippingAddress: dom.partnershipShippingAddress.value.trim(),
    phoneNumber: dom.partnershipPhoneNumber.value.trim(),
    orderNumber: dom.partnershipOrderNumber.value.trim(),
    shippingTracking: dom.partnershipTracking.value.trim(),
    shippedAt: dom.partnershipShippedAt.value,
    receivedAt: dom.partnershipReceivedAt.value,
    videoProgress: dom.partnershipVideoProgress.value,
    postDate: dom.partnershipPostDate.value,
    postUrl: dom.partnershipPostUrl.value.trim(),
    couponCode: dom.partnershipCoupon.value.trim(),
    orders: Number(dom.partnershipOrders.value || 0),
    revenueJpy: Number(dom.partnershipRevenue.value || 0),
  };
}

async function savePartnershipTracking() {
  const row = selectedCandidate();
  if (!row) {
    showToast("先选择一个达人");
    return;
  }
  try {
    const payload = currentPartnershipPayload(row);
    const result = await apiJson("/api/candidates", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.selectedId = result.candidate.id;
    await loadWorkspace({ silent: true });
    showToast("合作追踪已保存");
  } catch (error) {
    showToast(`合作追踪保存失败：${error.message}`);
  }
}

function analyzeCreatorReply(textValue, row) {
  const text = String(textValue || "").trim();
  if (!text) {
    return null;
  }
  const lower = text.toLowerCase();
  const rules = [
    {
      key: "rejected",
      label: "拒绝 / 暂不合作",
      status: "rejected",
      test: /難しい|見送り|できません|不可|忙しい|興味.*ない|今回は|すみません|ごめんなさい|not interested|decline|拒绝/i,
    },
    {
      key: "price",
      label: "报价 / 费用",
      status: "negotiating",
      test: /円|¥|料金|費用|単価|見積|お見積|rate|fee|price|报价|報酬/i,
    },
    {
      key: "product_request",
      label: "想看商品 / 图片",
      status: "replied",
      test: /商品|写真|画像|url|詳細|ラインナップ|どんな|product|image|素材/i,
    },
    {
      key: "condition",
      label: "询问条件",
      status: "replied",
      test: /条件|納期|投稿|二次利用|pr表記|スケジュール|いつ|形式|媒体|条件|timeline|usage/i,
    },
    {
      key: "interested",
      label: "有兴趣",
      status: "replied",
      test: /興味|ぜひ|可能|大丈夫|お願いします|検討|詳しく|前向き|ok|interested/i,
    },
  ];
  const matched = rules.find((rule) => rule.test.test(text) || rule.test.test(lower)) || {
    key: "needs_reply",
    label: "需要人工判断",
    status: "replied",
  };
  return {
    ...matched,
    draft: buildReplyDraft(row, matched.key, text),
    note: `达人回复识别：${matched.label}\n${text.slice(0, 300)}`,
  };
}

function buildReplyDraft(row, key, originalText) {
  const brand = state.payload?.brand?.name || "SOSOVE";
  const name = row.name || `@${row.handle}`;
  const product = selectedProduct(row);
  const productLabel = product?.label || "商品";
  const angle = clientProductAngle(row);
  if (key === "rejected") {
    return `${name}さん、ご返信ありがとうございます。\n\n承知いたしました。ご丁寧にお返事いただきありがとうございます。\nまたタイミングや企画内容が合いそうな機会がありましたら、改めてご相談させていただけますと幸いです。\n\n今後ともどうぞよろしくお願いいたします。`;
  }
  if (key === "price") {
    return `${name}さん、ご返信ありがとうございます。\n\n条件をご共有いただきありがとうございます。社内で確認いたしますので、念のため投稿形式、投稿本数、二次利用の可否、掲載期間、商品提供の扱いについても教えていただけますでしょうか。\n\n今回まずは${productLabel}（${angle}）での初回タイアップを想定しています。条件が合えば継続企画もご相談できればと思っております。`;
  }
  if (key === "product_request") {
    return `${name}さん、ご返信ありがとうございます。\n\nもちろんです。今回は${brand}の${productLabel}を中心に、${angle}をご紹介できればと考えています。\n商品画像、候補アイテム、条件の概要を整理してお送りします。\n\nご覧いただいたうえで、気になるアイテムや投稿しやすい形式があれば教えていただけますでしょうか。`;
  }
  if (key === "condition") {
    return `${name}さん、ご返信ありがとうございます。\n\n条件について、現時点では商品提供を含めたInstagramでのご紹介を想定しています。投稿内容は${name}さんの普段の雰囲気に合わせ、PR表記、投稿期限、二次利用の有無は事前に確認して進めたいです。\n\n対応可能な投稿形式と概算費用を教えていただけますでしょうか。`;
  }
  if (key === "interested") {
    return `${name}さん、ご返信ありがとうございます。ご興味を持っていただけて嬉しいです。\n\n今回は${brand}の${productLabel}（${angle}）をご紹介いただけないかと考えています。\nまずは候補商品と条件概要をお送りしますので、投稿しやすい形式やご希望条件があれば教えていただけますでしょうか。`;
  }
  return `${name}さん、ご返信ありがとうございます。\n\n内容確認いたしました。今回のご相談について、${brand}側で進め方を整理したうえでご返信いたします。\n念のため、対応可能な投稿形式、概算費用、商品提供の可否を教えていただけますでしょうか。`;
}

function renderReplyAssistant() {
  const analysis = state.replyAnalysis;
  if (!analysis) {
    dom.replyInsights.innerHTML = `<span class="profile-empty">回复识别结果会显示在这里</span>`;
    dom.replyDraft.textContent = "";
    dom.replyCopyBtn.disabled = true;
    dom.replyLogBtn.disabled = true;
    return;
  }
  dom.replyInsights.innerHTML = [
    ["类型", analysis.label],
    ["建议状态", state.payload?.statusLabels?.[analysis.status] || analysis.status],
    ["下一步", analysis.key === "price" ? "确认条件" : analysis.key === "rejected" ? "礼貌收尾" : "继续推进"],
    ["来源", analysis.configured ? `模型 ${analysis.model || ""}`.trim() : "本地规则"],
    Array.isArray(analysis.warnings) && analysis.warnings.length ? ["提示", analysis.warnings[0]] : null,
  ]
    .filter(Boolean)
    .map(([label, value]) => `<span class="mini-pill">${escapeHtml(label)} · ${escapeHtml(value)}</span>`)
    .join("");
  dom.replyDraft.textContent = analysis.draft;
  dom.replyCopyBtn.disabled = false;
  dom.replyLogBtn.disabled = false;
}

function initials(value) {
  const clean = String(value || "SO").trim();
  return clean.slice(0, 2).toUpperCase();
}

function renderDraft(row) {
  const drafts = row.drafts || {};
  document.querySelectorAll("[data-draft]").forEach((button) => {
    button.classList.toggle("is-active", state.copyMode === "default" && !state.templateKey && button.dataset.draft === state.activeDraft);
  });
  dom.templateSelect.value = state.templateKey;
  dom.productSelect.value = state.productKey;
  dom.copyToneSelect.value = state.copyTone;
  dom.copyLengthSelect.value = state.copyLength;
  dom.copyHookInput.value = state.copyHook;
  const modelSubject = state.copyMode === "model" && state.modelDraft?.candidateId === row.id ? state.modelDraft?.subject || "" : "";
  const templateSubject = state.templateKey ? fixedTemplateSubject(row, state.templateKey) : "";
  dom.emailSubjectRow.hidden = !(modelSubject || templateSubject || (state.copyMode === "default" && !state.templateKey && state.activeDraft === "email"));
  dom.emailSubject.textContent = modelSubject || templateSubject || drafts.emailSubject || "";
  dom.draftText.textContent = draftTextForMode(row);
  renderProductPoints(row);
  renderCopyInsights(row);
}

function draftTextForMode(row) {
  if (state.copyMode === "model" && state.modelDraft?.candidateId === row.id && state.modelDraft?.text) {
    return state.modelDraft.text;
  }
  if (isFixedTemplateKey(state.templateKey)) {
    return buildTemplateDraft(row, state.templateKey);
  }
  if (state.copyMode === "optimized") {
    return buildOptimizedDraft(row);
  }
  if (state.templateKey) {
    return buildTemplateDraft(row, state.templateKey);
  }
  const drafts = row.drafts || {};
  return drafts[state.activeDraft] || drafts.dm || "";
}

function templateName(key) {
  return {
    recommended: "自动推荐",
    product_seed: "商品提供",
    paid_post: "付费投稿",
    reels: "Reels 合作",
    affiliate: "折扣码 / 佣金",
    long_term: "长期合作",
    followup_second: "二次跟进",
    negotiate: "报价议价回复",
    fixed_paid_trial: "固定模板 1：有償ご試着",
    fixed_summer_collab: "固定模板 2：夏新作コラボ",
    fixed_monitor_offer: "固定模板 3：商品モニター",
    fixed_partner_recruit: "固定模板 4：発信パートナー",
  }[key] || "默认文案";
}

function creatorDisplayName(row) {
  return String(row.name || row.handle || "ご担当者").trim();
}

function creatorSalutation(row) {
  const name = creatorDisplayName(row);
  return /(?:様|さん|ちゃん|くん)$/u.test(name) ? name : `${name}様`;
}

function fixedTemplateSubject(row, key) {
  const name = creatorSalutation(row);
  return {
    fixed_paid_trial: "【SOSOVE - 有償ご試着】",
    fixed_summer_collab: `【SOSOVE】${name}へ 夏新作💰コラボのお願い`,
    fixed_monitor_offer: "【SOSOVE】💰ご提案／商品モニターのお願い",
    fixed_partner_recruit: `【SOSOVE】${name}へ　一緒に発信してくださる方へ`,
  }[key] || "";
}

function isFixedTemplateKey(key) {
  return Boolean(fixedTemplateSubject({}, key));
}

function recommendTemplateKey(row) {
  const blob = [row.niche, row.notes, ...(row.tags || []), ...(row.topPosts || [])].join(" ").toLowerCase();
  if (row.status === "negotiating") {
    return "negotiate";
  }
  if (row.status === "contacted" || row.followUpDate) {
    return "followup_second";
  }
  if (blob.includes("reel") || blob.includes("動画") || blob.includes("movie") || blob.includes("short")) {
    return "reels";
  }
  if ((row.followers || 0) >= 80000 || row.contactMethod === "creator_marketplace") {
    return "paid_post";
  }
  if (blob.includes("coupon") || blob.includes("クーポン") || blob.includes("affiliate")) {
    return "affiliate";
  }
  if ((row.score || 0) >= 82 && (row.engagementRate || 0) >= 4) {
    return "long_term";
  }
  return "product_seed";
}

function activeTemplateKey(row) {
  return state.templateKey && state.templateKey !== "recommended" ? state.templateKey : recommendTemplateKey(row);
}

function recommendationReason(row, key) {
  if (isFixedTemplateKey(key)) {
    return "使用你提供的固定建联模板，仅替换达人称呼";
  }
  if (key === "negotiate") {
    return "当前状态是报价中，优先使用议价回复";
  }
  if (key === "followup_second") {
    return "已有建联或跟进日期，优先使用二次跟进";
  }
  if (key === "reels") {
    return "标签或备注含视频/Reels 信号";
  }
  if (key === "paid_post") {
    return "粉丝量较高或来自 Creator Marketplace";
  }
  if (key === "affiliate") {
    return "资料中出现折扣码/佣金相关信号";
  }
  if (key === "long_term") {
    return "评分和互动较强，适合尝试长期合作";
  }
  return "适合先用低门槛商品提供建立合作";
}

function clientProductAngle(row) {
  const product = selectedProduct(row);
  if (product) {
    return product.angle;
  }
  const blob = [row.niche, ...(row.tags || []), ...(row.topPosts || [])].join(" ");
  if (blob.includes("低身長")) {
    return "低身長でもバランスを取りやすいワンピースや高腰パンツ";
  }
  if (blob.includes("オフィス") || blob.includes("通勤")) {
    return "通勤にも使いやすいきれいめカジュアル";
  }
  if (blob.includes("ママ") || blob.includes("体型")) {
    return "体型カバーしやすく日常で着回せるアイテム";
  }
  return "大人向けの着回ししやすい新作アイテム";
}

function productLibrary() {
  return {
    onepiece: {
      label: "通勤连衣裙",
      angle: "通勤にも休日にも使いやすいワンピース",
      points: ["一枚でコーデが完成", "きれいめに見える", "写真でシルエットが伝わりやすい"],
    },
    outer: {
      label: "轻外套 / 西装外套",
      angle: "羽織るだけできちんと見えする軽アウター",
      points: ["通勤に合わせやすい", "季節の変わり目に提案しやすい", "着回し投稿に向く"],
    },
    office_set: {
      label: "通勤套装",
      angle: "忙しい朝にも使いやすいオフィス向けセットアップ",
      points: ["上下別でも着回せる", "仕事服提案に自然", "大人女性の実用感がある"],
    },
    petite: {
      label: "小个子友好款",
      angle: "低身長でもバランスを取りやすいアイテム",
      points: ["丈感を訴求しやすい", "150cm台コーデと相性が良い", "比較投稿に向く"],
    },
    body_cover: {
      label: "体型遮盖款",
      angle: "体型カバーしやすく日常で着回せるアイテム",
      points: ["安心感を伝えやすい", "ママコーデと相性が良い", "購入理由に直結しやすい"],
    },
    pants_skirt: {
      label: "高腰裤 / 半裙",
      angle: "脚長見えしやすい高腰ボトムス",
      points: ["低身長にも提案しやすい", "着回し投稿に向く", "トップス比較が作りやすい"],
    },
    knit: {
      label: "针织 / 日常上衣",
      angle: "普段のコーデに取り入れやすいニットやトップス",
      points: ["商品提供の初回に向く", "季節感を出しやすい", "複数色提案しやすい"],
    },
  };
}

function recommendProductKey(row) {
  const blob = [row.niche, row.notes, ...(row.tags || []), ...(row.topPosts || [])].join(" ");
  if (/低身長|150cm|151cm|152cm|153cm|154cm|155cm|小柄/.test(blob)) {
    return "petite";
  }
  if (/体型|カバー|ママ|産後|腰回り/.test(blob)) {
    return "body_cover";
  }
  if (/オフィス|通勤|仕事|きれいめ/.test(blob)) {
    return (row.followers || 0) > 50000 ? "office_set" : "onepiece";
  }
  if (/ジャケット|アウター|羽織/.test(blob)) {
    return "outer";
  }
  if (/脚長|パンツ|スカート|高腰/.test(blob)) {
    return "pants_skirt";
  }
  return "knit";
}

function selectedProduct(row) {
  const key = state.productKey === "auto" ? recommendProductKey(row) : state.productKey;
  return productLibrary()[key] || null;
}

function renderProductPoints(row) {
  const product = selectedProduct(row);
  if (!product) {
    dom.productPoints.innerHTML = "";
    return;
  }
  dom.productPoints.innerHTML = [
    ["产品", product.label],
    ...product.points.map((point) => ["卖点", point]),
  ]
    .map(([label, value]) => `<span class="mini-pill">${escapeHtml(label)} · ${escapeHtml(value)}</span>`)
    .join("");
}

function creatorHook(row) {
  if (state.copyHook.trim()) {
    return state.copyHook.trim();
  }
  const post = (row.topPosts || [])[0];
  if (post) {
    return `特に「${post}」の見せ方が自然で、`;
  }
  if (row.notes) {
    const firstNote = String(row.notes).split(/\n|。/).find(Boolean) || "";
    if (firstNote.length >= 8) {
      return `${firstNote.slice(0, 48)}という点が印象的で、`;
    }
  }
  return `${row.niche || "ファッション"}の投稿の雰囲気が自然で、`;
}

function tonePhrase() {
  return {
    warm: {
      opener: "突然のご連絡失礼します。",
      close: "ご負担のない範囲でご確認いただけましたら嬉しいです。よろしくお願いいたします。",
      ask: "一度ご相談できますでしょうか。",
    },
    polite: {
      opener: "突然のご連絡にて失礼いたします。",
      close: "ご検討いただけますと幸いです。何卒よろしくお願いいたします。",
      ask: "ご相談の機会をいただくことは可能でしょうか。",
    },
    concise: {
      opener: "はじめまして。",
      close: "ご興味があればご返信ください。よろしくお願いいたします。",
      ask: "ご相談できますでしょうか。",
    },
  }[state.copyTone] || {
    opener: "突然のご連絡失礼します。",
    close: "ご確認いただけましたら幸いです。よろしくお願いいたします。",
    ask: "一度ご相談できますでしょうか。",
  };
}

function buildOptimizedDraft(row) {
  const key = activeTemplateKey(row);
  const brand = state.payload?.brand?.name || "SOSOVE";
  const name = row.name || `@${row.handle}`;
  const style = row.niche || "ファッション";
  const angle = clientProductAngle(row);
  const product = selectedProduct(row);
  const productPointText = product?.points?.length ? `特に、${product.points.slice(0, 2).join("、")}点を自然に伝えやすいと考えています。\n` : "";
  const hook = creatorHook(row);
  const tone = tonePhrase();
  const intro = `${name}さん、${tone.opener}\n${brand} のPR担当です。`;
  const context = `${hook}${brand} の${angle}と相性が良いと感じました。`;
  const lightAsk = "まずは商品提供を中心に、普段の投稿の雰囲気に合わせた自然なご紹介をご相談できればと思っています。";
  const paidAsk = "フィード投稿、ストーリーズ、またはリールでのタイアップを検討しています。対応可能な形式、概算費用、二次利用の可否を教えていただけますでしょうか。";
  const reelsAsk = "着用感や着回しが伝わる短尺動画でのご紹介をご相談できればと思っています。撮影可能な構成や条件を伺えますでしょうか。";
  const affiliateAsk = "商品提供に加えて、専用クーポンコードや成果報酬型のご紹介もご相談できればと思っています。対応可否と希望条件を教えていただけますでしょうか。";
  const longTermAsk = "単発だけでなく、季節ごとの新作や着回し企画も含めて継続的にご相談できれば嬉しいです。長期でのタイアップにご興味はありますでしょうか。";
  const followupAsk = `先日 ${brand} のPR相談でご連絡した件で、念のため再度ご連絡しました。ご興味がなければご返信不要です。条件確認だけでも可能でしたら、投稿形式とご料金の目安を伺えますと幸いです。`;
  const negotiateAsk = "条件を共有いただきありがとうございます。初回のお取り組みとして、商品提供を含めた形で少し予算を調整できないか検討しています。ストーリーズ中心、または投稿内容を軽めにしたプランで再度お見積りいただくことは可能でしょうか。";
  const askByKey = {
    product_seed: lightAsk,
    paid_post: paidAsk,
    reels: reelsAsk,
    affiliate: affiliateAsk,
    long_term: longTermAsk,
    followup_second: followupAsk,
    negotiate: negotiateAsk,
  };
  if (key === "followup_second") {
    return `${name}さん、こんにちは。\n\n${askByKey[key]}\n\n${tone.close}`;
  }
  if (key === "negotiate") {
    return `${name}さん\n\n${askByKey[key]}\n\n反応を見ながら継続企画もご相談できればと思っています。${tone.close}`;
  }
  const middle = askByKey[key] || lightAsk;
  if (state.copyLength === "short") {
    return `${intro}\n\n${context}\n${middle}\n\n${tone.close}`;
  }
  if (state.copyLength === "detailed") {
    return (
      `${intro}\n\n${style}に関する投稿を拝見し、${context}\n\n` +
      `${brand} は日本向けのレディースファッションブランドで、通勤、休日、体型カバー、きれいめカジュアルに合わせやすいアイテムを扱っています。\n\n` +
      `${productPointText}${middle}\n投稿内容は無理に指定せず、${name}さんの普段の雰囲気に合わせた形で進められれば嬉しいです。\n\n${tone.close}`
    );
  }
  return (
    `${intro}\n\n${style}の投稿を拝見し、${context}\n\n` +
    `${productPointText}${middle}\n投稿内容は無理に指定せず、${name}さんの普段の雰囲気に合わせた形で進められれば嬉しいです。\n\n${tone.close}`
  );
}

function buildTemplateDraft(row, key) {
  const brand = state.payload?.brand?.name || "SOSOVE";
  const name = row.name || `@${row.handle}`;
  const creatorName = creatorSalutation(row);
  const angle = clientProductAngle(row);
  const style = row.niche || "ファッション";
  const commonIntro = `${name}さん、はじめまして。${brand} のPR担当です。`;
  const templates = {
    fixed_paid_trial:
      `${creatorName} \n\n` +
      "SosoveのPR、Annie Leeと申します。\n\n" +
      `Sosoveはレディースファッションを展開しており、${creatorName}のご投稿を拝見させていただきました。ファッションセンスがすっごく素晴らしいと思います。\n` +
      `${creatorName}とのコラボをご提案したくご連絡いたします。\n\n` +
      "💰、及び無料サンプルを提供いたします。\n\n" +
      "ご検討のほど、どうぞよろしくお願い申し上げます。",
    fixed_summer_collab:
      `${creatorName} \n\n` +
      "SosoveのPR、Annieと申します。\n\n" +
      `Sosoveはレディースファッションを展開しており、${creatorName}のご投稿を拝見させていただきました。ファッションのセンスがすっごく素晴らしいと思います。\n` +
      `${creatorName}とのコラボをご提案したくご連絡いたします。\n\n` +
      "💰、及び無料サンプルを提供いたします。\n\n" +
      "ご検討のほど、どうぞよろしくお願い申し上げます。",
    fixed_monitor_offer:
      `${creatorName}\n\n` +
      "SOSOVEのPR-Annieです。\n\n" +
      `SOSOVEはレディースファッションブランドを扱っております。${creatorName}の投稿を拝見し、その美しさと女性らしいコーデのセンスがとても素敵だなと感じました。\n\n` +
      `そこで、ぜひ${creatorName}とコラボできればと思い、ご連絡させていただきました。\n\n` +
      "お礼💰と無料サンプルをご提供いたします。\n\n" +
      "ご検討いただけますと幸いです。よろしくお願いいたします。",
    fixed_partner_recruit:
      `${creatorName}、突然のDM失礼します。\n\n` +
      "SOSOVEのAnnieです。\n\n" +
      "現在、春夏の新作アイテムを実際に使いながら、SNSでご紹介してくださるパートナーを募集しています。\n\n" +
      "ご提供する商品は無料です。さらに、投稿ごとに報酬をお支払いします。\n\n" +
      `${creatorName}の自然な雰囲気や暮らしに合わせて、自由に発信していただけると嬉しいです。\n\n` +
      "もしご興味ありましたら、ぜひご一報ください💕",
    product_seed:
      `${commonIntro}\n\n${style}の投稿を拝見し、${brand} の${angle}と相性が良いと感じました。\n\n` +
      "まずは商品提供ベースで、普段の投稿の雰囲気に合わせたご紹介をご相談できれば嬉しいです。投稿内容は無理に指定せず、実際に着ていただいた自然な感想を大切にしたいです。\n\n" +
      "ご興味があれば、送付先やご希望アイテムについて一度ご相談できますでしょうか。",
    paid_post:
      `${commonIntro}\n\n${style}の投稿の見せ方がとても自然で、${brand} の${angle}をご紹介いただけないかと思いご連絡しました。\n\n` +
      "フィード投稿またはストーリーズでの有償タイアップを検討しています。対応可能な投稿形式、概算費用、二次利用の可否、投稿までのスケジュールを教えていただけますでしょうか。\n\n" +
      "条件が合えば、商品提供と合わせて進められればと思います。",
    reels:
      `${commonIntro}\n\n${brand} の${angle}を、着回しや着用感が伝わる Reels でご紹介いただけないかと思いご連絡しました。\n\n` +
      "短尺動画での対応可否、概算費用、撮影可能な構成、二次利用条件を教えていただけますでしょうか。${name}さんの普段の雰囲気を活かした自然な内容を希望しています。",
    affiliate:
      `${commonIntro}\n\n${style}の投稿を拝見し、${brand} のお客様層と近いと感じました。\n\n` +
      "商品提供に加えて、専用クーポンコードまたは成果報酬型のご紹介をご相談できればと思っています。条件確認だけでも可能でしたら、対応可否と希望条件を教えていただけますでしょうか。",
    long_term:
      `${commonIntro}\n\n${brand} では、日本向けの大人カジュアルを継続的にご紹介いただけるパートナーを探しています。\n\n` +
      `${name}さんの${style}の雰囲気がブランドと合うと感じ、単発ではなく季節ごとの新作紹介や着回し企画も含めてご相談できれば嬉しいです。\n\n` +
      "長期でのタイアップにご興味があれば、対応可能な形式と条件を伺えますでしょうか。",
    followup_second:
      `${name}さん、先日 ${brand} のPR相談でご連絡した件で、念のため再度ご連絡しました。\n\n` +
      "ご興味がなければご返信不要です。もし条件確認だけでも可能でしたら、投稿形式とご料金の目安を伺えますと幸いです。",
    negotiate:
      `${name}さん、ご返信ありがとうございます。条件を共有いただき大変助かります。\n\n` +
      "今回まずは初回の取り組みとして、商品提供を含めた形で少し予算を調整できないか検討しています。可能でしたら、ストーリーズ中心、または投稿内容を軽めにしたプランで再度お見積りいただくことはできますでしょうか。\n\n" +
      "条件が合えば、反応を見ながら継続企画もご相談できればと思っています。",
  };
  return templates[key] || row.drafts?.dm || "";
}

function renderCopyInsights(row) {
  const selectedKey = activeTemplateKey(row);
  const product = selectedProduct(row);
  const textValue = dom.draftText.textContent || "";
  const checks = [
    ["推荐", templateName(selectedKey)],
    ["产品", product?.label || "未选"],
    ["原因", recommendationReason(row, selectedKey)],
    ["钩子", state.copyHook.trim() || (row.topPosts || [])[0] || row.notes ? "已有" : "偏泛"],
    ["CTA", /教えて|ご相談|返信|伺え|可能/.test(textValue) ? "明确" : "偏弱"],
    ["长度", `${textValue.length}字`],
  ];
  dom.copyInsights.innerHTML = checks
    .map(([label, value]) => `<span class="mini-pill">${escapeHtml(label)} · ${escapeHtml(value)}</span>`)
    .join("");
}

function loadCopyModelSettings() {
  try {
    const saved = JSON.parse(localStorage.getItem("outreachCopyModel") || "{}");
    state.copyModelProvider = saved.provider || "local";
    state.copyModelBaseUrl = saved.baseUrl || "";
    state.copyModelName = saved.model || "";
    state.copyModelAuthMode = saved.authMode || "bearer";
    state.copyModelSaveKey = Boolean(saved.saveKey);
    state.copyModelApiKey = saved.saveKey ? saved.apiKey || "" : "";
  } catch {
    state.copyModelProvider = "local";
    state.copyModelBaseUrl = "";
    state.copyModelName = "";
    state.copyModelAuthMode = "bearer";
    state.copyModelApiKey = "";
    state.copyModelSaveKey = false;
  }
  dom.copyModelProvider.value = state.copyModelProvider;
  dom.copyModelBaseUrl.value = state.copyModelBaseUrl;
  dom.copyModelName.value = state.copyModelName;
  dom.copyModelAuthMode.value = state.copyModelAuthMode;
  dom.copyModelApiKey.value = state.copyModelApiKey;
  dom.copyModelSaveKey.checked = state.copyModelSaveKey;
  updateCopyModelStatus();
}

function saveCopyModelSettings() {
  state.copyModelProvider = dom.copyModelProvider.value || "local";
  state.copyModelBaseUrl = dom.copyModelBaseUrl.value.trim();
  state.copyModelName = dom.copyModelName.value.trim();
  state.copyModelAuthMode = dom.copyModelAuthMode.value || "bearer";
  state.copyModelApiKey = dom.copyModelApiKey.value.trim();
  state.copyModelSaveKey = dom.copyModelSaveKey.checked;
  localStorage.setItem(
    "outreachCopyModel",
    JSON.stringify({
      provider: state.copyModelProvider,
      baseUrl: state.copyModelBaseUrl,
      model: state.copyModelName,
      authMode: state.copyModelAuthMode,
      saveKey: state.copyModelSaveKey,
      apiKey: state.copyModelSaveKey ? state.copyModelApiKey : "",
    }),
  );
  updateCopyModelStatus();
}

function updateCopyModelStatus(message = "") {
  if (message) {
    dom.copyModelStatus.textContent = message;
    return;
  }
  if (state.copyModelProvider !== "api") {
    if (state.copyModelProvider === "cpa") {
      if (!state.copyModelBaseUrl || !state.copyModelName) {
        dom.copyModelStatus.textContent = "CPA 待填写";
        return;
      }
      dom.copyModelStatus.textContent = state.copyModelSaveKey && state.copyModelApiKey ? "CPA 已保存" : "CPA 已填写";
      return;
    }
    dom.copyModelStatus.textContent = "本地规则";
    return;
  }
  if (!state.copyModelBaseUrl || !state.copyModelName) {
    dom.copyModelStatus.textContent = "待填写 API";
    return;
  }
  dom.copyModelStatus.textContent = state.copyModelSaveKey && state.copyModelApiKey ? "API 已保存" : "API 已填写";
}

function clearCopyModelSettings() {
  localStorage.removeItem("outreachCopyModel");
  state.copyModelProvider = "local";
  state.copyModelBaseUrl = "";
  state.copyModelName = "";
  state.copyModelAuthMode = "bearer";
  state.copyModelApiKey = "";
  state.copyModelSaveKey = false;
  dom.copyModelProvider.value = "local";
  dom.copyModelBaseUrl.value = "";
  dom.copyModelName.value = "";
  dom.copyModelAuthMode.value = "bearer";
  dom.copyModelApiKey.value = "";
  dom.copyModelSaveKey.checked = false;
  updateCopyModelStatus("配置已清空");
}

function activeModelProvider() {
  return state.copyModelProvider === "cpa" ? "cpa" : state.copyModelProvider === "api" ? "api" : "local";
}

async function testCopyModelSettings() {
  saveCopyModelSettings();
  const provider = activeModelProvider();
  if (provider === "local") {
    updateCopyModelStatus("当前为本地规则");
    showToast("当前使用本地规则，不需要测试 API");
    return;
  }
  dom.copyModelTestBtn.disabled = true;
  updateCopyModelStatus("测试中...");
  try {
    const result = await apiJson("/api/copy/test", {
      method: "POST",
      body: JSON.stringify({
        provider,
        apiBaseUrl: state.copyModelBaseUrl,
        model: state.copyModelName,
        authMode: state.copyModelAuthMode,
        apiKey: dom.copyModelApiKey.value.trim(),
      }),
    });
    if (!result.ok) {
      throw new Error(result.error || "测试失败");
    }
    updateCopyModelStatus(`测试通过：${result.model || state.copyModelName}`);
    showToast("AI 接口测试通过");
  } catch (error) {
    updateCopyModelStatus("测试失败");
    showToast(`AI 接口测试失败：${error.message}`);
  } finally {
    dom.copyModelTestBtn.disabled = false;
  }
}

function selectedCopyOptions(row) {
  const product = selectedProduct(row);
  return {
    draftType: state.activeDraft,
    scenario: activeTemplateKey(row),
    tone: state.copyTone,
    length: state.copyLength,
    hook: state.copyHook.trim(),
    productKey: state.productKey,
    productLabel: product?.label || "",
    productAngle: product?.angle || clientProductAngle(row),
    productPoints: product?.points || [],
  };
}

async function generateModelDraft() {
  const row = selectedCandidate();
  if (!row) {
    showToast("先选择一个达人");
    return;
  }
  saveCopyModelSettings();
  const provider = activeModelProvider();
  dom.copyModelBtn.disabled = true;
  updateCopyModelStatus(provider !== "local" ? "模型生成中..." : "本地生成中...");
  try {
    const result = await apiJson("/api/copy/generate", {
      method: "POST",
      body: JSON.stringify({
        provider,
        apiBaseUrl: state.copyModelBaseUrl,
        model: state.copyModelName,
        authMode: state.copyModelAuthMode,
        apiKey: dom.copyModelApiKey.value.trim(),
        candidate: row,
        options: selectedCopyOptions(row),
      }),
    });
    if (!result.ok) {
      throw new Error(result.error || "生成失败");
    }
    state.modelDraft = { ...result, candidateId: row.id };
    state.copyMode = "model";
    dom.emailSubjectRow.hidden = !result.subject;
    dom.emailSubject.textContent = result.subject || "";
    dom.draftText.textContent = result.text || "";
    renderCopyInsights(row);
    const warning = Array.isArray(result.warnings) && result.warnings.length ? `；${result.warnings[0]}` : "";
    updateCopyModelStatus(result.configured ? `模型已生成：${result.model || "API"}` : "已用本地规则生成");
    showToast(`${result.configured ? "模型文案" : "本地文案"}已生成${warning}`);
  } catch (error) {
    updateCopyModelStatus("生成失败");
    showToast(`模型生成失败：${error.message}`);
  } finally {
    dom.copyModelBtn.disabled = false;
  }
}

async function generateModelReply() {
  const row = selectedCandidate();
  if (!row) {
    showToast("先选择一个达人");
    return;
  }
  const replyText = dom.replySource.value.trim();
  if (!replyText) {
    showToast("先粘贴达人回复");
    return;
  }
  saveCopyModelSettings();
  const provider = activeModelProvider();
  dom.replyModelBtn.disabled = true;
  dom.replyModelBtn.textContent = provider === "local" ? "本地生成中..." : "模型生成中...";
  try {
    const result = await apiJson("/api/reply/generate", {
      method: "POST",
      body: JSON.stringify({
        provider,
        apiBaseUrl: state.copyModelBaseUrl,
        model: state.copyModelName,
        authMode: state.copyModelAuthMode,
        apiKey: dom.copyModelApiKey.value.trim(),
        candidate: row,
        replyText,
      }),
    });
    if (!result.ok) {
      throw new Error(result.error || "生成失败");
    }
    state.replyAnalysis = {
      key: result.key,
      label: result.label,
      status: result.status,
      draft: result.draft,
      note: result.note,
      configured: Boolean(result.configured),
      model: result.model || "",
      warnings: result.warnings || [],
    };
    renderReplyAssistant();
    const warning = Array.isArray(result.warnings) && result.warnings.length ? `；${result.warnings[0]}` : "";
    showToast(`${result.configured ? "模型回复" : "本地回复"}已生成${warning}`);
  } catch (error) {
    showToast(`模型回复生成失败：${error.message}`);
  } finally {
    dom.replyModelBtn.disabled = false;
    dom.replyModelBtn.textContent = "模型生成回复";
  }
}

function applyRecommendedCopySettings(row) {
  state.templateKey = recommendTemplateKey(row);
  state.copyTone = row.contactMethod === "creator_marketplace" || (row.followers || 0) >= 80000 ? "polite" : "warm";
  state.copyLength = state.templateKey === "paid_post" || state.templateKey === "long_term" ? "detailed" : "standard";
  state.copyMode = "optimized";
}

function clearProfileSuggestion() {
  state.profileSuggestion = null;
  dom.profilePreview.innerHTML = "";
  dom.profileApplyBtn.disabled = true;
}

function renderProfilePreview() {
  const suggestion = state.profileSuggestion;
  if (!suggestion) {
    dom.profilePreview.innerHTML = `<span class="profile-empty">暂无识别结果</span>`;
    dom.profileApplyBtn.disabled = true;
    return;
  }
  const chips = [
    suggestion.email ? ["Email", suggestion.email] : null,
    suggestion.followers ? ["粉丝", formatCompact(suggestion.followers)] : null,
    suggestion.engagementRate ? ["互动率", `${suggestion.engagementRate}%`] : null,
    suggestion.avatarUrl ? ["头像", "已识别"] : null,
    suggestion.location ? ["地区", suggestion.location] : null,
    suggestion.niche ? ["赛道", suggestion.niche] : null,
    suggestion.tags?.length ? ["标签", suggestion.tags.join("、")] : null,
  ].filter(Boolean);
  dom.profilePreview.innerHTML = chips.length
    ? chips.map(([label, value]) => `<span class="mini-pill">${escapeHtml(label)} · ${escapeHtml(value)}</span>`).join("")
    : `<span class="profile-empty">没有识别到可补全字段</span>`;
  dom.profileApplyBtn.disabled = !chips.length;
}

function renderSource() {
  const source = state.payload.source;
  dom.sourceCaption.textContent = source.sampleMode
    ? "当前显示样例候选，保存或导入后会写入本地 JSON"
    : `本地文件：${source.candidatePath}`;
}

async function copyText(text, successMessage, sourceElement = null) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(successMessage);
  } catch {
    if (fallbackCopyText(text)) {
      showToast(successMessage);
      return;
    }
    if (sourceElement && selectElementText(sourceElement)) {
      showToast("复制被阻止，已选中文案，可按 Ctrl+C");
      return;
    }
    showToast("复制被浏览器阻止，文案已保留在右侧");
  }
}

function fallbackCopyText(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  textarea.style.top = "0";
  document.body.appendChild(textarea);
  textarea.select();
  let copied = false;
  try {
    copied = document.execCommand("copy");
  } catch {
    copied = false;
  }
  textarea.remove();
  return copied;
}

function selectElementText(element) {
  const selection = window.getSelection();
  if (!selection || !element) {
    return false;
  }
  const range = document.createRange();
  range.selectNodeContents(element);
  selection.removeAllRanges();
  selection.addRange(range);
  return true;
}

function buildGoogleSearch(keyword, signal) {
  const query = `site:instagram.com "${keyword}" "${signal}"`;
  return `https://www.google.com/search?q=${encodeURIComponent(query)}`;
}

function publicSearchKeyword() {
  const lines = dom.publicSearchKeyword.value
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  if (lines.length > 1) {
    return `site:instagram.com (${lines.map((line) => `"${line}"`).join(" OR ")})`;
  }
  return lines[0] || "fashion blogger japan";
}

function publicSearchQuery(keyword) {
  return keyword.toLowerCase().includes("site:instagram.com") ? keyword : `site:instagram.com "${keyword}"`;
}

function renderPublicSearchLink() {
  const query = publicSearchQuery(publicSearchKeyword());
  dom.publicSearchOpenLink.href = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
}

function skillHarvestPayload() {
  return {
    sourceMode: dom.skillSourceMode.value,
    market: dom.skillMarket.value.trim() || "Japan",
    language: dom.skillLanguage.value.trim() || "日语",
    niche: dom.skillNiche.value.trim() || "レディースファッション、40代コーデ、服",
    minFollowers: Number(dom.skillMinFollowers.value || 10000),
    maxFollowers: Number(dom.skillMaxFollowers.value || 100000),
    perTermLimit: Number(dom.skillPerTermLimit.value || 80),
    rawTarget: Number(dom.skillRawTarget.value || 200),
    topTarget: Number(dom.skillTopTarget.value || 50),
    seedTerms: dom.skillSeeds.value,
    exclusionRules: dom.skillExclusions.value,
    fullAngle: dom.skillFullAngle.checked,
    strictFilter: dom.skillStrictFilter.checked,
  };
}

function renderSkillPanel() {
  if (!dom.skillRunList || !state.payload) {
    return;
  }
  if (!dom.skillSeeds.dataset.ready) {
    const defaults = state.payload.skillPanel?.defaultSeeds || [];
    if (defaults.length && !dom.skillSeeds.value.trim()) {
      dom.skillSeeds.value = defaults.join("\n");
    }
    dom.skillSeeds.dataset.ready = "1";
  }
  if (!dom.skillExclusions.dataset.ready) {
    const defaults = state.payload.skillPanel?.defaultExclusions || [];
    if (defaults.length && !dom.skillExclusions.value.trim()) {
      dom.skillExclusions.value = defaults.join("\n");
    }
    dom.skillExclusions.dataset.ready = "1";
  }
  if (state.skillPrompt && dom.skillPromptOutput.value !== state.skillPrompt) {
    dom.skillPromptOutput.value = state.skillPrompt;
  }
  const panel = state.payload.skillPanel || {};
  const runs = panel.runs || [];
  if (!runs.length) {
    dom.skillRunList.innerHTML = `<div class="skill-run-empty">还没有可续跑抓取文件</div>`;
    return;
  }
  dom.skillRunList.innerHTML = runs
    .map((run) => {
      const counts = Object.entries(run.statusCounts || {})
        .map(([label, value]) => `${label}:${value}`)
        .join(" / ") || "pending";
      const runHint =
        (run.rawRows || 0) > 0
          ? "正在累计可见候选，可刷新查看最新进度"
          : "已创建计划，尚未开始浏览器抓取；复制提示词发给 Codex 后才会写入 raw";
      return `
        <article class="skill-run-row">
          <div class="skill-run-row-head">
            <strong>${escapeHtml(run.runId)}</strong>
            <button class="skill-run-delete" type="button" data-skill-run-delete="${escapeHtml(run.runId)}">删除</button>
          </div>
          <span>raw ${formatNumber(run.rawRows || 0)} / unique ${formatNumber(run.uniqueHandles || 0)} / steps ${formatNumber(run.progressRows || 0)}</span>
          <small>${escapeHtml(runHint)}</small>
          <small>${escapeHtml(counts)}</small>
          <small>${escapeHtml(run.rawPath || run.progressPath || "")}</small>
        </article>
      `;
    })
    .join("");
}

async function generateSkillPrompt() {
  dom.skillGeneratePromptBtn.disabled = true;
  dom.skillPanelStatus.textContent = "正在生成提示词...";
  try {
    const result = await apiJson("/api/skill/prompt", {
      method: "POST",
      body: JSON.stringify(skillHarvestPayload()),
    });
    state.skillPrompt = result.prompt || "";
    dom.skillPromptOutput.value = state.skillPrompt;
    dom.skillPanelStatus.textContent = "提示词已生成。下一步点“复制提示词”，发给 Codex 后才会开始控制浏览器抓取。";
    showToast("Skill 抓取提示词已生成");
  } catch (error) {
    dom.skillPanelStatus.textContent = `提示词生成失败：${error.message}`;
    showToast(`提示词生成失败：${error.message}`);
  } finally {
    dom.skillGeneratePromptBtn.disabled = false;
  }
}

async function createSkillPlan() {
  dom.skillCreatePlanBtn.disabled = true;
  dom.skillPanelStatus.textContent = "正在创建 plan/progress/raw CSV...";
  try {
    const result = await apiJson("/api/skill/plan", {
      method: "POST",
      body: JSON.stringify(skillHarvestPayload()),
    });
    state.skillPrompt = result.prompt || "";
    dom.skillPromptOutput.value = state.skillPrompt;
    if (state.payload) {
      state.payload.skillPanel = result.skillPanel;
    }
    renderSkillPanel();
    dom.skillPanelStatus.textContent = `已创建计划：${result.runId}。当前不会自动抓取；请点“复制提示词”发给 Codex，我收到后才会继续控制浏览器采集。`;
    showToast("抓取计划已创建，尚未开始浏览器采集");
  } catch (error) {
    dom.skillPanelStatus.textContent = `创建失败：${error.message}`;
    showToast(`创建失败：${error.message}`);
  } finally {
    dom.skillCreatePlanBtn.disabled = false;
  }
}

async function deleteSkillRun(runId) {
  const cleanRunId = String(runId || "").trim();
  if (!cleanRunId) {
    return;
  }
  const confirmed = window.confirm(`确认删除抓取计划 ${cleanRunId} 吗？\n\n会删除对应的 plan / progress / raw CSV，不会删除达人候选池。`);
  if (!confirmed) {
    return;
  }
  try {
    const result = await apiJson("/api/skill/run/delete", {
      method: "POST",
      body: JSON.stringify({ runId: cleanRunId }),
    });
    if (state.payload) {
      state.payload.skillPanel = result.skillPanel;
    }
    renderSkillPanel();
    showToast(`已删除抓取计划：${cleanRunId}`);
  } catch (error) {
    showToast(`删除抓取计划失败：${error.message}`);
  }
}

function defaultFollowUpDate(days = 3) {
  const next = new Date();
  next.setDate(next.getDate() + days);
  return localDateKey(next);
}

function parseSocialCount(value, unit = "") {
  const number = Number(String(value || "").replace(/,/g, ""));
  if (!Number.isFinite(number)) {
    return 0;
  }
  const normalizedUnit = String(unit || "").toLowerCase();
  if (normalizedUnit === "万" || normalizedUnit === "w") {
    return Math.round(number * 10000);
  }
  if (normalizedUnit === "k" || normalizedUnit === "千") {
    return Math.round(number * 1000);
  }
  if (normalizedUnit === "m") {
    return Math.round(number * 1000000);
  }
  return Math.round(number);
}

function mergeUnique(...lists) {
  const seen = new Set();
  const merged = [];
  lists.flat().forEach((item) => {
    const clean = String(item || "").trim();
    const key = clean.toLowerCase();
    if (clean && !seen.has(key)) {
      seen.add(key);
      merged.push(clean);
    }
  });
  return merged;
}

function inferLocation(text) {
  const rules = [
    [/tokyo|東京|tokio/i, "Tokyo"],
    [/osaka|大阪/i, "Osaka"],
    [/kyoto|京都/i, "Kyoto"],
    [/kanagawa|横浜|yokohama|神奈川/i, "Kanagawa"],
    [/nagoya|名古屋|aichi|愛知/i, "Aichi"],
    [/fukuoka|福岡/i, "Fukuoka"],
    [/japan|日本/i, "Japan"],
  ];
  return rules.find(([pattern]) => pattern.test(text))?.[1] || "";
}

function inferStyle(text) {
  const rules = [
    [/office|通勤|オフィス|きれいめ|綺麗め/i, ["オフィスカジュアル", ["通勤", "きれいめ"]]],
    [/petite|低身長|小柄|150cm|151cm|152cm|153cm|154cm|155cm/i, ["低身長コーデ", ["低身長"]]],
    [/mama|ママ|mom|kids|育児/i, ["ママコーデ", ["ママ", "休日"]]],
    [/骨格|wave|ウェーブ|ストレート|ナチュラル/i, ["骨格コーデ", ["骨格診断"]]],
    [/casual|カジュアル|大人|adult/i, ["大人カジュアル", ["大人カジュアル"]]],
    [/street|ストリート/i, ["ストリート", ["ストリート"]]],
  ];
  return rules.find(([pattern]) => pattern.test(text))?.[1] || ["大人カジュアル", []];
}

function extractProfileSuggestion(sourceText, row) {
  const source = String(sourceText || "").trim();
  if (!source) {
    return null;
  }
  const email = source.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)?.[0] || "";
  const handle =
    source.match(/instagram\.com\/([A-Za-z0-9._]{2,30})/i)?.[1] ||
    source.match(/(?<![\w.])@([A-Za-z0-9._]{2,30})(?![\w.])/i)?.[1] ||
    "";
  const followerMatch =
    source.match(/(?:followers|フォロワー|粉丝|粉絲)\D{0,16}([\d,.]+)\s*(万|w|k|m|千)?/i) ||
    source.match(/([\d,.]+)\s*(万|w|k|m|千)?\s*(?:followers|フォロワー|粉丝|粉絲)/i);
  const followers = followerMatch ? parseSocialCount(followerMatch[1], followerMatch[2]) : 0;
  const engagementMatch = source.match(/([\d.]+)\s*%\s*(?:ER|engagement|互动|エンゲージメント)?/i);
  const engagementRate = engagementMatch ? Number(Number(engagementMatch[1]).toFixed(2)) : 0;
  const avatarUrl =
    source.match(/https?:\/\/[^\s<>"'，。)）\]]+\.(?:jpg|jpeg|png|webp)(?:\?[^\s<>"'，。)）\]]*)?/i)?.[0] ||
    source.match(/(?:avatarUrl|avatar|profileImage|image|头像链接|头像)\s*[:：]\s*(https?:\/\/[^\s<>"'，。)）\]]+)/i)?.[1] ||
    "";
  const [niche, inferredTags] = inferStyle(source);
  const hashtagTags = Array.from(source.matchAll(/#([\p{L}\p{N}_ー-]{2,24})/gu))
    .map((match) => match[1])
    .slice(0, 8);
  const topPosts = hashtagTags.slice(0, 5);
  const location = inferLocation(source);
  const bioLines = source
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !/@|instagram\.com|followers|フォロワー|粉丝|粉絲|^\d+/.test(line))
    .slice(0, 4);
  const bio = bioLines.join(" / ").slice(0, 260);
  const suggestion = {
    handle: handle && handle.toLowerCase() !== String(row.handle || "").toLowerCase() ? handle : "",
    email,
    followers,
    engagementRate,
    avatarUrl: safeImageUrl(avatarUrl),
    location,
    niche,
    tags: mergeUnique(inferredTags, hashtagTags).slice(0, 8),
    topPosts,
    contactMethod: email ? "email" : "",
    notes: bio ? `资料补全：${bio}` : "",
  };
  Object.keys(suggestion).forEach((key) => {
    const value = suggestion[key];
    if (value === "" || value === 0 || (Array.isArray(value) && !value.length)) {
      delete suggestion[key];
    }
  });
  return Object.keys(suggestion).length ? suggestion : null;
}

function appendNote(existing, next) {
  const parts = String(existing || "")
    .split(/\n+/)
    .map((part) => part.trim())
    .filter(Boolean);
  if (next && !parts.includes(next)) {
    parts.push(next);
  }
  return parts.join("\n");
}

async function applyProfileSuggestion() {
  const row = selectedCandidate();
  const suggestion = state.profileSuggestion;
  if (!row || !suggestion) {
    return;
  }
  const payload = {
    ...row,
    ...suggestion,
    handle: row.handle || suggestion.handle || "",
    name: row.name || suggestion.name || row.handle,
    tags: mergeUnique(row.tags || [], suggestion.tags || []).slice(0, 8),
    topPosts: mergeUnique(row.topPosts || [], suggestion.topPosts || []).slice(0, 8),
    avatarUrl: suggestion.avatarUrl || row.avatarUrl || "",
    notes: appendNote(row.notes, suggestion.notes),
    contactMethod: suggestion.contactMethod || row.contactMethod,
  };
  try {
    const result = await apiJson("/api/candidates", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.selectedId = result.candidate.id;
    clearProfileSuggestion();
    dom.profileSource.value = "";
    await loadWorkspace({ silent: true });
    showToast("达人资料已补全");
  } catch (error) {
    showToast(`补全保存失败：${error.message}`);
  }
}

async function runInstagramEnrichment() {
  const row = selectedCandidate();
  if (!row) {
    showToast("先选择一个达人");
    return;
  }
  if (!row.handle) {
    showToast("当前达人缺少 Instagram handle");
    return;
  }
  const setup = instagramGraphSetup();
  if (!setup.canEnrichCandidates) {
    renderInstagramEnrichStatus(row);
    showToast("当前 token 不能补全达人候选池，需要 Facebook/Page token");
    return;
  }
  dom.instagramEnrichBtn.disabled = true;
  dom.instagramEnrichBtn.textContent = "补全中...";
  dom.instagramEnrichStatus.textContent = `正在通过官方 API 查询 @${row.handle}`;
  try {
    const result = await apiJson("/api/instagram/enrich", {
      method: "POST",
      body: JSON.stringify({ id: row.id, handle: row.handle }),
    });
    if (!result.ok) {
      throw new Error(result.error || "Instagram API 补全失败");
    }
    state.selectedId = result.candidate.id;
    state.profileSuggestion = null;
    dom.profileSource.value = "";
    await loadWorkspace({ silent: true });
    showToast(`@${result.candidate.handle || row.handle} 资料已补全`);
  } catch (error) {
    renderInstagramEnrichStatus(row);
    dom.instagramEnrichStatus.textContent = `补全失败：${error.message}`;
    showToast(`Instagram API 补全失败：${error.message}`);
  }
}

async function saveReplyAnalysis() {
  const row = selectedCandidate();
  const analysis = state.replyAnalysis;
  if (!row || !analysis) {
    return;
  }
  try {
    await apiJson("/api/candidates/status", {
      method: "POST",
      body: JSON.stringify({ id: row.id, status: analysis.status }),
    });
    await apiJson("/api/candidates/log", {
      method: "POST",
      body: JSON.stringify({
        id: row.id,
        note: analysis.note,
        type: "reply",
        followUpDate: dom.followupDate.value || row.followUpDate || defaultFollowUpDate(2),
      }),
    });
    state.replyAnalysis = null;
    dom.replySource.value = "";
    await loadWorkspace({ silent: true });
    renderReplyAssistant();
    showToast("达人回复已记录，状态已更新");
  } catch (error) {
    showToast(`回复记录失败：${error.message}`);
  }
}

async function updateStatus(id, status) {
  try {
    await apiJson("/api/candidates/status", {
      method: "POST",
      body: JSON.stringify({ id, status }),
    });
    await loadWorkspace({ silent: true });
    showToast("状态已更新");
  } catch (error) {
    showToast(`状态更新失败：${error.message}`);
  }
}

async function toggleCandidatePin(row) {
  if (!row) {
    return;
  }
  const nextPinned = !row.pinned;
  try {
    const result = await apiJson("/api/candidates/pin", {
      method: "POST",
      body: JSON.stringify({ id: row.id, pinned: nextPinned }),
    });
    if (!result.ok) {
      throw new Error("置顶保存失败");
    }
    state.selectedId = row.id;
    await loadWorkspace({ silent: true });
    showToast(nextPinned ? "已置顶达人" : "已取消置顶");
  } catch (error) {
    showToast(`置顶失败：${error.message}`);
  }
}

async function deleteCandidateRow(row) {
  if (!row) {
    return;
  }
  const label = row.handle ? `@${row.handle}` : row.name || "这个达人";
  const confirmed = window.confirm(`确认从候选池删除 ${label} 吗？\n\n删除后会从本地达人库移除，但不会影响 Instagram。`);
  if (!confirmed) {
    return;
  }
  try {
    const result = await apiJson("/api/candidates/delete", {
      method: "POST",
      body: JSON.stringify({ id: row.id }),
    });
    if (!result.ok) {
      throw new Error(result.error || "删除失败");
    }
    state.queue.ids = state.queue.ids.filter((id) => id !== row.id);
    if (state.selectedId === row.id) {
      const remaining = (state.payload?.candidates || []).filter((item) => item.id !== row.id);
      state.selectedId = remaining[0]?.id || "";
      state.modelDraft = null;
      state.replyAnalysis = null;
      clearProfileSuggestion();
    }
    await loadWorkspace({ silent: true });
    showToast(`${label} 已从候选池删除`);
  } catch (error) {
    showToast(`删除失败：${error.message}`);
  }
}

async function deleteAllCandidates() {
  const total = (state.payload?.candidates || []).length;
  if (!total) {
    showToast("候选池暂无达人可删除");
    return;
  }
  const confirmation = window.prompt(
    `将从本地候选池删除全部 ${formatNumber(total)} 个达人。\n\n此操作不会影响 Instagram，但无法在页面内撤销。\n请输入 DELETE 确认删除：`,
  );
  if (confirmation !== "DELETE") {
    showToast("已取消删除全部");
    return;
  }
  try {
    const result = await apiJson("/api/candidates/delete-all", {
      method: "POST",
      body: JSON.stringify({ confirm: "DELETE" }),
    });
    if (!result.ok) {
      throw new Error(result.error || "删除失败");
    }
    state.selectedId = "";
    state.queue = { active: false, ids: [], index: 0, sent: 0, total: 0 };
    state.profileCandidateId = "";
    state.modelDraft = null;
    state.replyAnalysis = null;
    clearProfileSuggestion();
    await loadWorkspace({ silent: true });
    showToast(`已删除 ${formatNumber(result.deleted ?? total)} 个候选达人`);
  } catch (error) {
    showToast(`删除全部失败：${error.message}`);
  }
}

async function saveFollowup(id, followUpDate) {
  try {
    await apiJson("/api/candidates/followup", {
      method: "POST",
      body: JSON.stringify({ id, followUpDate }),
    });
    await loadWorkspace({ silent: true });
    showToast("跟进日期已保存");
  } catch (error) {
    showToast(`保存失败：${error.message}`);
  }
}

async function logContact(id, note, followUpDate) {
  try {
    await apiJson("/api/candidates/log", {
      method: "POST",
      body: JSON.stringify({
        id,
        note,
        followUpDate,
        type: "contacted",
      }),
    });
    dom.contactNote.value = "";
    await loadWorkspace({ silent: true });
    showToast("联系记录已写入");
  } catch (error) {
    showToast(`记录失败：${error.message}`);
  }
}

async function runPublicSearchPreview() {
  const keyword = publicSearchKeyword();
  const engine = dom.publicSearchEngine.value;
  const limit = Number(dom.publicSearchLimit.value || 10);
  renderPublicSearchLink();
  dom.publicSearchStatus.textContent = "正在读取公开搜索结果...";
  dom.publicSearchBtn.disabled = true;
  try {
    const preview = await apiJson("/api/public-search/preview", {
      method: "POST",
      body: JSON.stringify({ keyword, engine, limit }),
    });
    state.previewMode = "collector";
    state.pendingImportCsv = "";
    state.pendingCollector = preview.sourceText
      ? {
          sourceText: preview.sourceText,
          keyword,
          sourceLabel: `public_search:${preview.engine || engine}`,
        }
      : null;
    state.importPreview = preview;
    renderImportPreview();
    const setup = preview.setup || {};
    if (!preview.configured) {
      dom.publicSearchStatus.textContent = "未配置 API key：请点击“打开搜索”，复制结果后粘到合规采集器。";
      showToast("未配置公开搜索 API，已生成手动搜索链接");
      return;
    }
    if (preview.error) {
      dom.publicSearchStatus.textContent = `搜索接口返回错误：${preview.error}`;
      showToast("公开搜索失败，请检查 API key 或稍后重试");
      return;
    }
    dom.publicSearchStatus.textContent = `搜索源：${preview.engine} · 结果 ${preview.resultCount || 0} · 提取 ${preview.summary?.rows || 0}`;
    showToast(`公开搜索预览完成：提取 ${preview.summary?.rows || 0} 个候选`);
    if (!setup.googleCse && !setup.serpApi) {
      dom.publicSearchStatus.textContent += " · 未检测到可用 API 配置";
    }
  } catch (error) {
    dom.publicSearchStatus.textContent = `公开搜索失败：${error.message}`;
    showToast(`公开搜索失败：${error.message}`);
  } finally {
    dom.publicSearchBtn.disabled = false;
  }
}

function startQueue() {
  const rows = queueEligibleRows();
  if (!rows.length) {
    showToast("当前筛选下没有可建联候选");
    return;
  }
  const ids = rows.map((row) => row.id);
  const selectedIndex = ids.indexOf(state.selectedId);
  state.queue = {
    active: true,
    ids,
    index: selectedIndex >= 0 ? selectedIndex : 0,
    sent: 0,
    total: ids.length,
  };
  state.selectedId = state.queue.ids[state.queue.index];
  state.activeDraft = "dm";
  render();
  showToast(`建联队列已开始：${rows.length} 个候选`);
}

function stopQueue() {
  state.queue = { active: false, ids: [], index: 0, sent: 0, total: 0 };
  renderQueue();
  showToast("建联队列已停止");
}

function openCurrentQueueProfile() {
  const row = currentQueueRow();
  if (!row) {
    return;
  }
  window.open(row.instagramUrl, "_blank", "noopener,noreferrer");
}

function copyCurrentQueueDm() {
  const row = currentQueueRow();
  if (!row) {
    return;
  }
  const text = row.id === state.selectedId ? dom.draftText.textContent : row.drafts?.dm || "";
  void copyText(text, `@${row.handle} 的文案已复制`);
}

function selectQueueIndex(index) {
  state.queue.index = index;
  const nextId = state.queue.ids[state.queue.index];
  if (!nextId) {
    state.queue = { active: false, ids: [], index: 0, sent: 0, total: 0 };
    render();
    showToast("队列已完成");
    return;
  }
  state.selectedId = nextId;
  state.activeDraft = "dm";
  render();
}

function skipCurrentQueueRow() {
  if (!state.queue.active) {
    return;
  }
  selectQueueIndex(state.queue.index + 1);
}

async function markCurrentQueueSent() {
  const row = currentQueueRow();
  if (!row) {
    return;
  }
  const followUpDate = dom.followupDate.value || row.followUpDate || defaultFollowUpDate();
  const note = dom.contactNote.value.trim() || "已手动发送建联消息（队列模式）";
  try {
    await apiJson("/api/candidates/log", {
      method: "POST",
      body: JSON.stringify({
        id: row.id,
        note,
        followUpDate,
        type: "contacted",
      }),
    });
    dom.contactNote.value = "";
    state.queue.sent += 1;
    state.queue.index += 1;
    const nextId = state.queue.ids[state.queue.index] || "";
    if (!nextId) {
      state.queue = { active: false, ids: [], index: 0, sent: 0, total: 0 };
      state.selectedId = "";
      await loadWorkspace({ silent: true });
      showToast("已记录建联，队列完成");
      return;
    }
    state.selectedId = nextId;
    await loadWorkspace({ silent: true });
    showToast("已记录建联，进入下一个");
  } catch (error) {
    showToast(`队列记录失败：${error.message}`);
  }
}

dom.refreshBtn.addEventListener("click", () => {
  void loadWorkspace();
});

dom.scrollTopBtn.addEventListener("click", () => {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
});

window.addEventListener("scroll", updateScrollTopButton, { passive: true });

dom.filterSearch.addEventListener("input", (event) => {
  state.filters.search = event.target.value.trim();
  renderQueue();
  renderCandidates();
});

dom.filterStatus.addEventListener("change", (event) => {
  state.filters.status = event.target.value;
  renderQueue();
  renderCandidates();
});

dom.filterTier.addEventListener("change", (event) => {
  state.filters.tier = event.target.value;
  renderQueue();
  renderCandidates();
});

dom.filterSort.addEventListener("change", (event) => {
  state.filters.sort = event.target.value;
  renderQueue();
  renderCandidates();
});

dom.clearFiltersBtn.addEventListener("click", () => {
  state.filters = { search: "", status: "", tier: "", workflow: "", sort: "score_desc" };
  dom.filterSearch.value = "";
  dom.filterStatus.value = "";
  dom.filterTier.value = "";
  dom.filterSort.value = state.filters.sort;
  renderTaskBoard();
  renderQueue();
  renderCandidates();
});

dom.deleteAllCandidatesBtn.addEventListener("click", () => {
  void deleteAllCandidates();
});

document.querySelectorAll("[data-workflow]").forEach((button) => {
  button.addEventListener("click", () => {
    state.filters.workflow = state.filters.workflow === button.dataset.workflow ? "" : button.dataset.workflow;
    const rows = filteredCandidates();
    if (rows.length) {
      state.selectedId = rows[0].id;
    }
    renderTaskBoard();
    renderQueue();
    renderCandidates();
    renderDetail();
  });
});

dom.queueTargetInput.addEventListener("input", renderQueue);
dom.queueStartBtn.addEventListener("click", startQueue);
dom.queueStopBtn.addEventListener("click", stopQueue);
dom.queueOpenBtn.addEventListener("click", openCurrentQueueProfile);
dom.queueCopyBtn.addEventListener("click", copyCurrentQueueDm);
dom.queueSkipBtn.addEventListener("click", skipCurrentQueueRow);
dom.queueSentNextBtn.addEventListener("click", () => {
  void markCurrentQueueSent();
});

dom.profileExtractBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (!row) {
    showToast("先选择一个达人");
    return;
  }
  state.profileSuggestion = extractProfileSuggestion(dom.profileSource.value, row);
  renderProfilePreview();
  showToast(state.profileSuggestion ? "已识别可补全字段" : "没有识别到可补全字段");
});

dom.profileSource.addEventListener("input", () => {
  clearProfileSuggestion();
});

dom.profileApplyBtn.addEventListener("click", () => {
  void applyProfileSuggestion();
});

dom.instagramEnrichBtn.addEventListener("click", () => {
  void runInstagramEnrichment();
});

dom.candidateList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  const card = event.target.closest(".candidate-card");
  if (!button && card) {
    state.selectedId = card.dataset.id;
    renderCandidates();
    renderDetail();
    return;
  }
  if (!button) {
    return;
  }
  const row = (state.payload.candidates || []).find((item) => item.id === button.dataset.id);
  if (!row) {
    return;
  }
  if (button.dataset.action === "select") {
    state.selectedId = row.id;
    renderCandidates();
    renderDetail();
  }
  if (button.dataset.action === "copy-dm") {
    void copyText(row.drafts?.dm || "", `@${row.handle} 的 DM 已复制`);
  }
  if (button.dataset.action === "pin") {
    void toggleCandidatePin(row);
  }
  if (button.dataset.action === "delete") {
    void deleteCandidateRow(row);
  }
});

document.querySelectorAll("[data-draft]").forEach((button) => {
  button.addEventListener("click", () => {
    state.activeDraft = button.dataset.draft;
    state.templateKey = "";
    state.copyMode = "default";
    const row = selectedCandidate();
    if (row) {
      renderDraft(row);
    }
  });
});

dom.templateSelect.addEventListener("change", (event) => {
  state.templateKey = event.target.value;
  state.copyMode = state.templateKey ? "optimized" : "default";
  const row = selectedCandidate();
  if (row) {
    renderDraft(row);
    showToast(state.templateKey ? `已切换到${templateName(state.templateKey)}优化文案` : "已切回默认文案");
  }
});

dom.copyToneSelect.addEventListener("change", (event) => {
  state.copyTone = event.target.value;
  state.copyMode = "optimized";
  const row = selectedCandidate();
  if (row) {
    renderDraft(row);
  }
});

dom.copyLengthSelect.addEventListener("change", (event) => {
  state.copyLength = event.target.value;
  state.copyMode = "optimized";
  const row = selectedCandidate();
  if (row) {
    renderDraft(row);
  }
});

dom.productSelect.addEventListener("change", (event) => {
  state.productKey = event.target.value;
  state.copyMode = "optimized";
  const row = selectedCandidate();
  if (row) {
    renderDraft(row);
    showToast(state.productKey === "auto" ? "已切回产品自动匹配" : "主推产品已更新");
  }
});

dom.copyHookInput.addEventListener("input", (event) => {
  state.copyHook = event.target.value;
  state.copyMode = "optimized";
  const row = selectedCandidate();
  if (row) {
    renderDraft(row);
  }
});

dom.replyAnalyzeBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (!row) {
    showToast("先选择一个达人");
    return;
  }
  state.replyAnalysis = analyzeCreatorReply(dom.replySource.value, row);
  renderReplyAssistant();
  showToast(state.replyAnalysis ? `已识别：${state.replyAnalysis.label}` : "先粘贴达人回复");
});

dom.replyModelBtn.addEventListener("click", () => {
  void generateModelReply();
});

dom.replySource.addEventListener("input", () => {
  state.replyAnalysis = null;
  renderReplyAssistant();
});

dom.replyCopyBtn.addEventListener("click", () => {
  if (!state.replyAnalysis) {
    return;
  }
  void copyText(state.replyAnalysis.draft, "回复文案已复制", dom.replyDraft);
});

dom.replyLogBtn.addEventListener("click", () => {
  void saveReplyAnalysis();
});

dom.replyClearBtn.addEventListener("click", () => {
  state.replyAnalysis = null;
  dom.replySource.value = "";
  renderReplyAssistant();
});

dom.partnershipSaveBtn.addEventListener("click", () => {
  void savePartnershipTracking();
});

[
  dom.partnershipInvitationSentAt,
  dom.partnershipConnectionAt,
  dom.partnershipBloggerId,
  dom.partnershipCreatorType,
  dom.partnershipFollowers,
  dom.partnershipProfileUrl,
  dom.partnershipStage,
  dom.partnershipQuote,
  dom.partnershipCollabProduct,
  dom.partnershipSampleStatus,
  dom.partnershipSampleCost,
  dom.partnershipRecipientName,
  dom.partnershipPostalCode,
  dom.partnershipShippingAddress,
  dom.partnershipPhoneNumber,
  dom.partnershipOrderNumber,
  dom.partnershipTracking,
  dom.partnershipShippedAt,
  dom.partnershipReceivedAt,
  dom.partnershipVideoProgress,
  dom.partnershipPostDate,
  dom.partnershipPostUrl,
  dom.partnershipCoupon,
  dom.partnershipOrders,
  dom.partnershipRevenue,
].forEach((input) => {
  const refreshSummary = () => {
    const row = selectedCandidate();
    if (row) {
      renderPartnershipTracker(currentPartnershipPayload(row));
    }
  };
  input.addEventListener("input", refreshSummary);
  input.addEventListener("change", refreshSummary);
});

dom.copyRecommendBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (!row) {
    return;
  }
  applyRecommendedCopySettings(row);
  renderDraft(row);
  showToast(`已推荐：${templateName(state.templateKey)}`);
});

dom.copyOptimizeBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (!row) {
    return;
  }
  state.copyMode = "optimized";
  if (!state.templateKey) {
    state.templateKey = recommendTemplateKey(row);
  }
  renderDraft(row);
  showToast("优化文案已生成");
});

dom.copyModelBtn.addEventListener("click", () => {
  void generateModelDraft();
});

dom.copyModelSaveBtn.addEventListener("click", () => {
  saveCopyModelSettings();
  showToast("AI 配置已保存");
});

dom.copyModelTestBtn.addEventListener("click", () => {
  void testCopyModelSettings();
});

dom.copyModelClearBtn.addEventListener("click", () => {
  clearCopyModelSettings();
  showToast("AI 配置已清空");
});

dom.copyModelProvider.addEventListener("change", saveCopyModelSettings);
dom.copyModelBaseUrl.addEventListener("change", saveCopyModelSettings);
dom.copyModelName.addEventListener("change", saveCopyModelSettings);
dom.copyModelAuthMode.addEventListener("change", saveCopyModelSettings);
dom.copyModelApiKey.addEventListener("change", saveCopyModelSettings);
dom.copyModelSaveKey.addEventListener("change", saveCopyModelSettings);

dom.copyDefaultBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  state.copyMode = "default";
  state.templateKey = "";
  state.copyHook = "";
  state.modelDraft = null;
  dom.copyHookInput.value = "";
  if (row) {
    renderDraft(row);
  }
  showToast("已恢复默认文案");
});

dom.templateCopyBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (!row) {
    return;
  }
  const fixedSubject = state.templateKey ? fixedTemplateSubject(row, state.templateKey) : "";
  const subjectPrefix = fixedSubject ? `${fixedSubject}\n\n` : "";
  void copyText(`${subjectPrefix}${dom.draftText.textContent}`, "当前文案已复制", dom.draftText);
});

dom.detailStatus.addEventListener("change", (event) => {
  const row = selectedCandidate();
  if (row) {
    void updateStatus(row.id, event.target.value);
  }
});

dom.deleteCandidateBtn.addEventListener("click", () => {
  void deleteCandidateRow(selectedCandidate());
});

dom.saveFollowupBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (row) {
    void saveFollowup(row.id, dom.followupDate.value);
  }
});

dom.quickLogBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (row) {
    const note = dom.contactNote.value.trim() || "已发送建联消息";
    void logContact(row.id, note, dom.followupDate.value);
  }
});

dom.copyDraftBtn.addEventListener("click", () => {
  const row = selectedCandidate();
  if (!row) {
    return;
  }
  const fixedSubject = state.templateKey ? fixedTemplateSubject(row, state.templateKey) : "";
  const subject = fixedSubject || (state.copyMode === "default" && !state.templateKey && state.activeDraft === "email" ? row.drafts.emailSubject : "");
  const subjectPrefix = subject ? `${subject}\n\n` : "";
  void copyText(`${subjectPrefix}${dom.draftText.textContent}`, "建联文案已复制", dom.draftText);
});

dom.searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const keyword = dom.keywordInput.value.trim() || "大人女子コーデ";
  const signal = dom.signalSelect.value;
  window.open(buildGoogleSearch(keyword, signal), "_blank", "noopener,noreferrer");
});

dom.keywordInput.addEventListener("input", () => {
  fillHashtagInput();
});
dom.publicSearchKeyword.addEventListener("input", () => {
  renderPublicSearchLink();
  fillHashtagInput();
});
dom.collectorKeyword.addEventListener("input", () => {
  fillHashtagInput();
});
dom.websiteKeyword.addEventListener("input", () => {
  fillHashtagInput();
});
dom.publicSearchEngine.addEventListener("change", renderPublicSearchLink);
dom.publicSearchBtn.addEventListener("click", () => {
  void runPublicSearchPreview();
});

dom.skillGeneratePromptBtn.addEventListener("click", () => {
  void generateSkillPrompt();
});

dom.skillCreatePlanBtn.addEventListener("click", () => {
  void createSkillPlan();
});

dom.skillCopyPromptBtn.addEventListener("click", () => {
  const prompt = dom.skillPromptOutput.value.trim();
  if (!prompt) {
    showToast("先生成提示词");
    return;
  }
  void copyText(prompt, "提示词已复制", dom.skillPromptOutput);
});

dom.skillRefreshRunsBtn.addEventListener("click", () => {
  void loadWorkspace({ silent: true });
  showToast("抓取进度已刷新");
});

dom.skillRunList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-skill-run-delete]");
  if (!button) {
    return;
  }
  void deleteSkillRun(button.dataset.skillRunDelete);
});

dom.openTagsBtn.addEventListener("click", () => {
  const tags = state.payload?.discovery?.hashtags || [];
  openHashtagPages(tags.slice(0, 4).map((item) => item.label));
});

dom.hashtagInput.addEventListener("input", () => {
  state.hashtagInputEdited = true;
  renderHashtagSuggestions();
});

dom.hashtagAutoBtn.addEventListener("click", () => {
  const tags = fillHashtagInput({ force: true });
  showToast(tags.length ? "Hashtag 已自动填入" : "没有可生成的 Hashtag");
});

dom.openInputTagsBtn.addEventListener("click", () => {
  const tags = parseHashtagInput();
  openHashtagPages(tags.length ? tags : buildHashtagSuggestions());
});

dom.copyTagsBtn.addEventListener("click", () => {
  const text = dom.hashtagInput.value.trim();
  if (!text) {
    showToast("没有可复制的 Hashtag");
    return;
  }
  void copyText(text, "Hashtag 已复制", dom.hashtagInput);
});

dom.hashtagSuggestions.addEventListener("click", (event) => {
  const button = event.target.closest("[data-tag]");
  if (button) {
    addHashtagToInput(button.dataset.tag);
  }
});

dom.collectorPreviewBtn.addEventListener("click", async () => {
  const sourceText = dom.collectorSource.value.trim();
  const keyword = dom.collectorKeyword.value.trim();
  if (!sourceText) {
    showToast("先粘贴搜索结果、URL 或 HTML");
    return;
  }
  try {
    const preview = await apiJson("/api/discovery/preview", {
      method: "POST",
      body: JSON.stringify({
        sourceText,
        keyword,
        sourceLabel: "manual_collector",
      }),
    });
    state.previewMode = "collector";
    state.pendingImportCsv = "";
    state.pendingCollector = { sourceText, keyword, sourceLabel: "manual_collector" };
    state.importPreview = preview;
    renderImportPreview();
    showToast(`已提取 ${preview.summary.rows || 0} 个候选`);
  } catch (error) {
    showToast(`采集预览失败：${error.message}`);
  }
});

dom.websitePreviewBtn.addEventListener("click", async () => {
  const sourceText = dom.websiteSource.value.trim();
  const keyword = dom.websiteKeyword.value.trim();
  if (!sourceText) {
    showToast("先粘贴达人网站或 Instagram 链接");
    return;
  }
  dom.websitePreviewBtn.disabled = true;
  dom.websiteStatus.textContent = "正在读取公开网页并识别达人信息...";
  try {
    const preview = await apiJson("/api/website/preview", {
      method: "POST",
      body: JSON.stringify({ sourceText, keyword }),
    });
    state.previewMode = "website";
    state.pendingImportCsv = "";
    state.pendingCollector = null;
    state.pendingWebsite = { sourceText, keyword };
    state.importPreview = preview;
    renderImportPreview();
    const errorText = preview.errors?.length ? `，${preview.errors.length} 个链接读取失败` : "";
    dom.websiteStatus.textContent = `识别完成：读取 ${preview.summary?.urls || 0} 个链接，提取 ${preview.summary?.rows || 0} 个候选${errorText}`;
    showToast(`达人网站识别完成：${preview.summary?.rows || 0} 个候选`);
  } catch (error) {
    dom.websiteStatus.textContent = `网站识别失败：${error.message}`;
    showToast(`网站识别失败：${error.message}`);
  } finally {
    dom.websitePreviewBtn.disabled = false;
  }
});

dom.csvInput.addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  if (!file) {
    return;
  }
  const csvText = await file.text();
  try {
    const preview = await apiJson("/api/import/preview", {
      method: "POST",
      body: JSON.stringify({ csvText }),
    });
    state.previewMode = "csv";
    state.pendingImportCsv = csvText;
    state.pendingCollector = null;
    state.importPreview = preview;
    renderImportPreview();
    showToast("CSV 已解析，请确认导入");
  } catch (error) {
    showToast(`预览失败：${error.message}`);
  } finally {
    event.target.value = "";
  }
});

dom.cancelImportBtn.addEventListener("click", () => {
  state.previewMode = "";
  state.pendingImportCsv = "";
  state.pendingCollector = null;
  state.pendingWebsite = null;
  state.importPreview = null;
  renderImportPreview();
});

dom.confirmImportBtn.addEventListener("click", async () => {
  if (!state.pendingImportCsv && !state.pendingCollector && !state.pendingWebsite) {
    showToast("没有待导入的数据");
    return;
  }
  try {
    const result =
      state.previewMode === "website"
        ? await apiJson("/api/website/import", {
            method: "POST",
            body: JSON.stringify(state.pendingWebsite),
          })
        : state.previewMode === "collector"
        ? await apiJson("/api/discovery/import", {
            method: "POST",
            body: JSON.stringify(state.pendingCollector),
          })
        : await apiJson("/api/import", {
            method: "POST",
            body: JSON.stringify({ csvText: state.pendingImportCsv }),
          });
    const mode = state.previewMode;
    state.previewMode = "";
    state.pendingImportCsv = "";
    state.pendingCollector = null;
    state.pendingWebsite = null;
    state.importPreview = null;
    await loadWorkspace({ silent: true });
    renderImportPreview();
    showToast(`${mode === "collector" ? "采集入库" : mode === "website" ? "网站识别入库" : "导入"}完成：新增 ${result.added}，更新 ${result.updated}`);
  } catch (error) {
    showToast(`导入失败：${error.message}`);
  }
});

dom.candidateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(dom.candidateForm);
  const payload = Object.fromEntries(formData.entries());
  try {
    const result = await apiJson("/api/candidates", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.selectedId = result.candidate.id;
    dom.candidateForm.reset();
    await loadWorkspace({ silent: true });
    showToast(result.created ? "候选已新增" : "候选已更新");
  } catch (error) {
    showToast(`保存失败：${error.message}`);
  }
});

loadCopyModelSettings();
updateScrollTopButton();
void loadWorkspace({ silent: true });
