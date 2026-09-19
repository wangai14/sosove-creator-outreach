from __future__ import annotations

import csv
import html
import ipaddress
import io
import json
import os
import re
import socket
import subprocess
import sys
import uuid
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, quote_plus, urlencode, urljoin, urlparse


PACKAGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PACKAGE_DIR.parent
STATIC_DIR = PACKAGE_DIR / "static"


def load_dotenv_files(*paths: Path) -> None:
    for path in paths:
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            clean = line.strip()
            if not clean or clean.startswith("#") or "=" not in clean:
                continue
            key, value = clean.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            os.environ[key] = value.strip().strip('"').strip("'")


load_dotenv_files(PACKAGE_DIR / ".env", ROOT_DIR / ".env")

DATA_DIR = Path(
    os.getenv(
        "INSTAGRAM_OUTREACH_DATA_DIR",
        str(ROOT_DIR / "data" / "instagram_creator_outreach"),
    )
)
CANDIDATES_PATH = DATA_DIR / "candidates.json"
INSTAGRAM_DM_SKILL_DIR = Path(
    os.getenv(
        "INSTAGRAM_DM_OUTREACH_SKILL_DIR",
        str(Path.home() / ".codex" / "skills" / "instagram-dm-outreach"),
    )
)
SKILL_HARVEST_OUTPUT_DIR = Path(
    os.getenv("INSTAGRAM_HARVEST_OUTPUT_DIR", str(ROOT_DIR / "data" / "instagram_harvest"))
)

DEFAULT_BRAND = {
    "name": "SOSOVE",
    "market": "Japan",
    "category": "レディースファッション",
    "site": "https://sosove.com",
    "offer": "商品提供を中心に、投稿内容や条件に合わせて案件をご相談",
    "audience": "20代後半から40代の日本女性、通勤、休日、体型カバー、きれいめカジュアルに関心がある層",
    "tone": "丁寧、自然、押し売りしない",
    "value_props": [
        "通勤にも休日にも使いやすいデザイン",
        "体型カバーしやすいシルエット",
        "落ち着いた大人カジュアル",
        "日本向けの着回し提案に合わせやすい",
    ],
}

CSV_FIELDS = [
    "handle",
    "pinned",
    "name",
    "bloggerId",
    "creatorType",
    "niche",
    "location",
    "followers",
    "engagementRate",
    "avgLikes",
    "contentFit",
    "audienceFit",
    "brandSafety",
    "collabSignal",
    "contactMethod",
    "email",
    "instagramUrl",
    "avatarUrl",
    "status",
    "followUpDate",
    "lastContacted",
    "invitationSentAt",
    "connectionAt",
    "priceHintJpy",
    "partnershipStage",
    "quoteJpy",
    "collabProduct",
    "sampleStatus",
    "sampleCostJpy",
    "recipientName",
    "postalCode",
    "shippingAddress",
    "phoneNumber",
    "orderNumber",
    "shippingTracking",
    "shippedAt",
    "receivedAt",
    "postDate",
    "videoProgress",
    "postUrl",
    "couponCode",
    "orders",
    "revenueJpy",
    "tags",
    "notes",
    "score",
    "tier",
    "nextAction",
]

SCORE_FIELDS = [
    ("followers", "粉丝区间", 18),
    ("engagement", "互动率", 22),
    ("content", "内容匹配", 20),
    ("audience", "人群匹配", 16),
    ("safety", "品牌安全", 8),
    ("collab", "合作信号", 10),
    ("contact", "可联系性", 6),
    ("data", "资料完整", 6),
]

STATUS_LABELS = {
    "new": "新候选",
    "review": "待审核",
    "ready": "可建联",
    "contacted": "已建联",
    "replied": "已回复",
    "negotiating": "报价中",
    "approved": "可合作",
    "rejected": "不匹配",
}

DISCOVERY_HASHTAGS = [
    "大人女子コーデ",
    "きれいめカジュアル",
    "30代ファッション",
    "40代ファッション",
    "低身長コーデ",
    "骨格ウェーブ",
    "骨格ストレート",
    "ママコーデ",
    "オフィスカジュアル",
    "着回しコーデ",
    "淡色コーデ",
    "体型カバーコーデ",
]

DISCOVERY_KEYWORDS = [
    "PR",
    "タイアップ",
    "商品提供",
    "レディースファッション",
    "大人カジュアル",
    "着回し",
    "低身長",
    "骨格診断",
    "ママコーデ",
    "通勤コーデ",
]

DEFAULT_SKILL_SEED_HASHTAGS = [
    "#40代ファッション",
    "#40代コーデ",
    "#大人カジュアル",
    "#きれいめカジュアル",
    "#フェミニンコーデ",
    "#ママコーデ",
    "#ワンピースコーデ",
    "#スカートコーデ",
    "#低身長コーデ",
    "#体型カバー",
    "#高見えコーデ",
    "#プチプラコーデ",
]

STRICT_FEMALE_CREATOR_REJECT_TEXT = (
    "明星、粉丝号、抽奖号、私密号、品牌店铺号、媒体号、纯店铺号、"
    "店员/スタッフ/販売員/アパレル店員、男性/メンズ账号、美容院/美容師/サロン/服务号、"
    "UNIQLO/ZARA/GU 等品牌官方号"
)

DEFAULT_SKILL_EXCLUSION_RULES = [
    "#芸能人除外",
    "#ファンアカウント除外",
    "#まとめ転載アカウント除外",
    "#メディアアカウント除外",
    "#懸賞アカウント除外",
    "#キャンペーン専用アカウント除外",
    "#非公開アカウント除外",
    "#投稿なしアカウント除外",
    "#ブランド公式除外",
    "#ショップ公式除外",
    "#ECショップ除外",
    "#セレクトショップ除外",
    "#UNIQLO公式除外",
    "#ZARA公式除外",
    "#GU公式除外",
    "#SHEIN公式除外",
    "#GRL公式除外",
    "#ショップスタッフ除外",
    "#販売員除外",
    "#アパレル店員除外",
    "#メンズアカウント除外",
    "#男性インフルエンサー除外",
    "#男装アカウント除外",
    "#美容院除外",
    "#美容師除外",
    "#ネイルサロン除外",
    "#エステサロン除外",
    "#予約サービスアカウント除外",
    "#ジム公式除外",
    "#フォトグラファー除外",
    "#企業アカウント除外",
    "#学校団体アカウント除外",
    "#グルメ中心除外",
    "#ペット中心除外",
    "#旅行中心除外",
    "#育児中心除外",
    "#インテリア中心除外",
    "#レディースファッション投稿なし除外",
    "#40代コーデ投稿なし除外",
    "#PR実績なし要確認",
]

INSTAGRAM_RESERVED_PATHS = {
    "about",
    "accounts",
    "api",
    "developer",
    "direct",
    "explore",
    "legal",
    "oauth",
    "p",
    "privacy",
    "reel",
    "reels",
    "stories",
    "terms",
}

INSTAGRAM_URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9._]{1,30})(?:[/\?#]|$)",
    re.IGNORECASE,
)
INSTAGRAM_AT_RE = re.compile(r"(?<![\w.])@([A-Za-z0-9._]{2,30})(?![\w.])")

URL_RE = re.compile(r"https?://[^\s<>'\"，。)）\]]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
MAX_WEBSITE_URLS = 20
MAX_WEBSITE_BYTES = 700_000
MAX_WEBSITE_PAGES_PER_URL = 4

INSTAGRAM_GRAPH_DEFAULT_VERSION = "v25.0"
INSTAGRAM_GRAPH_DEFAULT_BASE_URL = "https://graph.facebook.com"
INSTAGRAM_LOGIN_GRAPH_BASE_URL = "https://graph.instagram.com"
INSTAGRAM_BUSINESS_DISCOVERY_MODE = "business_discovery"
INSTAGRAM_LOGIN_MODE = "instagram_login"
INSTAGRAM_GRAPH_PROFILE_FIELDS = (
    "username,name,biography,followers_count,media_count,profile_picture_url,website"
)

BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

SAMPLE_CANDIDATES = [
    {
        "handle": "jp_style_note",
        "name": "Mika",
        "niche": "大人カジュアル",
        "location": "Tokyo",
        "followers": 42800,
        "engagementRate": 3.8,
        "avgLikes": 1260,
        "contentFit": 88,
        "audienceFit": 84,
        "brandSafety": 92,
        "collabSignal": 80,
        "contactMethod": "email",
        "email": "mika@example.com",
        "status": "ready",
        "priceHintJpy": 45000,
        "tags": ["30代", "通勤", "着回し"],
        "notes": "虚构样例账号。内容偏简洁通勤，适合连衣裙和外套线。",
        "topPosts": ["通勤コーデ", "淡色コーデ", "低身長でも使いやすい丈感"],
    },
    {
        "handle": "kurashi_wear_jp",
        "name": "Aya",
        "niche": "ママコーデ",
        "location": "Kanagawa",
        "followers": 18300,
        "engagementRate": 5.1,
        "avgLikes": 930,
        "contentFit": 81,
        "audienceFit": 90,
        "brandSafety": 89,
        "collabSignal": 68,
        "contactMethod": "dm",
        "status": "review",
        "priceHintJpy": 30000,
        "tags": ["ママ", "休日", "体型カバー"],
        "notes": "虚构样例账号。评论质量较好，先人工检查最近三条 PR。",
        "topPosts": ["公園コーデ", "体型カバー", "洗える素材"],
    },
    {
        "handle": "office_chic_tokyo",
        "name": "Rina",
        "niche": "オフィスカジュアル",
        "location": "Tokyo",
        "followers": 96500,
        "engagementRate": 2.4,
        "avgLikes": 2100,
        "contentFit": 93,
        "audienceFit": 78,
        "brandSafety": 95,
        "collabSignal": 74,
        "contactMethod": "creator_marketplace",
        "status": "new",
        "priceHintJpy": 80000,
        "tags": ["オフィス", "きれいめ", "高単価"],
        "notes": "虚构样例账号。适合正式感单品，费用可能偏高。",
        "topPosts": ["ジャケット着回し", "通勤バッグ", "週5コーデ"],
    },
    {
        "handle": "petite_daily_jp",
        "name": "Nana",
        "niche": "低身長コーデ",
        "location": "Osaka",
        "followers": 12600,
        "engagementRate": 6.2,
        "avgLikes": 790,
        "contentFit": 86,
        "audienceFit": 92,
        "brandSafety": 87,
        "collabSignal": 60,
        "contactMethod": "email",
        "email": "nana@example.com",
        "status": "ready",
        "priceHintJpy": 25000,
        "tags": ["低身長", "骨格ウェーブ", "ワンピース"],
        "notes": "虚构样例账号。适合测小个子连衣裙和高腰裤。",
        "topPosts": ["150cmコーデ", "脚長見え", "ワンピース比較"],
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def today_iso() -> str:
    return date.today().isoformat()


def load_candidates(use_samples: bool = True) -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        if not use_samples:
            return []
        return [normalize_candidate(item) for item in SAMPLE_CANDIDATES]
    try:
        payload = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [normalize_candidate(item) for item in SAMPLE_CANDIDATES]
    rows = payload.get("candidates") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return [normalize_candidate(item) for item in SAMPLE_CANDIDATES]
    return [normalize_candidate(item) for item in rows]


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "updatedAt": now_iso(),
        "candidates": [strip_runtime_fields(normalize_candidate(item)) for item in candidates],
    }
    CANDIDATES_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def strip_runtime_fields(candidate: dict[str, Any]) -> dict[str, Any]:
    runtime = {
        "score",
        "tier",
        "scoreBreakdown",
        "scoreBreakdownItems",
        "drafts",
        "nextAction",
        "instagramSearchUrl",
        "manualChecklist",
    }
    return {key: value for key, value in candidate.items() if key not in runtime}


def build_workspace_payload() -> dict[str, Any]:
    candidates = enrich_candidates(load_candidates())
    return {
        "ok": True,
        "brand": DEFAULT_BRAND,
        "statusLabels": STATUS_LABELS,
        "stats": summarize_candidates(candidates),
        "discovery": build_discovery_plan(),
        "skillPanel": build_skill_panel_payload(),
        "candidates": candidates,
        "csvFields": CSV_FIELDS,
        "integrations": {
            "instagramGraph": instagram_graph_setup_state(),
        },
        "source": {
            "mode": "local",
            "candidatePath": str(CANDIDATES_PATH),
            "sampleMode": not CANDIDATES_PATH.exists(),
            "syncedAt": now_iso(),
        },
    }


def enrich_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for item in candidates:
        candidate = normalize_candidate(item)
        score, breakdown = score_candidate(candidate)
        candidate["score"] = score
        candidate["scoreBreakdown"] = breakdown
        candidate["scoreBreakdownItems"] = build_score_breakdown_items(breakdown)
        candidate["tier"] = tier_for_score(score)
        candidate["drafts"] = build_outreach_drafts(candidate)
        candidate["nextAction"] = next_action(candidate, score)
        candidate["instagramSearchUrl"] = instagram_profile_url(candidate["handle"])
        candidate["manualChecklist"] = build_manual_checklist(candidate)
        enriched.append(candidate)
    return sorted(enriched, key=lambda row: (bool(row.get("pinned")), row["score"], row.get("updatedAt", "")), reverse=True)


def normalize_candidate(raw: dict[str, Any] | None) -> dict[str, Any]:
    raw = raw or {}
    handle = normalize_handle(
        first_value(
            raw,
            [
                "handle",
                "username",
                "account",
                "ig",
                "instagram",
                "instagramHandle",
                "profile",
                "profileUrl",
                "instagramUrl",
                "账号",
                "ins账号",
            ],
        )
    )
    name = text(first_value(raw, ["name", "displayName", "creator", "达人", "名称"])) or handle
    tags = normalize_tags(first_value(raw, ["tags", "tag", "labels", "标签"]))
    created_at = text(raw.get("createdAt")) or now_iso()
    updated_at = text(raw.get("updatedAt")) or created_at
    instagram_url = text(first_value(raw, ["instagramUrl", "profileUrl", "url", "homepage", "主页链接", "链接"]))
    if not instagram_url and handle:
        instagram_url = instagram_profile_url(handle)
    avatar_url = normalize_avatar_url(
        first_value(
            raw,
            [
                "avatarUrl",
                "avatarURL",
                "avatar",
                "profileImage",
                "profileImageUrl",
                "image",
                "imageUrl",
                "photo",
                "photoUrl",
                "thumbnail",
                "头像",
                "头像链接",
                "头像URL",
            ],
        )
    )

    return {
        "id": text(raw.get("id")) or stable_candidate_id(handle, name),
        "handle": handle,
        "pinned": boolish(first_value(raw, ["pinned", "pin", "starred", "置顶", "是否置顶"])),
        "name": name,
        "bloggerId": text(first_value(raw, ["bloggerId", "bloggerID", "creatorId", "creatorID", "博主id", "博主ID", "达人ID"])),
        "creatorType": text(first_value(raw, ["creatorType", "bloggerType", "influencerType", "博主类型", "达人类型"])),
        "niche": text(first_value(raw, ["niche", "category", "segment", "赛道"])) or "大人カジュアル",
        "location": text(first_value(raw, ["location", "city", "area", "地区"])) or "Japan",
        "followers": parse_count(first_value(raw, ["followers", "followerCount", "粉丝", "粉丝数"])),
        "engagementRate": parse_percent(
            first_value(raw, ["engagementRate", "engagement", "er", "互动率"])
        ),
        "avgLikes": parse_count(first_value(raw, ["avgLikes", "likes", "averageLikes", "平均点赞"])),
        "contentFit": parse_score(first_value(raw, ["contentFit", "内容匹配", "内容匹配度"]), 72),
        "audienceFit": parse_score(first_value(raw, ["audienceFit", "人群匹配", "人群匹配度"]), 72),
        "brandSafety": parse_score(first_value(raw, ["brandSafety", "安全", "品牌安全"]), 80),
        "collabSignal": parse_score(first_value(raw, ["collabSignal", "prSignal", "合作信号"]), 50),
        "contactMethod": normalize_contact_method(
            first_value(raw, ["contactMethod", "contact", "联系方式", "联系渠道"])
        ),
        "email": text(first_value(raw, ["email", "mail", "邮箱"])),
        "instagramUrl": instagram_url,
        "avatarUrl": avatar_url,
        "creatorMarketplace": boolish(first_value(raw, ["creatorMarketplace", "marketplace"])),
        "status": normalize_status(first_value(raw, ["status", "状态"])),
        "lastContacted": text(first_value(raw, ["lastContacted", "lastContactedAt", "最后联系"])),
        "invitationSentAt": normalize_date_text(
            first_value(raw, ["invitationSentAt", "inviteSentAt", "outreachSentAt", "发送邀约时间", "邀约时间"])
        ),
        "connectionAt": normalize_date_text(
            first_value(raw, ["connectionAt", "connectedAt", "contactedAt", "建联时间", "建联日期"])
        ),
        "followUpDate": normalize_date_text(first_value(raw, ["followUpDate", "nextFollowUp", "跟进日期"])),
        "priceHintJpy": parse_count(first_value(raw, ["priceHintJpy", "price", "报价", "预估报价"])),
        "partnershipStage": normalize_partnership_stage(first_value(raw, ["partnershipStage", "dealStage", "合作阶段"])),
        "quoteJpy": parse_count(first_value(raw, ["quoteJpy", "quotedFeeJpy", "creatorFeeJpy", "达人报价", "合作报价", "报价"])),
        "collabProduct": text(first_value(raw, ["collabProduct", "productName", "product", "合作产品", "产品"])),
        "sampleStatus": normalize_sample_status(first_value(raw, ["sampleStatus", "sample", "样品状态"])),
        "sampleCostJpy": parse_count(first_value(raw, ["sampleCostJpy", "sampleCost", "shippingCostJpy", "样品成本", "物流成本"])),
        "recipientName": text(first_value(raw, ["recipientName", "receiverName", "shippingName", "consignee", "收货姓名", "收件人", "姓名"])),
        "postalCode": text(first_value(raw, ["postalCode", "zipCode", "zip", "postcode", "邮编", "邮政编码"])),
        "shippingAddress": text(first_value(raw, ["shippingAddress", "address", "recipientAddress", "detailAddress", "收货地址", "详细地址", "地址"])),
        "phoneNumber": text(first_value(raw, ["phoneNumber", "phone", "mobile", "tel", "手机号", "手机", "电话"])),
        "orderNumber": text(first_value(raw, ["orderNumber", "orderNo", "orderId", "订单编号", "订单号"])),
        "shippingTracking": text(first_value(raw, ["shippingTracking", "trackingNumber", "tracking", "物流单号"])),
        "shippedAt": normalize_date_text(first_value(raw, ["shippedAt", "shippingDate", "shipDate", "发货时间", "发货日期"])),
        "receivedAt": normalize_date_text(first_value(raw, ["receivedAt", "deliveryDate", "deliveredAt", "收货时间", "收货日期"])),
        "postDate": normalize_date_text(first_value(raw, ["postDate", "publishDate", "投稿日期", "发帖日期"])),
        "videoProgress": normalize_video_progress(first_value(raw, ["videoProgress", "contentProgress", "videoStatus", "视频进度", "内容进度"])),
        "postUrl": text(first_value(raw, ["postUrl", "postLink", "contentUrl", "帖子链接"])),
        "couponCode": text(first_value(raw, ["couponCode", "discountCode", "fanDiscountCode", "优惠码", "粉丝折扣码"])),
        "orders": parse_count(first_value(raw, ["orders", "orderCount", "订单数"])),
        "revenueJpy": parse_count(first_value(raw, ["revenueJpy", "revenue", "salesJpy", "收入", "销售额"])),
        "tags": tags,
        "notes": text(first_value(raw, ["notes", "note", "备注"])),
        "source": text(first_value(raw, ["source", "来源"])) or "manual",
        "topPosts": normalize_list(first_value(raw, ["topPosts", "posts", "recentPosts", "近期内容"])),
        "contactHistory": normalize_contact_history(
            first_value(raw, ["contactHistory", "history", "联系历史"])
        ),
        "createdAt": created_at,
        "updatedAt": updated_at,
    }


def first_value(raw: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in raw and raw[key] not in (None, ""):
            return raw[key]
    lowered = {str(key).lower(): value for key, value in raw.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value not in (None, ""):
            return value
    return ""


def stable_candidate_id(handle: str, name: str) -> str:
    base = handle or name or uuid.uuid4().hex[:10]
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", base).strip("-").lower()
    return cleaned or uuid.uuid4().hex[:10]


def normalize_handle(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    raw = raw.split("?")[0].rstrip("/")
    if "instagram.com/" in raw:
        raw = raw.split("instagram.com/", 1)[1].split("/", 1)[0]
    return raw.lstrip("@").strip()


def instagram_profile_url(handle: str) -> str:
    handle = normalize_handle(handle)
    return f"https://www.instagram.com/{handle}/" if handle else "https://www.instagram.com/"


def normalize_avatar_url(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    raw = html.unescape(raw).strip("<>()[]{}'\"")
    match = URL_RE.search(raw)
    if match:
        raw = match.group(0).rstrip(".,，。")
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    return parsed._replace(fragment="").geturl()


def normalize_status(value: Any) -> str:
    raw = text(value).lower()
    aliases = {
        "": "new",
        "待审核": "review",
        "可建联": "ready",
        "已建联": "contacted",
        "已回复": "replied",
        "报价中": "negotiating",
        "可合作": "approved",
        "不匹配": "rejected",
    }
    raw = aliases.get(raw, raw)
    return raw if raw in STATUS_LABELS else "new"


def normalize_partnership_stage(value: Any) -> str:
    raw = text(value).lower()
    aliases = {
        "": "none",
        "未开始": "none",
        "报价确认": "pricing",
        "报价中": "pricing",
        "待寄样": "sample_pending",
        "待寄样品": "sample_pending",
        "已寄样": "sample_sent",
        "已寄样品": "sample_sent",
        "待发帖": "content_scheduled",
        "排期中": "content_scheduled",
        "已发帖": "posted",
        "已发布": "posted",
        "已复盘": "measured",
        "复盘完成": "measured",
    }
    normalized = aliases.get(raw, raw)
    allowed = {"none", "pricing", "sample_pending", "sample_sent", "content_scheduled", "posted", "measured"}
    return normalized if normalized in allowed else "none"


def normalize_sample_status(value: Any) -> str:
    raw = text(value).lower()
    aliases = {
        "": "none",
        "未安排": "none",
        "未寄样": "none",
        "已索要信息": "requested",
        "要地址": "requested",
        "备货中": "prepared",
        "准备中": "prepared",
        "已发货": "sent",
        "已寄出": "sent",
        "已签收": "delivered",
        "已送达": "delivered",
    }
    normalized = aliases.get(raw, raw)
    allowed = {"none", "requested", "prepared", "sent", "delivered"}
    return normalized if normalized in allowed else "none"


def normalize_video_progress(value: Any) -> str:
    raw = text(value).lower()
    aliases = {
        "": "not_started",
        "未开始": "not_started",
        "选品中": "product_confirming",
        "产品确认": "product_confirming",
        "已寄样": "sample_sent",
        "已发货": "sample_sent",
        "拍摄中": "filming",
        "制作中": "filming",
        "初稿待审": "draft_review",
        "待审核": "draft_review",
        "修改中": "revision",
        "已发布": "posted",
        "已复盘": "measured",
    }
    normalized = aliases.get(raw, raw)
    allowed = {"not_started", "product_confirming", "sample_sent", "filming", "draft_review", "revision", "posted", "measured"}
    return normalized if normalized in allowed else raw


def normalize_contact_method(value: Any) -> str:
    raw = text(value).lower()
    if "mail" in raw or "邮箱" in raw:
        return "email"
    if "creator" in raw or "market" in raw:
        return "creator_marketplace"
    if raw in {"dm", "私信", "message", "instagram"}:
        return "dm"
    if raw in {"email", "creator_marketplace", "dm"}:
        return raw
    return "unknown"


def normalize_tags(value: Any) -> list[str]:
    tags = normalize_list(value)
    return [tag for tag in tags if tag][:8]


def normalize_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [text(item) for item in value if text(item)]
    return [part.strip() for part in re.split(r"[,;、/|，\n\r]+", str(value)) if part.strip()]


def normalize_date_text(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    try:
        return date.fromisoformat(raw[:10]).isoformat()
    except ValueError:
        return raw[:10]


def normalize_contact_history(value: Any) -> list[dict[str, str]]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return [
                {
                    "id": uuid.uuid4().hex[:10],
                    "type": "note",
                    "date": today_iso(),
                    "note": value.strip(),
                    "followUpDate": "",
                }
            ] if value.strip() else []
        return normalize_contact_history(parsed)
    if not isinstance(value, list):
        return []
    history = []
    for item in value:
        if isinstance(item, str):
            note = item.strip()
            if not note:
                continue
            history.append(
                {
                    "id": uuid.uuid4().hex[:10],
                    "type": "note",
                    "date": today_iso(),
                    "note": note,
                    "followUpDate": "",
                }
            )
            continue
        if not isinstance(item, dict):
            continue
        note = text(item.get("note") or item.get("message") or item.get("content"))
        history.append(
            {
                "id": text(item.get("id")) or uuid.uuid4().hex[:10],
                "type": normalize_history_type(item.get("type")),
                "date": normalize_date_text(item.get("date") or item.get("createdAt")) or today_iso(),
                "note": note,
                "followUpDate": normalize_date_text(item.get("followUpDate")),
            }
        )
    return sorted(history, key=lambda row: row.get("date", ""), reverse=True)[:20]


def normalize_history_type(value: Any) -> str:
    raw = text(value).lower()
    if raw in {"contacted", "followup", "reply", "note", "price", "sample"}:
        return raw
    if "reply" in raw or "回复" in raw:
        return "reply"
    if "follow" in raw or "跟进" in raw:
        return "followup"
    if "price" in raw or "报价" in raw:
        return "price"
    return "contacted"


def append_history_event(
    history_value: Any,
    event_type: str,
    note: str,
    event_date: str,
    follow_up_date: str = "",
) -> list[dict[str, str]]:
    history = normalize_contact_history(history_value)
    event = {
        "id": uuid.uuid4().hex[:10],
        "type": normalize_history_type(event_type),
        "date": normalize_date_text(event_date) or today_iso(),
        "note": note.strip(),
        "followUpDate": normalize_date_text(follow_up_date),
    }
    return normalize_contact_history([event, *history])


def default_follow_up_date(days: int = 3) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def candidate_quality_issues(candidate: dict[str, Any]) -> list[str]:
    issues = []
    if not candidate.get("handle"):
        issues.append("缺少 Instagram handle")
    if candidate.get("contactMethod") == "email" and not candidate.get("email"):
        issues.append("Email 渠道但缺少邮箱")
    if not candidate.get("followers"):
        issues.append("缺少粉丝数")
    if not candidate.get("engagementRate"):
        issues.append("缺少互动率")
    if candidate.get("followers", 0) > 500000 and candidate.get("engagementRate", 0) < 1:
        issues.append("粉丝高但互动率偏低")
    if candidate.get("brandSafety", 100) < 65:
        issues.append("品牌安全分偏低")
    return issues[:6]


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    raw = text(value).lower()
    return raw in {"1", "true", "yes", "y", "是", "有", "支持"}


def parse_count(value: Any) -> int:
    if value in (None, ""):
        return 0
    if isinstance(value, (int, float)):
        return int(float(value))
    raw = str(value).strip().lower().replace(",", "")
    multiplier = 1
    if raw.endswith("k"):
        multiplier = 1000
        raw = raw[:-1]
    elif raw.endswith("m"):
        multiplier = 1000000
        raw = raw[:-1]
    elif raw.endswith("万"):
        multiplier = 10000
        raw = raw[:-1]
    match = re.search(r"-?\d+(?:\.\d+)?", raw)
    if not match:
        return 0
    return int(float(match.group(0)) * multiplier)


def parse_percent(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    if isinstance(value, (int, float)):
        number = float(value)
        return round(number * 100, 2) if 0 < number <= 1 else round(number, 2)
    raw = str(value).strip().replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", raw)
    if not match:
        return 0.0
    number = float(match.group(0))
    if "%" not in raw and 0 < number <= 1:
        number *= 100
    return round(number, 2)


def parse_score(value: Any, fallback: float) -> int:
    if value in (None, ""):
        return int(fallback)
    number = parse_percent(value)
    if 0 < number <= 1:
        number *= 100
    return int(max(0, min(100, round(number))))


def score_candidate(candidate: dict[str, Any]) -> tuple[int, dict[str, int]]:
    followers = int(candidate.get("followers") or 0)
    engagement = float(candidate.get("engagementRate") or 0)
    content_fit = int(candidate.get("contentFit") or 0)
    audience_fit = int(candidate.get("audienceFit") or 0)
    brand_safety = int(candidate.get("brandSafety") or 0)
    collab_signal = int(candidate.get("collabSignal") or 0)
    contact_method = candidate.get("contactMethod")

    if 5000 <= followers <= 80000:
        follower_score = 18
    elif 80000 < followers <= 180000:
        follower_score = 15
    elif 2000 <= followers < 5000:
        follower_score = 11
    elif 180000 < followers <= 500000:
        follower_score = 10
    elif followers > 0:
        follower_score = 6
    else:
        follower_score = 0

    engagement_score = int(min(22, max(0, engagement / 6 * 22)))
    content_score = int(content_fit / 100 * 20)
    audience_score = int(audience_fit / 100 * 16)
    safety_score = int(brand_safety / 100 * 8)
    collab_score = int(collab_signal / 100 * 10)
    contact_score = {"email": 6, "creator_marketplace": 6, "dm": 3}.get(str(contact_method), 0)
    completeness_score = 0
    completeness_score += 2 if candidate.get("notes") else 0
    completeness_score += 2 if candidate.get("tags") else 0
    completeness_score += 2 if candidate.get("topPosts") else 0

    breakdown = {
        "followers": follower_score,
        "engagement": engagement_score,
        "content": content_score,
        "audience": audience_score,
        "safety": safety_score,
        "collab": collab_score,
        "contact": contact_score,
        "data": completeness_score,
    }
    return min(100, sum(breakdown.values())), breakdown


def build_score_breakdown_items(breakdown: dict[str, int]) -> list[dict[str, Any]]:
    return [
        {
            "key": key,
            "label": label,
            "value": int(breakdown.get(key, 0)),
            "max": max_points,
            "pct": round(int(breakdown.get(key, 0)) / max_points * 100, 1) if max_points else 0,
        }
        for key, label, max_points in SCORE_FIELDS
    ]


def tier_for_score(score: int) -> str:
    if score >= 86:
        return "S"
    if score >= 74:
        return "A"
    if score >= 62:
        return "B"
    if score >= 48:
        return "C"
    return "D"


def next_action(candidate: dict[str, Any], score: int) -> str:
    status = candidate.get("status")
    if status == "contacted":
        if candidate.get("followUpDate"):
            return f"{candidate['followUpDate']} 跟进回复"
        return "3日後に返信確認"
    if status in {"replied", "negotiating"}:
        return "条件と投稿形式を整理"
    if status == "approved":
        return "商品選定と発送情報を確認"
    if status == "rejected":
        return "候補から除外"
    if score >= 74 and candidate.get("contactMethod") in {"email", "creator_marketplace"}:
        return "本文を確認して送信"
    if score >= 62:
        return "最近投稿とコメント品質を確認"
    return "保留または追加調査"


def build_manual_checklist(candidate: dict[str, Any]) -> list[dict[str, str]]:
    contact = candidate.get("contactMethod")
    items = [
        ("recent_posts", "最近10投稿がブランドと合う"),
        ("comments", "コメントが自然で購入層に近い"),
        ("pr_history", "PR表記と過去案件に不自然さがない"),
        ("terms", "条件、二次利用、投稿期限を送信前に確認"),
    ]
    if contact == "dm":
        items.append(("dm_review", "DM本文は人が確認してから送る"))
    if not candidate.get("email") and contact == "email":
        items.append(("email_missing", "メールアドレスを確認"))
    return [{"id": key, "label": label} for key, label in items]


def build_outreach_drafts(candidate: dict[str, Any]) -> dict[str, str]:
    name = candidate.get("name") or f"@{candidate.get('handle', '')}"
    handle = candidate.get("handle")
    niche = candidate.get("niche") or "ファッション"
    tags = "、".join(candidate.get("tags") or [niche])
    recent_hook = choose_recent_hook(candidate)
    product_angle = product_angle_for(candidate)

    dm = (
        f"{name}さん、はじめまして。突然のご連絡失礼します。\n\n"
        f"レディースファッションブランド {DEFAULT_BRAND['name']} のPR担当です。"
        f"{recent_hook}、{DEFAULT_BRAND['name']} の{product_angle}と相性が良いと感じ、ご連絡しました。\n\n"
        f"もしご興味があれば、商品提供を含めたInstagramでのご紹介について一度ご相談できますでしょうか。"
        f"無理な投稿指定ではなく、{name}さんの普段の雰囲気に合わせた形で進められれば嬉しいです。\n\n"
        "ご確認いただけましたら幸いです。よろしくお願いいたします。"
    )
    email_subject = f"【{DEFAULT_BRAND['name']}】Instagramタイアップのご相談"
    email = (
        f"{name}様\n\n"
        f"はじめまして。{DEFAULT_BRAND['name']} のPR担当です。\n"
        f"Instagram（@{handle}）の{tags}に関する投稿を拝見し、"
        f"{recent_hook}点がとても印象的でした。\n\n"
        f"{DEFAULT_BRAND['name']} は、{DEFAULT_BRAND['audience']}に向けた"
        f"{DEFAULT_BRAND['category']}ブランドです。今回、{product_angle}を中心に、"
        "投稿またはリールでのご紹介をご相談できればと思いご連絡しました。\n\n"
        "可能でしたら、対応可能な投稿形式、概算費用、商品提供の可否、二次利用の条件を"
        "ご教示いただけますでしょうか。\n\n"
        "どうぞよろしくお願いいたします。\n"
        f"{DEFAULT_BRAND['name']} PR"
    )
    followup = (
        f"{name}さん、先日 {DEFAULT_BRAND['name']} のPR相談でご連絡した件で、"
        "念のため再度ご連絡しました。\n\n"
        "ご興味がなければご返信不要です。もし条件確認だけでも可能でしたら、"
        "投稿形式とご料金の目安を伺えますと幸いです。"
    )
    return {
        "dm": dm,
        "emailSubject": email_subject,
        "email": email,
        "followup": followup,
    }


def generate_copy_draft(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "invalid payload"}
    raw_candidate = payload.get("candidate") if isinstance(payload.get("candidate"), dict) else {}
    options = payload.get("options") if isinstance(payload.get("options"), dict) else {}
    candidate = normalize_candidate(raw_candidate)
    provider = text(payload.get("provider") or options.get("provider") or os.getenv("OUTREACH_COPY_MODEL_PROVIDER", "local")).lower()
    fallback_text = build_copy_fallback_text(candidate, options)
    fallback_subject = build_copy_subject(candidate, options)
    prompt = build_copy_model_prompt(candidate, options)
    base_result = {
        "ok": True,
        "provider": "local",
        "configured": False,
        "text": fallback_text,
        "subject": fallback_subject,
        "prompt": prompt,
        "warnings": [],
    }
    if provider not in {"api", "model", "openai", "openai_compatible", "cpa"}:
        return base_result

    config = resolve_copy_model_config(payload)
    if not config.get("baseUrl") or not config.get("model"):
        base_result["provider"] = "openai_compatible"
        base_result["warnings"] = ["模型接口未配置完整，已使用本地规则生成。"]
        return base_result
    try:
        model_result = call_openai_compatible_copy_model(config, prompt)
    except (OSError, TimeoutError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError) as exc:
        base_result["provider"] = "openai_compatible"
        base_result["warnings"] = [f"模型接口调用失败，已使用本地规则生成：{exc}"]
        return base_result
    text_value = text(model_result.get("text"))
    if not text_value:
        base_result["provider"] = "openai_compatible"
        base_result["warnings"] = ["模型返回为空，已使用本地规则生成。"]
        return base_result
    return {
        "ok": True,
        "provider": "openai_compatible",
        "configured": True,
        "model": config.get("model"),
        "text": text_value,
        "subject": text(model_result.get("subject")) or fallback_subject,
        "prompt": prompt,
        "warnings": [],
    }


def generate_reply_draft(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "invalid payload"}
    reply_text = text(payload.get("replyText"))
    if not reply_text:
        return {"ok": False, "error": "missing reply text"}
    raw_candidate = payload.get("candidate") if isinstance(payload.get("candidate"), dict) else {}
    candidate = normalize_candidate(raw_candidate)
    provider = text(payload.get("provider") or os.getenv("OUTREACH_COPY_MODEL_PROVIDER", "local")).lower()
    category = classify_creator_reply(reply_text)
    fallback_text = build_reply_fallback_text(candidate, category["key"])
    base_result = {
        "ok": True,
        "provider": "local",
        "configured": False,
        "key": category["key"],
        "label": category["label"],
        "status": category["status"],
        "draft": fallback_text,
        "note": f"达人回复识别：{category['label']}\n{reply_text[:300]}",
        "warnings": [],
    }
    if provider not in {"api", "model", "openai", "openai_compatible", "cpa"}:
        return base_result

    config = resolve_copy_model_config({**payload, "maxTokens": payload.get("maxTokens") or 700})
    if not config.get("baseUrl") or not config.get("model"):
        base_result["provider"] = "openai_compatible"
        base_result["warnings"] = ["模型接口未配置完整，已使用本地规则生成。"]
        return base_result
    try:
        model_result = call_openai_compatible_copy_model(config, build_reply_model_prompt(candidate, reply_text, category))
    except (OSError, TimeoutError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError) as exc:
        base_result["provider"] = "openai_compatible"
        base_result["warnings"] = [f"模型接口调用失败，已使用本地规则生成：{exc}"]
        return base_result
    model_text = text(model_result.get("text"))
    if not model_text:
        base_result["provider"] = "openai_compatible"
        base_result["warnings"] = ["模型返回为空，已使用本地规则生成。"]
        return base_result
    return {
        **base_result,
        "provider": "openai_compatible",
        "configured": True,
        "model": config.get("model"),
        "draft": model_text,
        "warnings": [],
    }


def classify_creator_reply(reply_text: str) -> dict[str, str]:
    rules = [
        {
            "key": "rejected",
            "label": "拒绝 / 暂不合作",
            "status": "rejected",
            "pattern": r"難しい|見送り|できません|不可|忙しい|興味.*ない|今回は|すみません|ごめんなさい|not interested|decline|拒绝",
        },
        {
            "key": "price",
            "label": "报价 / 费用",
            "status": "negotiating",
            "pattern": r"円|¥|料金|費用|単価|見積|お見積|rate|fee|price|报价|報酬",
        },
        {
            "key": "product_request",
            "label": "想看商品 / 图片",
            "status": "replied",
            "pattern": r"商品|写真|画像|url|詳細|ラインナップ|どんな|product|image|素材",
        },
        {
            "key": "condition",
            "label": "询问条件",
            "status": "replied",
            "pattern": r"条件|納期|投稿|二次利用|pr表記|スケジュール|いつ|形式|媒体|timeline|usage",
        },
        {
            "key": "interested",
            "label": "有兴趣",
            "status": "replied",
            "pattern": r"興味|ぜひ|可能|大丈夫|お願いします|検討|詳しく|前向き|ok|interested",
        },
    ]
    for rule in rules:
        if re.search(rule["pattern"], reply_text, re.IGNORECASE):
            return {key: rule[key] for key in ["key", "label", "status"]}
    return {"key": "needs_reply", "label": "需要人工判断", "status": "replied"}


def build_reply_fallback_text(candidate: dict[str, Any], key: str) -> str:
    brand = DEFAULT_BRAND["name"]
    name = candidate.get("name") or f"@{candidate.get('handle', '')}"
    product = product_angle_for(candidate)
    if key == "rejected":
        return (
            f"{name}さん、ご返信ありがとうございます。\n\n"
            "承知いたしました。ご丁寧にお返事いただきありがとうございます。\n"
            "またタイミングや企画内容が合いそうな機会がありましたら、改めてご相談させていただけますと幸いです。\n\n"
            "今後ともどうぞよろしくお願いいたします。"
        )
    if key == "price":
        return (
            f"{name}さん、ご返信ありがとうございます。\n\n"
            "条件をご共有いただきありがとうございます。社内で確認いたしますので、念のため投稿形式、投稿本数、二次利用の可否、掲載期間、商品提供の扱いについても教えていただけますでしょうか。\n\n"
            f"今回まずは{product}での初回タイアップを想定しています。条件が合えば継続企画もご相談できればと思っております。"
        )
    if key == "product_request":
        return (
            f"{name}さん、ご返信ありがとうございます。\n\n"
            f"もちろんです。今回は{brand}の{product}を中心にご紹介できればと考えています。\n"
            "商品画像、候補アイテム、条件の概要を整理してお送りします。\n\n"
            "ご覧いただいたうえで、気になるアイテムや投稿しやすい形式があれば教えていただけますでしょうか。"
        )
    if key == "condition":
        return (
            f"{name}さん、ご返信ありがとうございます。\n\n"
            "条件について、現時点では商品提供を含めたInstagramでのご紹介を想定しています。投稿内容は普段の雰囲気に合わせ、PR表記、投稿期限、二次利用の有無は事前に確認して進めたいです。\n\n"
            "対応可能な投稿形式と概算費用を教えていただけますでしょうか。"
        )
    if key == "interested":
        return (
            f"{name}さん、ご返信ありがとうございます。ご興味を持っていただけて嬉しいです。\n\n"
            f"今回は{brand}の{product}をご紹介いただけないかと考えています。\n"
            "まずは候補商品と条件概要をお送りしますので、投稿しやすい形式やご希望条件があれば教えていただけますでしょうか。"
        )
    return (
        f"{name}さん、ご返信ありがとうございます。\n\n"
        f"内容確認いたしました。今回のご相談について、{brand}側で進め方を整理したうえでご返信いたします。\n"
        "念のため、対応可能な投稿形式、概算費用、商品提供の可否を教えていただけますでしょうか。"
    )


def build_reply_model_prompt(candidate: dict[str, Any], reply_text: str, category: dict[str, str]) -> list[dict[str, str]]:
    compact_candidate = {
        key: candidate.get(key)
        for key in [
            "handle",
            "name",
            "niche",
            "location",
            "followers",
            "engagementRate",
            "contactMethod",
            "tags",
            "notes",
            "collabProduct",
            "quoteJpy",
            "partnershipStage",
        ]
    }
    instruction = (
        "You help a Japanese fashion brand reply to Instagram creator collaboration messages. "
        "Write only a concise Japanese reply that is ready for human review. "
        "Do not invent concrete fees, URLs, dates, tracking numbers, or product names. "
        "Return JSON only with keys: subject, text. Leave subject empty unless an email subject is clearly useful."
    )
    user_payload = {
        "brand": DEFAULT_BRAND,
        "candidate": compact_candidate,
        "creatorReply": reply_text[:2500],
        "detectedCategory": category,
        "requirements": [
            "Japanese",
            "respectful and natural",
            "answer the creator's likely intent",
            "ask for the minimum next information needed",
            "do not say the message was already sent",
            "avoid pressure and overpromising",
        ],
    }
    return [
        {"role": "system", "content": instruction},
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
    ]


def test_copy_model_config(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "invalid payload"}
    provider = text(payload.get("provider") or os.getenv("OUTREACH_COPY_MODEL_PROVIDER", "local")).lower()
    if provider not in {"api", "model", "openai", "openai_compatible", "cpa"}:
        return {"ok": True, "provider": "local", "configured": False, "message": "local provider"}
    config = resolve_copy_model_config({**payload, "maxTokens": payload.get("maxTokens") or 80})
    if not config.get("baseUrl") or not config.get("model"):
        return {"ok": False, "provider": "openai_compatible", "configured": False, "error": "missing base URL or model"}
    messages = [
        {"role": "system", "content": "Return JSON only."},
        {"role": "user", "content": "{\"subject\":\"ok\",\"text\":\"ok\"}"},
    ]
    try:
        result = call_openai_compatible_copy_model(config, messages)
    except (OSError, TimeoutError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError) as exc:
        return {"ok": False, "provider": "openai_compatible", "configured": True, "model": config.get("model"), "error": str(exc)}
    return {
        "ok": bool(text(result.get("text")) or text(result.get("subject"))),
        "provider": "openai_compatible",
        "configured": True,
        "model": config.get("model"),
        "sample": text(result.get("text"))[:120],
    }


def resolve_copy_model_config(payload: dict[str, Any]) -> dict[str, Any]:
    provider = text(payload.get("provider") or os.getenv("OUTREACH_COPY_MODEL_PROVIDER", "local")).lower()
    return {
        "provider": provider,
        "baseUrl": text(payload.get("apiBaseUrl")) or os.getenv("OUTREACH_COPY_MODEL_BASE_URL", ""),
        "apiKey": text(payload.get("apiKey")) or os.getenv("OUTREACH_COPY_MODEL_API_KEY", ""),
        "model": text(payload.get("model")) or os.getenv("OUTREACH_COPY_MODEL_NAME", ""),
        "authMode": normalize_copy_auth_mode(payload.get("authMode") or os.getenv("OUTREACH_COPY_MODEL_AUTH_MODE", "")),
        "compatMode": text(payload.get("compatMode") or os.getenv("OUTREACH_COPY_MODEL_COMPAT_MODE", "")) or ("cpa" if provider == "cpa" else "openai"),
        "timeout": parse_count(payload.get("timeoutSeconds") or os.getenv("OUTREACH_COPY_MODEL_TIMEOUT", "30")) or 30,
        "temperature": parse_float(payload.get("temperature"), 0.65),
        "maxTokens": parse_count(payload.get("maxTokens") or os.getenv("OUTREACH_COPY_MODEL_MAX_TOKENS", "900")) or 900,
    }


def normalize_copy_auth_mode(value: Any) -> str:
    raw = text(value).lower()
    if raw in {"x-api-key", "x_api_key", "apikey", "api-key"}:
        return "x-api-key"
    if raw in {"authorization", "raw", "authorization_raw"}:
        return "authorization"
    if raw in {"none", "no_auth", "off"}:
        return "none"
    return "bearer"


def build_copy_fallback_text(candidate: dict[str, Any], options: dict[str, Any]) -> str:
    brand = DEFAULT_BRAND["name"]
    name = candidate.get("name") or f"@{candidate.get('handle', '')}"
    niche = candidate.get("niche") or "fashion / lifestyle"
    scenario = text(options.get("scenario") or "product_seed")
    tone = text(options.get("tone") or "warm")
    length = text(options.get("length") or "standard")
    hook = text(options.get("hook")) or choose_recent_hook(candidate)
    product = text(options.get("productLabel") or options.get("productAngle")) or product_angle_for(candidate)
    ask = {
        "paid_post": "投稿形式、料金目安、二次利用の可否について一度ご相談できますでしょうか。",
        "reels": "Reelsでの自然な着用紹介について、条件を一度ご相談できますでしょうか。",
        "affiliate": "商品提供に加えて、専用コードや成果報酬型の形もご相談できますでしょうか。",
        "long_term": "単発だけでなく、季節ごとの継続的な企画も含めてご相談できれば嬉しいです。",
        "followup_second": "先日のご連絡について念のため再度ご連絡しました。ご興味がなければ返信不要です。",
        "negotiate": "条件を拝見し、初回は商品提供を含めた小さめの形から調整できないかご相談したいです。",
    }.get(scenario, "商品提供を中心に、普段の投稿の雰囲気に合わせた自然なご紹介をご相談できますでしょうか。")
    opener = "突然のご連絡失礼いたします。" if tone != "concise" else "はじめまして。"
    detail = (
        f"\n\n{brand}は日本向けのレディースファッションブランドで、通勤や休日に使いやすい大人向けアイテムを扱っています。"
        if length == "detailed"
        else ""
    )
    return (
        f"{name}さん、{opener}\n\n"
        f"{brand}のPR担当です。{niche}に関する投稿を拝見し、{hook}\n"
        f"{brand}の{product}と相性が良いと感じ、ご連絡しました。{detail}\n\n"
        f"{ask}\n\n"
        "投稿内容は無理に指定せず、普段の雰囲気に合う形を大切にしたいです。"
        "ご確認いただけましたら幸いです。よろしくお願いいたします。"
    )


def build_copy_subject(candidate: dict[str, Any], options: dict[str, Any]) -> str:
    brand = DEFAULT_BRAND["name"]
    scenario = text(options.get("scenario"))
    if scenario in {"paid_post", "reels", "long_term"}:
        return f"【{brand}】Instagramタイアップのご相談"
    return f"【{brand}】商品提供・PRのご相談"


def build_copy_model_prompt(candidate: dict[str, Any], options: dict[str, Any]) -> list[dict[str, str]]:
    compact_candidate = {
        key: candidate.get(key)
        for key in [
            "handle",
            "name",
            "niche",
            "location",
            "followers",
            "engagementRate",
            "contactMethod",
            "email",
            "tags",
            "notes",
            "topPosts",
        ]
    }
    instruction = (
        "You write concise Japanese outreach copy for Instagram creator collaborations. "
        "Use a respectful, natural tone. Do not invent facts. "
        "Return JSON only with keys: subject, text. The text should be ready to send after human review."
    )
    user_payload = {
        "brand": DEFAULT_BRAND,
        "candidate": compact_candidate,
        "options": options,
        "requirements": [
            "Japanese",
            "personalized opening",
            "clear collaboration ask",
            "no pressure",
            "no claim that a message has already been sent",
        ],
    }
    return [
        {"role": "system", "content": instruction},
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
    ]


def call_openai_compatible_copy_model(config: dict[str, Any], messages: list[dict[str, str]]) -> dict[str, str]:
    target = normalize_chat_completions_url(text(config.get("baseUrl")))
    body = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": int(config.get("maxTokens") or 900),
    }
    if config.get("compatMode") != "cpa":
        body["temperature"] = float(config.get("temperature") or 0.65)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "InstagramCreatorOutreach/0.1",
    }
    apply_model_auth_header(headers, config)
    request = urllib.request.Request(
        target,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=int(config.get("timeout") or 30)) as response:
            raw_payload = response.read(2_000_000)
    except urllib.error.HTTPError as exc:
        raise ValueError(format_model_http_error(exc, config)) from exc
    parsed = json.loads(raw_payload.decode("utf-8"))
    content = extract_chat_completion_text(parsed)
    return parse_model_copy_content(content)


def apply_model_auth_header(headers: dict[str, str], config: dict[str, Any]) -> None:
    api_key = text(config.get("apiKey"))
    if not api_key:
        return
    auth_mode = normalize_copy_auth_mode(config.get("authMode"))
    if auth_mode == "none":
        return
    if auth_mode == "x-api-key":
        headers["X-API-Key"] = api_key
        return
    if auth_mode == "authorization":
        headers["Authorization"] = api_key
        return
    headers["Authorization"] = f"Bearer {api_key}"


def format_model_http_error(exc: urllib.error.HTTPError, config: dict[str, Any]) -> str:
    try:
        payload = exc.read(4096).decode("utf-8", errors="replace")
    except OSError:
        payload = ""
    payload = sanitize_model_error(payload, config)
    detail = f": {payload}" if payload else ""
    return f"HTTP {exc.code} {exc.reason}{detail}"


def sanitize_model_error(message: str, config: dict[str, Any]) -> str:
    clean = text(message)
    api_key = text(config.get("apiKey"))
    if api_key:
        clean = clean.replace(api_key, "***")
    clean = re.sub(r"sk-[A-Za-z0-9_-]{8,}", "sk-***", clean)
    return clean[:800]


def normalize_chat_completions_url(base_url: str) -> str:
    clean = base_url.strip().rstrip("/")
    if not re.match(r"^https?://", clean, re.IGNORECASE):
        raise ValueError("invalid model base URL")
    if clean.endswith("/chat/completions"):
        return clean
    if clean.endswith("/v1"):
        return f"{clean}/chat/completions"
    return f"{clean}/v1/chat/completions"


def extract_chat_completion_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") if isinstance(payload, dict) else []
    if not choices:
        return ""
    first = choices[0] if isinstance(choices[0], dict) else {}
    message = first.get("message") if isinstance(first.get("message"), dict) else {}
    return text(message.get("content") or first.get("text"))


def parse_model_copy_content(content: str) -> dict[str, str]:
    clean = text(content)
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.IGNORECASE)
        clean = re.sub(r"\s*```$", "", clean)
    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError:
        return {"text": clean, "subject": ""}
    if isinstance(parsed, dict):
        return {"text": text(parsed.get("text") or parsed.get("body")), "subject": text(parsed.get("subject"))}
    return {"text": clean, "subject": ""}


def parse_float(value: Any, fallback: float) -> float:
    if value in (None, ""):
        return fallback
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def choose_recent_hook(candidate: dict[str, Any]) -> str:
    posts = candidate.get("topPosts") or []
    if posts:
        return f"特に「{posts[0]}」の投稿の見せ方が自然で"
    niche = candidate.get("niche") or "ファッション"
    return f"{niche}の投稿の雰囲気が自然で"


def product_angle_for(candidate: dict[str, Any]) -> str:
    text_blob = " ".join(
        [
            str(candidate.get("niche") or ""),
            " ".join(candidate.get("tags") or []),
            " ".join(candidate.get("topPosts") or []),
        ]
    )
    if "低身長" in text_blob:
        return "低身長でもバランスを取りやすいワンピースや高腰パンツ"
    if "オフィス" in text_blob or "通勤" in text_blob:
        return "通勤にも使いやすいきれいめカジュアル"
    if "ママ" in text_blob or "体型" in text_blob:
        return "体型カバーしやすく日常で着回せるアイテム"
    if "淡色" in text_blob:
        return "淡色でまとめやすい大人カジュアル"
    return "大人向けの着回ししやすい新作アイテム"


def summarize_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(candidates)
    if not total:
        return {
            "total": 0,
            "ready": 0,
            "avgScore": 0,
            "contacted": 0,
            "needsReview": 0,
            "estimatedCostJpy": 0,
            "partnershipActive": 0,
            "partnershipPosted": 0,
            "partnershipOrders": 0,
            "partnershipRevenueJpy": 0,
            "partnershipCostJpy": 0,
            "partnershipRoiPct": 0,
            "byStatus": {},
            "byTier": {},
        }
    by_status: dict[str, int] = {}
    by_tier: dict[str, int] = {}
    for row in candidates:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
        by_tier[row["tier"]] = by_tier.get(row["tier"], 0) + 1
    partnership_cost = sum(int(row.get("quoteJpy") or 0) + int(row.get("sampleCostJpy") or 0) for row in candidates)
    partnership_revenue = sum(int(row.get("revenueJpy") or 0) for row in candidates)
    partnership_roi = round(((partnership_revenue - partnership_cost) / partnership_cost) * 100, 1) if partnership_cost else 0
    return {
        "total": total,
        "ready": sum(1 for row in candidates if row["score"] >= 74 and row["status"] != "rejected"),
        "avgScore": round(sum(row["score"] for row in candidates) / total, 1),
        "contacted": sum(1 for row in candidates if row["status"] in {"contacted", "replied", "negotiating", "approved"}),
        "needsReview": sum(1 for row in candidates if row["status"] in {"new", "review"}),
        "estimatedCostJpy": sum(int(row.get("priceHintJpy") or 0) for row in candidates if row["score"] >= 74),
        "partnershipActive": sum(1 for row in candidates if row.get("partnershipStage") not in {"", "none"}),
        "partnershipPosted": sum(1 for row in candidates if row.get("partnershipStage") in {"posted", "measured"} or row.get("postUrl")),
        "partnershipOrders": sum(int(row.get("orders") or 0) for row in candidates),
        "partnershipRevenueJpy": partnership_revenue,
        "partnershipCostJpy": partnership_cost,
        "partnershipRoiPct": partnership_roi,
        "byStatus": by_status,
        "byTier": by_tier,
    }


def build_discovery_plan() -> dict[str, Any]:
    hashtag_rows = []
    for tag in DISCOVERY_HASHTAGS:
        hashtag_rows.append(
            {
                "label": f"#{tag}",
                "instagramUrl": f"https://www.instagram.com/explore/tags/{quote(tag)}/",
                "googleUrl": google_url(f'site:instagram.com/explore/tags "{tag}"'),
            }
        )
    query_rows = []
    templates = [
        'site:instagram.com "{keyword}" "PR" "メール"',
        'site:instagram.com "{keyword}" "タイアップ" "ファッション"',
        'site:instagram.com "{keyword}" "商品提供" "コーデ"',
        'site:instagram.com "{keyword}" "骨格" "着回し"',
    ]
    for keyword in DISCOVERY_KEYWORDS:
        for template in templates[:2]:
            query = template.format(keyword=keyword)
            query_rows.append({"label": keyword, "query": query, "url": google_url(query)})
    marketplace = [
        {
            "label": "Meta Business Suite",
            "url": "https://business.facebook.com/",
            "note": "Creator Marketplaceで日本、女性ファッション、エンゲージメント条件を絞る",
        },
        {
            "label": "Instagram inbox",
            "url": "https://www.instagram.com/direct/inbox/",
            "note": "送信前レビュー済みのDMだけ手動で送る",
        },
    ]
    return {
        "hashtags": hashtag_rows,
        "queries": query_rows[:16],
        "marketplace": marketplace,
        "keywords": DISCOVERY_KEYWORDS,
        "guardrails": [
            "大量自動DMを避け、候補ごとに本文を確認する",
            "公開メール、Creator Marketplace、返信済みDMを優先する",
            "PR表記、二次利用、投稿期限、報酬条件を送信前に明記する",
        ],
    }


def build_skill_panel_payload() -> dict[str, Any]:
    return {
        "skillDir": str(INSTAGRAM_DM_SKILL_DIR),
        "outputDir": str(SKILL_HARVEST_OUTPUT_DIR),
        "defaultSeeds": DEFAULT_SKILL_SEED_HASHTAGS,
        "defaultExclusions": DEFAULT_SKILL_EXCLUSION_RULES,
        "runs": list_skill_harvest_runs(),
    }


def normalize_seed_terms(value: Any) -> list[str]:
    if isinstance(value, list):
        raw_parts = [text(item) for item in value]
    else:
        raw_parts = re.split(r"[\n,，\s]+", text(value))
    seeds: list[str] = []
    for part in raw_parts:
        clean = text(part).strip()
        if not clean:
            continue
        if clean.startswith("#"):
            clean = "#" + clean.lstrip("#").strip()
        if clean not in seeds:
            seeds.append(clean)
    return seeds[:80]


def normalize_rule_lines(value: Any) -> list[str]:
    if isinstance(value, list):
        raw_parts = [text(item) for item in value]
    else:
        raw_parts = re.split(r"[\r\n]+", text(value))
    rules: list[str] = []
    for part in raw_parts:
        clean = text(part).strip(" \t-•、,，;；")
        if clean and clean not in rules:
            rules.append(clean)
    return rules[:80]


def skill_harvest_options(payload: dict[str, Any] | None) -> dict[str, Any]:
    payload = payload or {}
    seeds = normalize_seed_terms(payload.get("seedTerms") or payload.get("seeds"))
    if not seeds:
        seeds = list(DEFAULT_SKILL_SEED_HASHTAGS)
    exclusion_rules = normalize_rule_lines(payload.get("exclusionRules") or payload.get("exclusions"))
    if not exclusion_rules:
        exclusion_rules = list(DEFAULT_SKILL_EXCLUSION_RULES)
    market = text(payload.get("market")) or "Japan"
    language = text(payload.get("language")) or "日语"
    niche = text(payload.get("niche")) or "レディースファッション、40代コーデ、服"
    source_mode = text(payload.get("sourceMode")) or "instagram"
    if source_mode not in {"instagram", "hybrid", "competitor"}:
        source_mode = "instagram"
    min_followers = max(0, parse_count(payload.get("minFollowers")) or 10000)
    max_followers = max(min_followers, parse_count(payload.get("maxFollowers")) or 100000)
    per_term_limit = max(1, min(parse_count(payload.get("perTermLimit")) or 80, 200))
    raw_target = max(1, min(parse_count(payload.get("rawTarget")) or 200, 2000))
    top_target = max(1, min(parse_count(payload.get("topTarget")) or 50, raw_target))
    return {
        "market": market,
        "language": language,
        "niche": niche,
        "sourceMode": source_mode,
        "seedTerms": seeds,
        "minFollowers": min_followers,
        "maxFollowers": max_followers,
        "perTermLimit": per_term_limit,
        "rawTarget": raw_target,
        "topTarget": top_target,
        "strictFilter": bool(payload.get("strictFilter", True)),
        "fullAngle": bool(payload.get("fullAngle", True)),
        "exclusionRules": exclusion_rules,
    }


def build_skill_harvest_prompt(payload: dict[str, Any] | None) -> dict[str, Any]:
    options = skill_harvest_options(payload)
    seed_block = "\n".join(f"  {seed}" for seed in options["seedTerms"])
    exclusion_block = "\n".join(f"  - {rule}" for rule in options["exclusionRules"])
    source_line = {
        "instagram": "控制浏览器在 Instagram 内部关键词/hashtag 全角度发现日本女装达人，只导出 CSV，不私信。",
        "hybrid": "结合 Google/public search 和 Instagram 内部关键词/hashtag 全角度发现日本女装达人，只导出 CSV，不私信。",
        "competitor": "以竞品账号/公开线索为种子发现日本女装达人，只抓公开可见信息，只导出 CSV，不私信。",
    }[options["sourceMode"]]
    strict_line = (
        f"- 开启 strict female creator filter：只保留女性个人穿搭/女装达人，排除：{STRICT_FEMALE_CREATOR_REJECT_TEXT}"
        if options["strictFilter"]
        else "- 使用普通过滤：排除明显不相关、私密、抽奖和品牌店铺号"
    )
    full_angle = (
        "- 开启 full-angle 扩展：风格词、年龄词、体型词、季节词、场景词、单品词、穿搭词、价格感词、合作意向词、相关 hashtag、近义词和组合词"
        if options["fullAngle"]
        else "- 只使用输入的种子关键词/hashtag"
    )
    prompt = f"""使用 $instagram-dm-outreach，{source_line}

要求：
- 语言：{options["language"]}
- 地区：{options["market"]}
- 粉丝：{options["minFollowers"]}-{options["maxFollowers"]}
- 类型：{options["niche"]}
- 种子关键词/hashtag：
{seed_block}
{full_angle}
- 合作信号：PR、お仕事依頼、企業案件、アンバサダー、提供、タイアップ、コラボ、お問い合わせ
{strict_line}
- 面板排除规则：采集阶段先跳过，最终达人池导入 CSV 不保留以下账号；如果不确定，放到候选详情 CSV 并标记 needs_review，不要补进 top：
{exclusion_block}
- 每个关键词/hashtag 最多采集 {options["perTermLimit"]} 个可见帖子/Reels 作者
- 打开候选主页补全公开信息
- 使用可续跑模式
- 先采集 {options["rawTarget"]} 个候选，去重后保留 top {options["topTarget"]}
- 输出：
  1. 达人池导入 CSV
  2. 候选详情 CSV

安全边界：
- 只抓公开可见信息
- 不私信
- 不抓完整粉丝/关注列表
- 不使用隐藏 API、cookie、localStorage、network payload
"""
    return {"ok": True, "options": options, "prompt": prompt}


def create_skill_harvest_plan(payload: dict[str, Any] | None) -> dict[str, Any]:
    prompt_payload = build_skill_harvest_prompt(payload)
    options = prompt_payload["options"]
    SKILL_HARVEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = text((payload or {}).get("runId")) or datetime.now().strftime("%Y-%m-%d_jp_womenswear_panel_%H%M%S")
    run_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", run_id).strip("_")[:90] or datetime.now().strftime("%Y-%m-%d_jp_panel_%H%M%S")
    plan_path = SKILL_HARVEST_OUTPUT_DIR / f"instagram_discovery_plan_{run_id}.csv"

    build_script = INSTAGRAM_DM_SKILL_DIR / "scripts" / "build_instagram_discovery_plan.py"
    manage_script = INSTAGRAM_DM_SKILL_DIR / "scripts" / "manage_instagram_harvest_run.py"
    if not build_script.exists() or not manage_script.exists():
        return {
            "ok": False,
            "error": "instagram-dm-outreach skill scripts not found",
            "skillDir": str(INSTAGRAM_DM_SKILL_DIR),
        }

    raw_multiplier = max(1, (int(options["rawTarget"]) + int(options["topTarget"]) - 1) // int(options["topTarget"]))
    cmd = [
        sys.executable,
        str(build_script),
        "--language",
        "ja",
        "--category",
        "fashion",
        "--target-final",
        str(options["topTarget"]),
        "--raw-multiplier",
        str(raw_multiplier),
        "--per-keyword-limit",
        str(options["perTermLimit"]),
        "--per-hashtag-limit",
        str(options["perTermLimit"]),
        "--format",
        "csv",
    ]
    if options["fullAngle"]:
        cmd.append("--full-angle")
    for seed in options["seedTerms"]:
        cmd.extend(["--seed", seed])

    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    try:
        built = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
        plan_path.write_text(built.stdout, encoding="utf-8-sig")
        init_cmd = [
            sys.executable,
            str(manage_script),
            "init",
            "--plan",
            str(plan_path),
            "--output-dir",
            str(SKILL_HARVEST_OUTPUT_DIR),
            "--run-id",
            run_id,
        ]
        initialized = subprocess.run(init_cmd, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    except subprocess.CalledProcessError as exc:
        return {
            "ok": False,
            "error": (exc.stderr or exc.stdout or str(exc))[:1600],
            "planPath": str(plan_path),
        }

    progress_path = SKILL_HARVEST_OUTPUT_DIR / f"instagram_harvest_progress_{run_id}.csv"
    raw_path = SKILL_HARVEST_OUTPUT_DIR / f"raw_instagram_harvest_{run_id}_working.csv"
    seen_path = SKILL_HARVEST_OUTPUT_DIR / "seen_creators.csv"
    return {
        "ok": True,
        "runId": run_id,
        "prompt": prompt_payload["prompt"],
        "options": options,
        "planPath": str(plan_path),
        "progressPath": str(progress_path),
        "rawPath": str(raw_path),
        "seenPath": str(seen_path),
        "stdout": initialized.stdout,
        "skillPanel": build_skill_panel_payload(),
    }


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    for encoding in ("utf-8-sig", "utf-8", "utf-16", "cp932", "gb18030"):
        try:
            with path.open("r", encoding=encoding, newline="") as fh:
                return list(csv.DictReader(fh))
        except UnicodeError:
            continue
        except OSError:
            return []
    return []


def list_skill_harvest_runs(limit: int = 8) -> list[dict[str, Any]]:
    if not SKILL_HARVEST_OUTPUT_DIR.exists():
        return []
    run_ids: set[str] = set()
    for path in SKILL_HARVEST_OUTPUT_DIR.glob("instagram_harvest_progress_*.csv"):
        run_ids.add(path.stem.removeprefix("instagram_harvest_progress_"))
    for path in SKILL_HARVEST_OUTPUT_DIR.glob("raw_instagram_harvest_*_working.csv"):
        run_ids.add(path.name.removeprefix("raw_instagram_harvest_").removesuffix("_working.csv"))

    rows = [summarize_skill_harvest_run(run_id) for run_id in run_ids]
    rows.sort(key=lambda item: item.get("updatedAt", ""), reverse=True)
    return rows[:limit]


def skill_harvest_run_files(run_id: str) -> list[Path]:
    clean_run_id = text(run_id)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}", clean_run_id):
        return []
    return [
        SKILL_HARVEST_OUTPUT_DIR / f"instagram_discovery_plan_{clean_run_id}.csv",
        SKILL_HARVEST_OUTPUT_DIR / f"instagram_harvest_progress_{clean_run_id}.csv",
        SKILL_HARVEST_OUTPUT_DIR / f"raw_instagram_harvest_{clean_run_id}_working.csv",
        SKILL_HARVEST_OUTPUT_DIR / f"raw_instagram_harvest_{clean_run_id}_deduped.csv",
    ]


def delete_skill_harvest_run(run_id: str) -> dict[str, Any]:
    clean_run_id = text(run_id)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}", clean_run_id):
        return {"ok": False, "error": "invalid runId", "deleted": [], "skillPanel": build_skill_panel_payload()}

    deleted: list[str] = []
    missing: list[str] = []
    for path in skill_harvest_run_files(clean_run_id):
        try:
            resolved = path.resolve()
            output_dir = SKILL_HARVEST_OUTPUT_DIR.resolve()
            if output_dir not in resolved.parents:
                continue
            if resolved.exists() and resolved.is_file():
                resolved.unlink()
                deleted.append(str(resolved))
            else:
                missing.append(str(resolved))
        except OSError:
            continue

    return {
        "ok": bool(deleted),
        "runId": clean_run_id,
        "deleted": deleted,
        "missing": missing,
        "error": "" if deleted else "run files not found",
        "skillPanel": build_skill_panel_payload(),
    }


def summarize_skill_harvest_run(run_id: str) -> dict[str, Any]:
    progress_path = SKILL_HARVEST_OUTPUT_DIR / f"instagram_harvest_progress_{run_id}.csv"
    raw_path = SKILL_HARVEST_OUTPUT_DIR / f"raw_instagram_harvest_{run_id}_working.csv"
    plan_path = SKILL_HARVEST_OUTPUT_DIR / f"instagram_discovery_plan_{run_id}.csv"
    progress_rows = read_csv_rows(progress_path)
    raw_rows = read_csv_rows(raw_path)
    handles = []
    for row in raw_rows:
        handle = normalize_handle(first_value(row, ["handle", "profile_url", "instagramUrl", "source_url"]))
        if handle:
            handles.append(handle.lower())
    status_counts: dict[str, int] = {}
    updated_at = ""
    for row in progress_rows:
        status = text(row.get("status")) or "pending"
        status_counts[status] = status_counts.get(status, 0) + 1
        updated_at = max(updated_at, text(row.get("updated_at")))
    for path in [raw_path, progress_path, plan_path]:
        if path.exists():
            updated_at = max(updated_at, datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"))
    return {
        "runId": run_id,
        "planPath": str(plan_path) if plan_path.exists() else "",
        "progressPath": str(progress_path) if progress_path.exists() else "",
        "rawPath": str(raw_path) if raw_path.exists() else "",
        "progressRows": len(progress_rows),
        "rawRows": len(raw_rows),
        "uniqueHandles": len(set(handles)),
        "statusCounts": status_counts,
        "updatedAt": updated_at,
    }


def google_url(query: str) -> str:
    return f"https://www.google.com/search?q={quote_plus(query)}"


def public_search_preview(
    keyword: str,
    engine: str = "auto",
    limit: int = 10,
) -> dict[str, Any]:
    clean_keyword = text(keyword) or "fashion blogger japan"
    clean_engine = text(engine).lower() or "auto"
    if clean_engine not in {"auto", "google_cse", "serpapi"}:
        clean_engine = "auto"
    max_results = max(1, min(parse_count(limit), 30))
    query = build_public_search_query(clean_keyword)
    selected_engine = choose_public_search_engine(clean_engine)
    configured = public_search_is_configured(selected_engine)
    source_text = ""
    results: list[dict[str, str]] = []
    error = ""
    if configured:
        try:
            results = fetch_public_search_results(query, selected_engine, max_results)
            source_text = format_public_search_source(results)
        except (OSError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            error = str(exc)
    preview = preview_discovery_candidates(
        source_text,
        keyword=clean_keyword,
        source_label=f"public_search:{selected_engine}",
    )
    return {
        **preview,
        "engine": selected_engine,
        "configured": configured,
        "query": query,
        "searchUrl": google_url(query),
        "resultCount": len(results),
        "sourceText": source_text,
        "error": error,
        "setup": public_search_setup_state(),
    }


def build_public_search_query(keyword: str) -> str:
    raw_keyword = text(keyword)
    lines = [part.strip() for part in raw_keyword.splitlines() if part.strip()]
    if len(lines) > 1 and "site:instagram.com" not in raw_keyword.lower():
        quoted = " OR ".join(f'"{line}"' for line in lines)
        return f"site:instagram.com ({quoted})"
    clean_keyword = re.sub(r"\s+", " ", raw_keyword).strip()
    if not clean_keyword:
        clean_keyword = "fashion blogger japan"
    if "site:instagram.com" in clean_keyword.lower():
        return clean_keyword
    return f'site:instagram.com "{clean_keyword}"'


def public_search_setup_state() -> dict[str, bool]:
    return {
        "googleCse": bool(os.getenv("GOOGLE_CSE_API_KEY") and public_search_google_cx()),
        "serpApi": bool(os.getenv("SERPAPI_API_KEY")),
    }


def public_search_google_cx() -> str:
    return os.getenv("GOOGLE_CSE_CX") or os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID") or ""


def choose_public_search_engine(engine: str) -> str:
    if engine == "auto":
        setup = public_search_setup_state()
        if setup["googleCse"]:
            return "google_cse"
        if setup["serpApi"]:
            return "serpapi"
        return "google_cse"
    return engine


def public_search_is_configured(engine: str) -> bool:
    setup = public_search_setup_state()
    if engine == "google_cse":
        return setup["googleCse"]
    if engine == "serpapi":
        return setup["serpApi"]
    return False


def fetch_public_search_results(query: str, engine: str, limit: int) -> list[dict[str, str]]:
    if engine == "serpapi":
        return fetch_serpapi_results(query, limit)
    return fetch_google_cse_results(query, limit)


def fetch_google_cse_results(query: str, limit: int) -> list[dict[str, str]]:
    api_key = os.getenv("GOOGLE_CSE_API_KEY", "")
    cx = public_search_google_cx()
    if not api_key or not cx:
        return []
    collected: list[dict[str, str]] = []
    start = 1
    while len(collected) < limit and start <= 91:
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "num": min(10, limit - len(collected)),
            "start": start,
        }
        payload = read_json_url("https://www.googleapis.com/customsearch/v1", params)
        for item in payload.get("items", []) if isinstance(payload, dict) else []:
            if not isinstance(item, dict):
                continue
            collected.append(
                {
                    "title": text(item.get("title")),
                    "link": text(item.get("link")),
                    "snippet": text(item.get("snippet")),
                }
            )
            if len(collected) >= limit:
                break
        if not payload.get("items"):
            break
        start += 10
    return collected


def fetch_serpapi_results(query: str, limit: int) -> list[dict[str, str]]:
    api_key = os.getenv("SERPAPI_API_KEY", "")
    if not api_key:
        return []
    payload = read_json_url(
        "https://serpapi.com/search.json",
        {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": min(100, limit),
            "gl": "jp",
            "hl": "ja",
        },
    )
    collected: list[dict[str, str]] = []
    for item in payload.get("organic_results", []) if isinstance(payload, dict) else []:
        if not isinstance(item, dict):
            continue
        collected.append(
            {
                "title": text(item.get("title")),
                "link": text(item.get("link")),
                "snippet": text(item.get("snippet")),
            }
        )
        if len(collected) >= limit:
            break
    return collected


def read_json_url(url: str, params: dict[str, Any]) -> dict[str, Any]:
    target = f"{url}?{urlencode(params)}"
    request = urllib.request.Request(
        target,
        headers={"User-Agent": "InstagramCreatorOutreach/0.1"},
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        payload = response.read()
    parsed = json.loads(payload.decode("utf-8"))
    return parsed if isinstance(parsed, dict) else {}


def format_public_search_source(results: list[dict[str, str]]) -> str:
    chunks = []
    for item in results:
        chunks.extend(
            [
                item.get("title", ""),
                item.get("link", ""),
                item.get("snippet", ""),
            ]
        )
    return "\n".join(part for part in chunks if part)


def instagram_graph_setup_state() -> dict[str, Any]:
    config = resolve_instagram_graph_config()
    mode = config.get("mode") or INSTAGRAM_BUSINESS_DISCOVERY_MODE
    business_discovery = mode == INSTAGRAM_BUSINESS_DISCOVERY_MODE and bool(config.get("ownUserId"))
    configured = bool(config.get("accessToken") and (mode == INSTAGRAM_LOGIN_MODE or config.get("ownUserId")))
    return {
        "configured": configured,
        "accessToken": bool(config.get("accessToken")),
        "ownUserId": bool(config.get("ownUserId")),
        "mode": mode,
        "businessDiscovery": business_discovery,
        "canEnrichCandidates": configured and business_discovery,
        "version": config.get("version"),
        "baseUrl": config.get("baseUrl"),
    }


def resolve_instagram_graph_config() -> dict[str, str]:
    access_token = os.getenv("META_ACCESS_TOKEN") or os.getenv("INSTAGRAM_ACCESS_TOKEN") or ""
    raw_mode = text(os.getenv("META_GRAPH_MODE") or os.getenv("INSTAGRAM_GRAPH_MODE")).lower()
    if raw_mode in {"instagram", "instagram_login", "ig_login", "graph_instagram"}:
        mode = INSTAGRAM_LOGIN_MODE
    elif raw_mode in {"business", "business_discovery", "facebook", "page"}:
        mode = INSTAGRAM_BUSINESS_DISCOVERY_MODE
    else:
        mode = INSTAGRAM_LOGIN_MODE if looks_like_instagram_login_token(access_token) else INSTAGRAM_BUSINESS_DISCOVERY_MODE
    configured_base_url = os.getenv("META_GRAPH_API_BASE_URL") or os.getenv("INSTAGRAM_GRAPH_API_BASE_URL") or ""
    base_url = configured_base_url or (
        INSTAGRAM_LOGIN_GRAPH_BASE_URL if mode == INSTAGRAM_LOGIN_MODE else INSTAGRAM_GRAPH_DEFAULT_BASE_URL
    )
    return {
        "baseUrl": base_url.rstrip("/"),
        "version": (
            os.getenv("META_GRAPH_API_VERSION")
            or os.getenv("INSTAGRAM_GRAPH_API_VERSION")
            or INSTAGRAM_GRAPH_DEFAULT_VERSION
        ).strip("/"),
        "accessToken": access_token,
        "ownUserId": os.getenv("META_IG_USER_ID") or os.getenv("INSTAGRAM_OWN_USER_ID") or "",
        "mode": mode,
    }


def looks_like_instagram_login_token(access_token: str) -> bool:
    return text(access_token).startswith("IGAA")


def enrich_candidate_from_instagram_api(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "invalid payload"}
    candidates = load_candidates(use_samples=False)
    candidate_id = text(payload.get("id"))
    requested_handle = normalize_handle(
        first_value(payload, ["handle", "instagramUrl", "profileUrl", "url", "username"])
    )
    selected: dict[str, Any] | None = None
    for row in candidates:
        if candidate_id and row.get("id") == candidate_id:
            selected = row
            break
        if requested_handle and row.get("handle", "").lower() == requested_handle.lower():
            selected = row
            break

    target_handle = normalize_handle(selected.get("handle") if selected else requested_handle)
    if not target_handle:
        return {"ok": False, "configured": instagram_graph_setup_state()["configured"], "error": "missing Instagram handle"}

    profile_result = fetch_instagram_graph_profile(target_handle)
    if not profile_result.get("ok"):
        return profile_result

    patch = build_instagram_graph_candidate(profile_result.get("profile") or {}, fallback_handle=target_handle)
    if selected:
        updated = merge_instagram_graph_candidate(selected, patch)
        updated_rows = [updated if row.get("id") == selected.get("id") else row for row in candidates]
        created = False
    else:
        patch["createdAt"] = now_iso()
        patch["updatedAt"] = patch["createdAt"]
        updated = normalize_candidate(patch)
        updated_rows = [*candidates, updated]
        created = True
    save_candidates(updated_rows)
    return {
        "ok": True,
        "configured": True,
        "created": created,
        "candidate": enrich_candidates([updated])[0],
        "profile": {
            key: value
            for key, value in (profile_result.get("profile") or {}).items()
            if key in {"username", "name", "biography", "followers_count", "media_count", "profile_picture_url", "website"}
        },
        "setup": instagram_graph_setup_state(),
        "source": profile_result.get("source", "instagram_graph_api"),
    }


def fetch_instagram_graph_profile(handle: str) -> dict[str, Any]:
    config = resolve_instagram_graph_config()
    setup = instagram_graph_setup_state()
    if not config.get("accessToken"):
        return {
            "ok": False,
            "configured": False,
            "setup": setup,
            "error": "Instagram API 未配置：需要 META_ACCESS_TOKEN",
        }
    clean_handle = normalize_extracted_handle(handle)
    if not clean_handle:
        return {"ok": False, "configured": True, "setup": setup, "error": "invalid Instagram handle"}
    if config.get("mode") == INSTAGRAM_LOGIN_MODE:
        return fetch_instagram_login_profile(clean_handle, config, setup)
    if not config.get("ownUserId"):
        return {
            "ok": False,
            "configured": False,
            "setup": setup,
            "error": "Business Discovery 模式未配置完整：需要 META_ACCESS_TOKEN 和 META_IG_USER_ID",
        }
    fields = f"business_discovery.username({clean_handle}){{{INSTAGRAM_GRAPH_PROFILE_FIELDS}}}"
    try:
        payload = read_meta_graph_url(config, config["ownUserId"], {"fields": fields})
    except (OSError, urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {
            "ok": False,
            "configured": True,
            "setup": setup,
            "error": sanitize_secret_text(str(exc), config.get("accessToken", "")),
        }
    profile = payload.get("business_discovery") if isinstance(payload, dict) else {}
    if not isinstance(profile, dict) or not profile:
        return {
            "ok": False,
            "configured": True,
            "setup": setup,
            "error": "Instagram API 未返回 business_discovery；请确认目标是可查询账号，且 token 来自已绑定的专业 IG/Page 权限流。",
        }
    return {"ok": True, "configured": True, "profile": profile, "source": "instagram_graph_api", "setup": setup}


def fetch_instagram_login_profile(handle: str, config: dict[str, str], setup: dict[str, Any]) -> dict[str, Any]:
    try:
        profile = read_meta_graph_url(config, "me", {"fields": INSTAGRAM_GRAPH_PROFILE_FIELDS})
    except (OSError, urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {
            "ok": False,
            "configured": True,
            "setup": setup,
            "error": sanitize_secret_text(str(exc), config.get("accessToken", "")),
        }
    own_handle = normalize_extracted_handle(text(profile.get("username")))
    if not own_handle:
        return {
            "ok": False,
            "configured": True,
            "setup": setup,
            "error": "Instagram Login API 未返回 username；请重新生成 token 并确认 instagram_business_basic 权限。",
        }
    if handle.lower() != own_handle.lower():
        return {
            "ok": False,
            "configured": True,
            "setup": setup,
            "error": (
                f"当前配置的是 Instagram Login token，只能补全授权账号 @{own_handle}，"
                f"不能查询其他达人 @{handle}。要补全达人候选池，请改用 Facebook/Page 连接的 Instagram 专业账号 token，并配置 META_IG_USER_ID。"
            ),
        }
    return {"ok": True, "configured": True, "profile": profile, "source": "instagram_login_api", "setup": setup}


def read_meta_graph_url(config: dict[str, str], path: str, params: dict[str, Any]) -> dict[str, Any]:
    base_url = text(config.get("baseUrl")) or INSTAGRAM_GRAPH_DEFAULT_BASE_URL
    version = text(config.get("version")) or INSTAGRAM_GRAPH_DEFAULT_VERSION
    access_token = text(config.get("accessToken"))
    if not re.match(r"^https://graph\.(?:facebook|instagram)\.com$", base_url, re.IGNORECASE):
        raise ValueError("invalid Instagram Graph API base URL")
    clean_path = quote(str(path).strip("/"), safe="")
    target = f"{base_url}/{version}/{clean_path}?{urlencode({**params, 'access_token': access_token})}"
    request = urllib.request.Request(
        target,
        headers={"Accept": "application/json", "User-Agent": "InstagramCreatorOutreach/0.1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw_payload = response.read(1_000_000)
    except urllib.error.HTTPError as exc:
        raise ValueError(format_meta_graph_http_error(exc, access_token)) from exc
    parsed = json.loads(raw_payload.decode("utf-8"))
    return parsed if isinstance(parsed, dict) else {}


def format_meta_graph_http_error(exc: urllib.error.HTTPError, access_token: str = "") -> str:
    try:
        raw = exc.read(8192).decode("utf-8", errors="replace")
    except OSError:
        raw = ""
    message = raw
    try:
        payload = json.loads(raw)
        error = payload.get("error") if isinstance(payload, dict) else {}
        if isinstance(error, dict):
            parts = [
                text(error.get("message")),
                f"type={text(error.get('type'))}" if error.get("type") else "",
                f"code={text(error.get('code'))}" if error.get("code") else "",
            ]
            message = " ".join(part for part in parts if part)
    except json.JSONDecodeError:
        pass
    detail = f": {sanitize_secret_text(message, access_token)}" if message else ""
    return f"HTTP {exc.code} {exc.reason}{detail}"


def sanitize_secret_text(message: str, *secrets: str) -> str:
    clean = text(message)
    for secret in secrets:
        if secret:
            clean = clean.replace(secret, "***")
    clean = re.sub(r"\b(?:IGAA|EAAG|EAAI)[A-Za-z0-9_-]{16,}\b", "***", clean)
    clean = re.sub(r"access_token=[^&\s]+", "access_token=***", clean)
    return clean[:900]


def build_instagram_graph_candidate(profile: dict[str, Any], fallback_handle: str = "") -> dict[str, Any]:
    handle = normalize_handle(profile.get("username") or fallback_handle)
    biography = text(profile.get("biography"))
    website = text(profile.get("website"))
    source_text = "\n".join(part for part in [biography, website] if part)
    email = EMAIL_RE.search(source_text or "")
    hashtag_tags = [match.group(1) for match in re.finditer(r"#([\w\u3040-\u30ff\u3400-\u9fff]{2,24})", source_text)]
    inferred_tags = infer_creator_tags(source_text)
    tags = merge_unique_lists(hashtag_tags, inferred_tags)
    note_parts = ["Instagram Graph API 补全"]
    if biography:
        note_parts.append(f"简介：{biography[:280]}")
    if website:
        note_parts.append(f"网站：{website}")
    media_count = parse_count(profile.get("media_count"))
    if media_count:
        note_parts.append(f"媒体数：{media_count}")
    return {
        "handle": handle,
        "name": text(profile.get("name")) or handle,
        "followers": parse_count(profile.get("followers_count")),
        "instagramUrl": instagram_profile_url(handle),
        "avatarUrl": normalize_avatar_url(profile.get("profile_picture_url")),
        "email": email.group(0) if email else "",
        "contactMethod": "email" if email else "",
        "location": infer_creator_location(source_text),
        "niche": infer_creator_niche(tags, ""),
        "tags": tags[:8],
        "notes": "\n".join(note_parts),
        "source": "instagram_graph_api",
    }


def merge_instagram_graph_candidate(existing: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    for key in ["handle", "followers", "instagramUrl", "avatarUrl"]:
        if patch.get(key):
            merged[key] = patch[key]
    patch_name = text(patch.get("name"))
    current_name = text(merged.get("name"))
    current_handle = text(merged.get("handle"))
    if patch_name and (not current_name or current_name.lower() == current_handle.lower()):
        merged["name"] = patch_name
    if patch.get("email") and not merged.get("email"):
        merged["email"] = patch["email"]
        merged["contactMethod"] = "email"
    if patch.get("location") and not merged.get("location"):
        merged["location"] = patch["location"]
    if patch.get("niche") and text(merged.get("niche")) in {"", "待人工判断"}:
        merged["niche"] = patch["niche"]
    merged["tags"] = merge_unique_lists(merged.get("tags"), patch.get("tags"))[:8]
    merged["notes"] = merge_note_text(merged.get("notes"), patch.get("notes"))
    merged["source"] = merge_note_text(merged.get("source"), patch.get("source")).replace("\n", "+")
    merged["updatedAt"] = now_iso()
    return normalize_candidate(merged)


def preview_website_candidates(source_text: str, keyword: str = "") -> dict[str, Any]:
    urls = extract_candidate_urls(source_text)
    existing = load_candidates(use_samples=False)
    existing_by_handle = {row["handle"].lower(): row for row in existing if row.get("handle")}
    rows = []
    counts = {"add": 0, "update": 0, "duplicate_source": 0, "skip": 0}
    seen: set[str] = set()
    fetch_errors: list[str] = []

    for index, url in enumerate(urls, start=1):
        page = inspect_public_creator_page(url)
        if page.get("error"):
            fetch_errors.append(f"{url}: {page['error']}")
        for candidate in build_website_candidates(page, keyword=keyword):
            handle_key = candidate.get("handle", "").lower()
            action = "add"
            issues = candidate_quality_issues(candidate)
            if handle_key and handle_key in seen:
                action = "duplicate_source"
                issues.append("本次网站列表内重复账号")
            elif handle_key and handle_key in existing_by_handle:
                action = "update"
            elif not handle_key:
                action = "skip"
                issues.append("没有识别到 Instagram 账号")
            if handle_key:
                seen.add(handle_key)
            counts[action] += 1
            score, breakdown = score_candidate(candidate)
            rows.append(
                {
                    "row": index,
                    "action": action,
                    "issues": issues,
                    "candidate": {
                        **candidate,
                        "score": score,
                        "tier": tier_for_score(score),
                        "scoreBreakdownItems": build_score_breakdown_items(breakdown),
                        "matchedText": page.get("summary", ""),
                    },
                }
            )

    return {
        "ok": True,
        "summary": {
            **counts,
            "rows": len(rows),
            "valid": counts["add"] + counts["update"] + counts["duplicate_source"],
            "urls": len(urls),
        },
        "rows": rows,
        "errors": fetch_errors[:8],
        "guardrails": [
            "只读取公开网页的 HTML 文本，不登录网站",
            "Instagram 链接只解析账号，不批量抓取 Instagram 页面",
            "导入前请在预览中人工确认粉丝数、ER、邮箱和合作适配度",
        ],
    }


def import_website_candidates(source_text: str, keyword: str = "") -> dict[str, Any]:
    preview = preview_website_candidates(source_text, keyword=keyword)
    existing = load_candidates(use_samples=False)
    by_id = {row["id"]: row for row in existing}
    by_handle = {row["handle"].lower(): row["id"] for row in existing if row.get("handle")}
    added = 0
    updated = 0
    skipped = 0
    seen: set[str] = set()

    for item in preview.get("rows", []):
        candidate = normalize_candidate(item.get("candidate") or {})
        handle_key = candidate.get("handle", "").lower()
        if not handle_key or handle_key in seen:
            skipped += 1
            continue
        seen.add(handle_key)
        existing_id = by_handle.get(handle_key)
        if existing_id and existing_id in by_id:
            by_id[existing_id] = merge_website_candidate(by_id[existing_id], candidate)
            updated += 1
        else:
            candidate["createdAt"] = now_iso()
            candidate["updatedAt"] = candidate["createdAt"]
            by_id[candidate["id"]] = candidate
            by_handle[handle_key] = candidate["id"]
            added += 1

    save_candidates(list(by_id.values()))
    return {
        "ok": True,
        "added": added,
        "updated": updated,
        "skipped": skipped,
        "total": len(by_id),
        "errors": preview.get("errors", []),
    }


def extract_candidate_urls(source_text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for raw in re.split(r"[\s,，]+", source_text or ""):
        clean = raw.strip().strip("<>()[]{}'\"")
        if not clean:
            continue
        match = URL_RE.search(clean)
        if match:
            clean = match.group(0)
        elif re.fullmatch(r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[^\s]*)?", clean):
            clean = f"https://{clean}"
        else:
            continue
        clean = clean.rstrip(".,，。")
        key = clean.lower()
        if key not in seen:
            seen.add(key)
            urls.append(clean)
        if len(urls) >= MAX_WEBSITE_URLS:
            break
    return urls


def inspect_public_creator_page(url: str) -> dict[str, Any]:
    normalized_url = normalize_public_url(url)
    host = urlparse(normalized_url).netloc.lower()
    if "instagram.com" in host:
        return inspect_instagram_url_only(normalized_url)
    try:
        ensure_public_fetch_url(normalized_url)
        html_text = read_public_html(normalized_url)
        page = extract_webpage_text(html_text, normalized_url)
        page["url"] = normalized_url
        page["isInstagram"] = False
        pages = [page]
        for linked_url in select_related_creator_links(page.get("links", []), normalized_url):
            if len(pages) >= MAX_WEBSITE_PAGES_PER_URL:
                break
            try:
                ensure_public_fetch_url(linked_url)
                linked_html = read_public_html(linked_url)
                linked_page = extract_webpage_text(linked_html, linked_url)
                linked_page["url"] = linked_url
                linked_page["isInstagram"] = False
                pages.append(linked_page)
            except (OSError, ValueError, urllib.error.URLError, TimeoutError) as exc:
                page.setdefault("fetchWarnings", []).append(f"{linked_url}: {exc}")
        return combine_public_creator_pages(pages, normalized_url)
    except (OSError, ValueError, urllib.error.URLError, TimeoutError) as exc:
        return {
            "url": normalized_url,
            "isInstagram": False,
            "title": "",
            "description": "",
            "text": "",
            "summary": "",
            "error": str(exc),
        }


def select_related_creator_links(links: Any, base_url: str) -> list[str]:
    base = urlparse(base_url)
    keywords = (
        "about",
        "contact",
        "inquiry",
        "profile",
        "media",
        "kit",
        "press",
        "pr",
        "collab",
        "collaboration",
        "work",
        "creator",
        "influencer",
    )
    selected: list[str] = []
    seen = {base_url.lower()}
    for raw in normalize_list(links):
        clean = text(raw)
        if not clean or EMAIL_RE.fullmatch(clean):
            continue
        parsed = urlparse(urljoin(base_url, clean))
        if parsed.scheme not in {"http", "https"}:
            continue
        if parsed.netloc.lower() != base.netloc.lower():
            continue
        path_key = f"{parsed.path}?{parsed.query}".lower()
        if not any(keyword in path_key for keyword in keywords):
            continue
        linked_url = parsed._replace(fragment="").geturl()
        key = linked_url.lower()
        if key in seen:
            continue
        seen.add(key)
        selected.append(linked_url)
        if len(selected) >= MAX_WEBSITE_PAGES_PER_URL - 1:
            break
    return selected


def combine_public_creator_pages(pages: list[dict[str, Any]], source_url: str) -> dict[str, Any]:
    if not pages:
        return {
            "url": source_url,
            "isInstagram": False,
            "title": "",
            "description": "",
            "links": [],
            "text": "",
            "summary": "",
            "error": "",
        }
    combined = dict(pages[0])
    links = merge_unique_lists(*(page.get("links", []) for page in pages))
    warnings: list[str] = []
    sections: list[str] = []
    summaries: list[str] = []
    descriptions: list[str] = []
    avatar_urls: list[str] = []
    for page in pages:
        if page.get("fetchWarnings"):
            warnings.extend(normalize_list(page.get("fetchWarnings")))
        if page.get("description"):
            descriptions.append(text(page.get("description")))
        if page.get("avatarUrl"):
            avatar_urls.append(text(page.get("avatarUrl")))
        if page.get("summary"):
            summaries.append(text(page.get("summary")))
        section = "\n".join(
            part
            for part in [
                f"Page URL: {page.get('url', '')}",
                text(page.get("title")),
                text(page.get("description")),
                "\n".join(normalize_list(page.get("links"))),
                text(page.get("text")),
            ]
            if part
        )
        if section:
            sections.append(section)
    combined["url"] = source_url
    combined["isInstagram"] = False
    combined["pages"] = [page.get("url", "") for page in pages if page.get("url")]
    combined["links"] = links
    combined["description"] = " / ".join(merge_unique_lists(descriptions))[:420]
    combined["avatarUrl"] = next(
        (normalized for url in merge_unique_lists(avatar_urls) for normalized in [normalize_avatar_url(url)] if normalized),
        "",
    )
    combined["text"] = "\n\n".join(sections)
    combined["summary"] = " / ".join(merge_unique_lists(summaries))[:520]
    if warnings:
        combined["fetchWarnings"] = warnings[:6]
    return combined


def normalize_public_url(url: str) -> str:
    clean = text(url).strip("<>()[]{}'\"")
    if not re.match(r"^https?://", clean, re.IGNORECASE):
        clean = f"https://{clean}"
    parsed = urlparse(clean)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("invalid URL")
    return clean


def ensure_public_fetch_url(url: str) -> None:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host.lower() in BLOCKED_HOSTS or host.lower().endswith(".local"):
        raise ValueError("blocked non-public host")
    try:
        ipaddress.ip_address(host)
        hosts = [host]
    except ValueError:
        hosts = [item[4][0] for item in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)]
    for item in hosts:
        ip = ipaddress.ip_address(item)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            raise ValueError("blocked private network address")


def read_public_html(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "InstagramCreatorOutreach/0.1 (+manual creator research)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        content_type = response.headers.get("Content-Type", "")
        if content_type and "text/html" not in content_type and "text/plain" not in content_type:
            raise ValueError(f"unsupported content type: {content_type.split(';')[0]}")
        payload = response.read(MAX_WEBSITE_BYTES + 1)
    if len(payload) > MAX_WEBSITE_BYTES:
        payload = payload[:MAX_WEBSITE_BYTES]
    charset_match = re.search(r"charset=([\w-]+)", content_type, re.IGNORECASE)
    charset = charset_match.group(1) if charset_match else "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def extract_webpage_text(html_text: str, url: str) -> dict[str, Any]:
    title = extract_html_title(html_text)
    description = extract_meta_description(html_text)
    avatar_url = extract_meta_image(html_text, url)
    links = extract_html_link_values(html_text, url)
    signals = extract_relevant_html_signals(html_text)
    body = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", html_text)
    body = re.sub(r"(?is)<br\s*/?>", "\n", body)
    body = re.sub(r"(?is)</(p|div|li|h[1-6]|section|article)>", "\n", body)
    body = re.sub(r"(?is)<[^>]+>", " ", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n", body).strip()
    link_text = "\n".join(merge_unique_lists(links, signals))
    summary = " / ".join(part for part in [title, description, body[:260], link_text[:180]] if part)
    return {
        "url": url,
        "title": title,
        "description": description,
        "avatarUrl": avatar_url,
        "links": links,
        "text": "\n".join(part for part in [title, description, link_text, body] if part),
        "summary": summary[:520],
    }


def extract_relevant_html_signals(html_text: str) -> list[str]:
    decoded = html.unescape(html_text or "")
    values: list[str] = []
    for email in EMAIL_RE.findall(decoded):
        values.append(email)
    for match in INSTAGRAM_URL_RE.finditer(decoded):
        values.append(match.group(0))
    for match in re.finditer(r"""(?is)<meta[^>]+content=["']([^"']+)["']""", html_text or ""):
        content = clean_page_text(match.group(1))
        if is_relevant_creator_signal(content):
            values.append(content[:500])
    for match in re.finditer(
        r"""(?is)<script[^>]+type=["']application/ld\+json["'][^>]*>(.*?)</script>""",
        html_text or "",
    ):
        content = clean_page_text(re.sub(r"(?is)<[^>]+>", " ", match.group(1)))
        if is_relevant_creator_signal(content):
            values.append(content[:1200])
    return merge_unique_lists(values)[:80]


def is_relevant_creator_signal(value: str) -> bool:
    clean = text(value)
    if not clean:
        return False
    return bool(
        EMAIL_RE.search(clean)
        or INSTAGRAM_URL_RE.search(clean)
        or re.search(
            r"followers?|follower|engagement|creator|influencer|media\s*kit|profile|contact|collab|PR|fashion|beauty|lifestyle",
            clean,
            re.IGNORECASE,
        )
    )


def extract_html_link_values(html_text: str, base_url: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for match in re.finditer(r"""(?is)\b(?:href|data-href|data-url)=["']([^"']+)["']""", html_text or ""):
        raw = html.unescape(match.group(1)).strip()
        if not raw:
            continue
        lowered = raw.lower()
        if lowered.startswith(("javascript:", "#", "tel:")):
            continue
        if lowered.startswith("mailto:"):
            clean = raw[7:].split("?", 1)[0]
        elif re.match(r"^https?://", raw, re.IGNORECASE) or raw.startswith("/"):
            clean = urljoin(base_url, raw)
        else:
            clean = raw
        key = clean.lower()
        if key not in seen:
            seen.add(key)
            values.append(clean)
        if len(values) >= 80:
            break
    return values


def extract_html_title(html_text: str) -> str:
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", html_text)
    return clean_page_text(match.group(1))[:140] if match else ""


def extract_meta_description(html_text: str) -> str:
    patterns = [
        r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        r'(?is)<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
        r'(?is)<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']',
        r'(?is)<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']og:description["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text)
        if match:
            return clean_page_text(match.group(1))[:260]
    return ""


def extract_meta_image(html_text: str, base_url: str) -> str:
    patterns = [
        r'(?is)<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\'](.*?)["\']',
        r'(?is)<meta[^>]+name=["\']twitter:image(?::src)?["\'][^>]+content=["\'](.*?)["\']',
        r'(?is)<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']og:image(?::secure_url)?["\']',
        r'(?is)<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']twitter:image(?::src)?["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text or "")
        if not match:
            continue
        raw = html.unescape(match.group(1)).strip()
        candidate = normalize_avatar_url(urljoin(base_url, raw))
        if candidate:
            return candidate
    return ""


def clean_page_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def inspect_instagram_url_only(url: str) -> dict[str, Any]:
    handle = normalize_handle(url)
    return {
        "url": instagram_profile_url(handle),
        "isInstagram": True,
        "title": handle,
        "description": "",
        "text": url,
        "summary": f"Instagram URL: @{handle}" if handle else url,
        "error": "",
    }


def build_website_candidates(page: dict[str, Any], keyword: str = "") -> list[dict[str, Any]]:
    source_text = page_text_blob(page)
    profiles = extract_instagram_profiles(source_text)
    if page.get("isInstagram"):
        handle = normalize_handle(page.get("url"))
        profiles = [{"handle": handle, "url": instagram_profile_url(handle), "matchedText": page.get("summary", "")}] if handle else []
    if not profiles:
        return []
    emails = EMAIL_RE.findall(source_text)
    followers = infer_followers_from_text(source_text)
    engagement_rate = infer_engagement_from_text(source_text)
    tags = infer_creator_tags(source_text, keyword)
    niche = infer_creator_niche(tags, keyword)
    collab_signal = infer_collab_signal(source_text)
    candidates = []
    seen: set[str] = set()
    for profile in profiles:
        handle = profile["handle"]
        if not handle or handle.lower() in seen:
            continue
        seen.add(handle.lower())
        note_parts = [
            "达人网站识别器自动建档，请人工复核关键数据。",
            f"来源网站：{page.get('url', '')}",
        ]
        if page.get("title"):
            note_parts.append(f"页面标题：{page['title'][:120]}")
        if page.get("description"):
            note_parts.append(f"页面简介：{page['description'][:180]}")
        if page.get("isInstagram"):
            note_parts.append("Instagram 页面未自动抓取，仅从链接解析账号。")
        if page.get("error"):
            note_parts.append(f"抓取提示：{page['error']}")
        if profile.get("matchedText"):
            note_parts.append(f"上下文：{profile['matchedText'][:180]}")
        candidate = normalize_candidate(
            {
                "handle": handle,
                "name": infer_creator_name(page, handle),
                "niche": niche,
                "location": infer_creator_location(source_text),
                "followers": followers,
                "engagementRate": engagement_rate,
                "contentFit": 66 if tags else 58,
                "audienceFit": 66,
                "brandSafety": 72,
                "collabSignal": collab_signal,
                "contactMethod": "email" if emails else "dm",
                "email": emails[0] if emails else "",
                "instagramUrl": profile.get("url") or instagram_profile_url(handle),
                "avatarUrl": page.get("avatarUrl", ""),
                "status": "review",
                "tags": tags,
                "notes": "\n".join(note_parts),
                "source": "website_inspector",
            }
        )
        candidates.append(candidate)
    return candidates


def page_text_blob(page: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["url", "title", "description", "links", "text", "summary"]:
        value = page.get(key)
        if isinstance(value, list):
            parts.extend(text(item) for item in value if text(item))
        elif text(value):
            parts.append(text(value))
    return "\n".join(parts)


def infer_creator_name(page: dict[str, Any], handle: str) -> str:
    title = text(page.get("title"))
    if not title:
        return handle
    clean = re.split(r"[｜|\-–—]", title)[0].strip()
    clean = re.sub(r"(?i)instagram|official|公式|プロフィール", "", clean).strip()
    return clean[:60] or handle


def infer_followers_from_text(source_text: str) -> int:
    patterns = [
        r"(?:followers|フォロワー|粉丝|粉絲|follower)\D{0,18}([\d,.]+)\s*(万|萬|w|k|m|万人)?",
        r"([\d,.]+)\s*(万|萬|w|k|m|万人)?\s*(?:followers|フォロワー|粉丝|粉絲|follower)",
    ]
    for pattern in patterns:
        match = re.search(pattern, source_text, re.IGNORECASE)
        if match:
            return parse_count("".join(part for part in match.groups() if part))
    return 0


def infer_engagement_from_text(source_text: str) -> float:
    patterns = [
        r"(?:平均\s*)?(?:ER|engagement|エンゲージメント|互动率|平均ER)\D{0,12}([\d.]+)\s*%",
        r"([\d.]+)\s*%\s*(?:ER|engagement|エンゲージメント|互动率)",
    ]
    for pattern in patterns:
        match = re.search(pattern, source_text, re.IGNORECASE)
        if match:
            return parse_percent(match.group(1))
    return 0.0


def infer_collab_signal(source_text: str) -> int:
    score = 30
    rules = [
        (r"PR|タイアップ|案件|企業PR|アンバサダー|ambassador|collab|合作|商务", 24),
        (r"リール|Reels|ストーリーズ|stories|フィード|投稿対応", 14),
        (r"実績|再生|万回|事例|媒体資料|media kit", 12),
        (r"メール|mail|contact|お問い合わせ", 10),
    ]
    for pattern, value in rules:
        if re.search(pattern, source_text, re.IGNORECASE):
            score += value
    return min(score, 95)


def infer_creator_tags(source_text: str, keyword: str = "") -> list[str]:
    rules = [
        (r"美容|beauty|コスメ|スキンケア", "美容"),
        (r"健康|ヘルス|health|サプリ", "健康"),
        (r"ファッション|fashion|コーデ|服|wear", "ファッション"),
        (r"ライフスタイル|lifestyle|暮らし", "ライフスタイル"),
        (r"音楽|music|クリエーター|creator", "音楽"),
        (r"ママ|育児|mom|kids", "ママ"),
        (r"低身長|petite|150cm|小个子", "低身長"),
        (r"通勤|オフィス|office", "通勤"),
        (r"PR|タイアップ|案件|アンバサダー", "PR実績あり"),
        (r"Reels|リール|動画", "Reels対応"),
    ]
    tags = normalize_tags(keyword)
    for pattern, tag in rules:
        if re.search(pattern, source_text, re.IGNORECASE):
            tags.append(tag)
    return normalize_tags(tags)


def infer_creator_niche(tags: list[str], keyword: str = "") -> str:
    if keyword:
        return text(keyword)
    if "ファッション" in tags and "美容" in tags:
        return "美容・ファッション"
    if "ファッション" in tags:
        return "ファッション"
    if "美容" in tags or "健康" in tags:
        return "美容・健康"
    if "ライフスタイル" in tags:
        return "ライフスタイル"
    return "要人工判断"


def infer_creator_location(source_text: str) -> str:
    if re.search(r"Tokyo|東京", source_text, re.IGNORECASE):
        return "Tokyo"
    if re.search(r"Osaka|大阪", source_text, re.IGNORECASE):
        return "Osaka"
    if re.search(r"Japan|日本", source_text, re.IGNORECASE):
        return "Japan"
    return "Japan"


def merge_website_candidate(existing: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    keep_existing_fields = {"followers", "engagementRate", "avgLikes", "email"}
    for key, value in candidate.items():
        if key in keep_existing_fields and existing.get(key):
            continue
        if value not in (None, "", [], 0, 0.0):
            merged[key] = value
    merged["tags"] = merge_unique_lists(existing.get("tags"), candidate.get("tags"))[:8]
    merged["notes"] = merge_note_text(existing.get("notes"), candidate.get("notes"))
    merged["updatedAt"] = now_iso()
    return normalize_candidate(merged)


def merge_unique_lists(*values: Any) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for value in values:
        for item in normalize_list(value):
            key = item.lower()
            if key and key not in seen:
                seen.add(key)
                merged.append(item)
    return merged


def merge_note_text(*values: Any) -> str:
    parts = []
    for value in values:
        clean = text(value)
        if clean and clean not in parts:
            parts.append(clean)
    return "\n".join(parts)


def preview_discovery_candidates(
    source_text: str,
    keyword: str = "",
    source_label: str = "pasted_results",
) -> dict[str, Any]:
    existing = load_candidates(use_samples=False)
    existing_by_handle = {
        row["handle"].lower(): row
        for row in existing
        if row.get("handle")
    }
    extracted = extract_instagram_profiles(source_text)
    rows = []
    counts = {"add": 0, "update": 0, "duplicate_source": 0, "skip": 0}
    seen: set[str] = set()
    for index, item in enumerate(extracted, start=1):
        handle = item["handle"]
        handle_key = handle.lower()
        action = "add"
        issues: list[str] = []
        if handle_key in seen:
            action = "duplicate_source"
            issues.append("本次采集文本内重复")
        elif handle_key in existing_by_handle:
            action = "update"
        seen.add(handle_key)
        candidate = build_discovery_candidate(item, keyword=keyword, source_label=source_label)
        score, breakdown = score_candidate(candidate)
        rows.append(
            {
                "row": index,
                "action": action,
                "issues": issues,
                "candidate": {
                    **candidate,
                    "score": score,
                    "tier": tier_for_score(score),
                    "scoreBreakdownItems": build_score_breakdown_items(breakdown),
                    "matchedText": item.get("matchedText", ""),
                },
            }
        )
        counts[action] += 1

    return {
        "ok": True,
        "summary": {
            **counts,
            "rows": len(rows),
            "valid": counts["add"] + counts["update"] + counts["duplicate_source"],
        },
        "rows": rows,
        "guardrails": [
            "只解析你提供的搜索结果、URL 列表、HTML 或导出文本",
            "不会登录 Instagram，也不会抓取粉丝、评论、帖子或私信",
            "导入后的达人默认进入待审核，需要人工打开主页确认数据",
        ],
    }


def import_discovery_candidates(
    source_text: str,
    keyword: str = "",
    source_label: str = "pasted_results",
) -> dict[str, Any]:
    existing = load_candidates(use_samples=False)
    by_id = {row["id"]: row for row in existing}
    by_handle = {row["handle"].lower(): row["id"] for row in existing if row.get("handle")}
    extracted = extract_instagram_profiles(source_text)
    added = 0
    updated = 0
    skipped = 0
    seen: set[str] = set()

    for item in extracted:
        handle_key = item["handle"].lower()
        if handle_key in seen:
            skipped += 1
            continue
        seen.add(handle_key)
        candidate = build_discovery_candidate(item, keyword=keyword, source_label=source_label)
        existing_id = by_handle.get(handle_key)
        if existing_id and existing_id in by_id:
            by_id[existing_id] = merge_discovery_candidate(by_id[existing_id], candidate, item)
            updated += 1
        else:
            candidate["createdAt"] = now_iso()
            candidate["updatedAt"] = candidate["createdAt"]
            by_id[candidate["id"]] = candidate
            by_handle[handle_key] = candidate["id"]
            added += 1

    save_candidates(list(by_id.values()))
    return {"ok": True, "added": added, "updated": updated, "skipped": skipped, "total": len(by_id)}


def extract_instagram_profiles(source_text: str) -> list[dict[str, str]]:
    text_value = html_unescape(source_text or "")
    profiles: list[dict[str, str]] = []
    for match in INSTAGRAM_URL_RE.finditer(text_value):
        handle = normalize_extracted_handle(match.group(1))
        if not handle:
            continue
        profiles.append(
            {
                "handle": handle,
                "url": instagram_profile_url(handle),
                "matchedText": context_for_match(text_value, match.start(), match.end()),
            },
        )
    for match in INSTAGRAM_AT_RE.finditer(text_value):
        handle = normalize_extracted_handle(match.group(1))
        if not handle:
            continue
        profiles.append(
            {
                "handle": handle,
                "url": instagram_profile_url(handle),
                "matchedText": context_for_match(text_value, match.start(), match.end()),
            },
        )
    return profiles


def normalize_extracted_handle(value: str) -> str:
    handle = normalize_handle(value)
    if not handle:
        return ""
    lowered = handle.lower()
    if lowered in INSTAGRAM_RESERVED_PATHS:
        return ""
    if handle.startswith(".") or handle.endswith(".") or ".." in handle:
        return ""
    if not re.fullmatch(r"[A-Za-z0-9._]{2,30}", handle):
        return ""
    return handle


def context_for_match(source_text: str, start: int, end: int, radius: int = 80) -> str:
    snippet = source_text[max(0, start - radius): min(len(source_text), end + radius)]
    return re.sub(r"\s+", " ", snippet).strip()


def build_discovery_candidate(
    item: dict[str, str],
    keyword: str = "",
    source_label: str = "pasted_results",
) -> dict[str, Any]:
    keyword_text = text(keyword)
    tags = [keyword_text] if keyword_text else []
    note_parts = [
        "合规采集器自动建档，仅从用户提供文本中提取 profile handle。",
        f"来源：{text(source_label) or 'pasted_results'}",
    ]
    if item.get("matchedText"):
        note_parts.append(f"上下文：{item['matchedText'][:160]}")
    return normalize_candidate(
        {
            "handle": item["handle"],
            "name": item["handle"],
            "niche": keyword_text or "待人工判断",
            "location": "Japan",
            "instagramUrl": item.get("url") or instagram_profile_url(item["handle"]),
            "status": "review",
            "contentFit": 62,
            "audienceFit": 62,
            "brandSafety": 72,
            "collabSignal": 30,
            "contactMethod": "unknown",
            "tags": tags,
            "notes": "\n".join(note_parts),
            "source": f"collector:{text(source_label) or 'pasted_results'}",
        }
    )


def merge_discovery_candidate(
    existing: dict[str, Any],
    candidate: dict[str, Any],
    item: dict[str, str],
) -> dict[str, Any]:
    merged = dict(existing)
    merged["updatedAt"] = now_iso()
    if not merged.get("instagramUrl"):
        merged["instagramUrl"] = candidate.get("instagramUrl", "")
    existing_tags = set(normalize_tags(merged.get("tags")))
    for tag in normalize_tags(candidate.get("tags")):
        existing_tags.add(tag)
    merged["tags"] = sorted(existing_tags)
    source_note = f"采集器再次发现：{item.get('matchedText', '')[:160]}".strip()
    existing_notes = text(merged.get("notes"))
    if source_note and source_note not in existing_notes:
        merged["notes"] = "\n".join(part for part in [existing_notes, source_note] if part)
    return normalize_candidate(merged)


def html_unescape(value: str) -> str:
    replacements = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": '"',
        "&#39;": "'",
    }
    for raw, replacement in replacements.items():
        value = value.replace(raw, replacement)
    return value


def import_candidates_from_csv(csv_text: str) -> dict[str, Any]:
    existing = load_candidates(use_samples=False)
    by_id = {row["id"]: row for row in existing}
    by_handle = {row["handle"].lower(): row["id"] for row in existing if row.get("handle")}
    rows = parse_csv_rows(csv_text)
    added = 0
    updated = 0
    for row in rows:
        candidate = normalize_candidate(row)
        if not candidate["handle"] and not candidate["name"]:
            continue
        existing_id = by_handle.get(candidate["handle"].lower()) or candidate["id"]
        if existing_id in by_id:
            merged = {**by_id[existing_id], **strip_empty(candidate), "updatedAt": now_iso()}
            by_id[existing_id] = normalize_candidate(merged)
            updated += 1
        else:
            candidate["createdAt"] = now_iso()
            candidate["updatedAt"] = candidate["createdAt"]
            by_id[candidate["id"]] = candidate
            if candidate.get("handle"):
                by_handle[candidate["handle"].lower()] = candidate["id"]
            added += 1
    save_candidates(list(by_id.values()))
    return {"ok": True, "added": added, "updated": updated, "total": len(by_id)}


def preview_import_candidates(csv_text: str) -> dict[str, Any]:
    existing = load_candidates(use_samples=False)
    existing_by_handle = {
        row["handle"].lower(): row
        for row in existing
        if row.get("handle")
    }
    rows = parse_csv_rows(csv_text)
    seen_handles: set[str] = set()
    preview_rows = []
    counts = {"add": 0, "update": 0, "duplicate_csv": 0, "skip": 0}

    for index, row in enumerate(rows, start=1):
        candidate = normalize_candidate(row)
        issues = candidate_quality_issues(candidate)
        handle_key = candidate.get("handle", "").lower()
        if not candidate.get("handle") and not candidate.get("name"):
            action = "skip"
            issues.append("缺少 handle/name")
        elif handle_key and handle_key in seen_handles:
            action = "duplicate_csv"
            issues.append("CSV 内重复账号，将只保留后出现的更新")
        elif handle_key and handle_key in existing_by_handle:
            action = "update"
        else:
            action = "add"
        if handle_key:
            seen_handles.add(handle_key)
        counts[action] += 1
        score, breakdown = score_candidate(candidate)
        preview_rows.append(
            {
                "row": index,
                "action": action,
                "issues": issues,
                "candidate": {
                    **candidate,
                    "score": score,
                    "tier": tier_for_score(score),
                    "scoreBreakdownItems": build_score_breakdown_items(breakdown),
                },
            }
        )

    return {
        "ok": True,
        "summary": {
            **counts,
            "rows": len(preview_rows),
            "valid": counts["add"] + counts["update"] + counts["duplicate_csv"],
        },
        "rows": preview_rows,
    }


def parse_csv_rows(csv_text: str) -> list[dict[str, Any]]:
    sample = csv_text[:2048]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(csv_text), dialect=dialect)
    return [dict(row) for row in reader]


def upsert_candidate(payload: dict[str, Any]) -> dict[str, Any]:
    candidates = load_candidates(use_samples=False)
    candidate = normalize_candidate(payload)
    now = now_iso()
    found = False
    updated_rows = []
    for row in candidates:
        if row["id"] == candidate["id"] or (
            row.get("handle") and candidate.get("handle") and row["handle"].lower() == candidate["handle"].lower()
        ):
            patch = strip_empty(candidate)
            if not payload_has_explicit_pin(payload):
                patch.pop("pinned", None)
            merged = {**row, **patch, "updatedAt": now}
            updated_rows.append(normalize_candidate(merged))
            found = True
        else:
            updated_rows.append(row)
    if not found:
        candidate["createdAt"] = now
        candidate["updatedAt"] = now
        updated_rows.append(candidate)
    save_candidates(updated_rows)
    return {"ok": True, "candidate": enrich_candidates([candidate])[0], "created": not found}


def payload_has_explicit_pin(payload: dict[str, Any]) -> bool:
    keys = {"pinned", "pin", "starred", "置顶", "是否置顶"}
    lowered = {str(key).lower() for key in payload.keys()}
    return any(key.lower() in lowered for key in keys)


def update_candidate_status(candidate_id: str, status: str) -> dict[str, Any]:
    candidates = load_candidates(use_samples=True)
    normalized_status = normalize_status(status)
    changed = False
    for row in candidates:
        if row["id"] == candidate_id:
            row["status"] = normalized_status
            row["updatedAt"] = now_iso()
            if normalized_status == "contacted" and not row.get("lastContacted"):
                row["lastContacted"] = today_iso()
                row["followUpDate"] = row.get("followUpDate") or default_follow_up_date()
                row["contactHistory"] = append_history_event(
                    row.get("contactHistory"),
                    "contacted",
                    "标记为已建联",
                    row["lastContacted"],
                    row["followUpDate"],
                )
            changed = True
            break
    if changed:
        save_candidates(candidates)
    return {"ok": changed, "status": normalized_status}


def update_candidate_pin(candidate_id: str, pinned: Any) -> dict[str, Any]:
    candidates = load_candidates(use_samples=True)
    changed = False
    updated_candidate: dict[str, Any] | None = None
    next_pinned = boolish(pinned)
    for row in candidates:
        if row["id"] == candidate_id:
            row["pinned"] = next_pinned
            row["updatedAt"] = now_iso()
            updated_candidate = row
            changed = True
            break
    if changed:
        save_candidates(candidates)
    return {
        "ok": changed,
        "pinned": next_pinned,
        "candidate": enrich_candidates([updated_candidate])[0] if updated_candidate else None,
    }


def log_candidate_contact(
    candidate_id: str,
    note: str = "",
    contact_type: str = "contacted",
    follow_up_date: str = "",
) -> dict[str, Any]:
    candidates = load_candidates(use_samples=True)
    changed = False
    updated_candidate: dict[str, Any] | None = None
    today = today_iso()
    follow_up = normalize_date_text(follow_up_date) or default_follow_up_date()
    for row in candidates:
        if row["id"] == candidate_id:
            row["status"] = "contacted" if row.get("status") in {"new", "review", "ready"} else row["status"]
            row["lastContacted"] = today
            row["followUpDate"] = follow_up
            row["updatedAt"] = now_iso()
            row["contactHistory"] = append_history_event(
                row.get("contactHistory"),
                normalize_history_type(contact_type),
                note or "记录一次建联动作",
                today,
                follow_up,
            )
            updated_candidate = row
            changed = True
            break
    if changed:
        save_candidates(candidates)
    return {
        "ok": changed,
        "candidate": enrich_candidates([updated_candidate])[0] if updated_candidate else None,
    }


def update_candidate_followup(candidate_id: str, follow_up_date: str) -> dict[str, Any]:
    candidates = load_candidates(use_samples=True)
    follow_up = normalize_date_text(follow_up_date)
    changed = False
    for row in candidates:
        if row["id"] == candidate_id:
            row["followUpDate"] = follow_up
            row["updatedAt"] = now_iso()
            changed = True
            break
    if changed:
        save_candidates(candidates)
    return {"ok": changed, "followUpDate": follow_up}


def delete_candidate(candidate_id: str) -> dict[str, Any]:
    candidates = load_candidates(use_samples=False)
    next_rows = [row for row in candidates if row["id"] != candidate_id]
    if len(next_rows) == len(candidates):
        return {"ok": False, "error": "candidate not found"}
    save_candidates(next_rows)
    return {"ok": True, "deleted": candidate_id}


def backup_candidates(candidates: list[dict[str, Any]], reason: str) -> str:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    backup_path = DATA_DIR / f"candidates_backup_{reason}_{timestamp}.json"
    payload = {
        "createdAt": now_iso(),
        "reason": reason,
        "candidates": [strip_runtime_fields(normalize_candidate(item)) for item in candidates],
    }
    backup_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(backup_path)


def delete_all_candidates(confirm: str = "") -> dict[str, Any]:
    if confirm != "DELETE":
        return {"ok": False, "error": "confirmation required", "deleted": 0}
    candidates = load_candidates(use_samples=False)
    deleted = len(candidates)
    backup_path = backup_candidates(candidates, "delete_all") if candidates else ""
    save_candidates([])
    return {"ok": True, "deleted": deleted, "total": 0, "backup": backup_path}


def strip_empty(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if value not in (None, "", [])}


def export_candidates_csv(candidates: list[dict[str, Any]] | None = None) -> str:
    candidates = enrich_candidates(candidates or load_candidates())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in candidates:
        data = {field: row.get(field, "") for field in CSV_FIELDS}
        data["tags"] = "、".join(row.get("tags") or [])
        writer.writerow(data)
    return output.getvalue()


def text(value: Any) -> str:
    return str(value).strip() if value not in (None, "") else ""
