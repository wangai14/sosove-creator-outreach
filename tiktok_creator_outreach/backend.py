from __future__ import annotations

import csv
import io
import json
import os
import re
import urllib.error
import urllib.request
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlencode, urlparse

from instagram_creator_outreach.backend import (
    call_openai_compatible_copy_model,
    resolve_copy_model_config,
    test_copy_model_config as shared_test_copy_model_config,
)


PACKAGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PACKAGE_DIR.parent
STATIC_DIR = PACKAGE_DIR / "static"
DATA_DIR = Path(os.getenv("TIKTOK_OUTREACH_DATA_DIR", str(ROOT_DIR / "data" / "tiktok_creator_outreach")))
CANDIDATES_PATH = DATA_DIR / "candidates.json"

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

PARTNERSHIP_STAGES = {
    "none": "未开始",
    "pricing": "报价确认",
    "sample_pending": "待寄样",
    "sample_sent": "已寄样",
    "content_scheduled": "内容排期",
    "draft_review": "脚本/初稿审核",
    "posted": "已发布",
    "measured": "复盘完成",
}

VIDEO_PROGRESS = {
    "not_started": "未开始",
    "product_confirming": "选品确认",
    "script_review": "脚本审核",
    "sample_sent": "样品已寄",
    "filming": "拍摄中",
    "draft_review": "初稿待审",
    "revision": "修改中",
    "posted": "已发布",
    "measured": "已复盘",
}

CSV_FIELDS = [
    "handle", "pinned", "name", "creatorType", "niche", "location", "followers", "avgViews",
    "medianViews", "engagementRate", "avgLikes", "avgComments", "avgShares", "viewFollowerRatio",
    "videoFrequency", "contentFit", "audienceFit", "brandSafety", "collabSignal", "contactMethod",
    "email", "tiktokUrl", "avatarUrl", "status", "followUpDate", "lastContacted", "invitationSentAt",
    "connectionAt", "partnershipStage", "quoteJpy", "collabProduct", "sampleStatus", "sampleCostJpy",
    "recipientName", "postalCode", "shippingAddress", "phoneNumber", "orderNumber", "shippingTracking",
    "shippedAt", "receivedAt", "videoFormat", "videoProgress", "scriptDueDate", "draftDueDate", "postDate",
    "postUrl", "savedWorks", "featuredWorkId", "sparkAdsStatus", "sparkAuthorizationCode", "usageRightsDays", "couponCode", "orders",
    "revenueJpy", "tags", "notes",
]

TIKTOK_URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?(?:tiktok\.com|tiktok\.jp)/@([A-Za-z0-9._-]{2,30})(?:[/\?#]|$)",
    re.IGNORECASE,
)
TIKTOK_AT_RE = re.compile(r"(?<![\w.])@([A-Za-z0-9._-]{2,30})(?![\w.-])")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def today_iso() -> str:
    return date.today().isoformat()


def text(value: Any) -> str:
    return str(value).strip() if value not in (None, "") else ""


def first_value(raw: dict[str, Any], keys: list[str]) -> Any:
    lowered = {str(key).lower(): value for key, value in raw.items()}
    for key in keys:
        if key in raw and raw[key] not in (None, ""):
            return raw[key]
        value = lowered.get(key.lower())
        if value not in (None, ""):
            return value
    return ""


def parse_count(value: Any) -> int:
    if value in (None, ""):
        return 0
    if isinstance(value, (int, float)):
        return max(0, int(float(value)))
    raw = str(value).strip().lower().replace(",", "")
    multiplier = 1
    for suffix, scale in (("万", 10_000), ("w", 10_000), ("k", 1_000), ("m", 1_000_000)):
        if raw.endswith(suffix):
            multiplier = scale
            raw = raw[: -len(suffix)]
            break
    match = re.search(r"\d+(?:\.\d+)?", raw)
    return int(float(match.group(0)) * multiplier) if match else 0


def parse_float(value: Any, fallback: float = 0.0) -> float:
    if value in (None, ""):
        return fallback
    try:
        return float(value)
    except (TypeError, ValueError):
        match = re.search(r"-?\d+(?:\.\d+)?", str(value).replace(",", ""))
        return float(match.group(0)) if match else fallback


def parse_percent(value: Any) -> float:
    raw = text(value)
    number = parse_float(value)
    if "%" in raw:
        return round(number, 2)
    return round(number * 100, 2) if 0 < number <= 1 else round(number, 2)


def parse_score(value: Any, fallback: int = 70) -> int:
    if value in (None, ""):
        return fallback
    return max(0, min(100, int(parse_float(value, fallback))))


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return text(value).lower() in {"1", "true", "yes", "y", "是", "已置顶"}


def normalize_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [text(item).lstrip("#") for item in value if text(item)]
    return [part.strip().lstrip("#") for part in re.split(r"[,;、|\n\r]+", str(value)) if part.strip()]


def normalize_handle(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    match = TIKTOK_URL_RE.search(raw)
    if match:
        raw = match.group(1)
    raw = raw.split("?")[0].strip().strip("/").lstrip("@")
    return raw if re.fullmatch(r"[A-Za-z0-9._-]{2,30}", raw) else ""


def tiktok_profile_url(handle: str) -> str:
    clean = normalize_handle(handle)
    return f"https://www.tiktok.com/@{clean}" if clean else "https://www.tiktok.com/"


def normalize_url(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    parsed = urlparse(raw)
    return raw if parsed.scheme in {"http", "https"} and parsed.netloc else ""


def normalize_status(value: Any) -> str:
    raw = text(value).lower()
    aliases = {label: key for key, label in STATUS_LABELS.items()}
    normalized = aliases.get(raw, raw or "new")
    return normalized if normalized in STATUS_LABELS else "new"


def normalize_choice(value: Any, choices: dict[str, str], fallback: str) -> str:
    raw = text(value).lower()
    aliases = {label: key for key, label in choices.items()}
    normalized = aliases.get(raw, raw or fallback)
    return normalized if normalized in choices else fallback


def stable_id(handle: str, name: str) -> str:
    base = handle or name or uuid.uuid4().hex[:10]
    clean = re.sub(r"[^A-Za-z0-9_-]+", "-", base).strip("-").lower()
    return clean or uuid.uuid4().hex[:10]


def normalize_history(value: Any) -> list[dict[str, str]]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return [{"id": uuid.uuid4().hex[:10], "type": "note", "date": today_iso(), "note": value, "followUpDate": ""}]
    if not isinstance(value, list):
        return []
    rows = []
    for item in value:
        if not isinstance(item, dict):
            continue
        rows.append({
            "id": text(item.get("id")) or uuid.uuid4().hex[:10],
            "type": text(item.get("type")) or "note",
            "date": text(item.get("date"))[:10] or today_iso(),
            "note": text(item.get("note")),
            "followUpDate": text(item.get("followUpDate"))[:10],
        })
    return sorted(rows, key=lambda row: row["date"], reverse=True)[:30]


def normalize_saved_works(value: Any) -> list[dict[str, str]]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            value = [{"url": value}]
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        return []

    rows: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for item in value:
        if isinstance(item, str):
            item = {"url": item}
        if not isinstance(item, dict):
            continue
        url = normalize_url(first_value(item, ["url", "workUrl", "videoUrl", "link", "作品链接"]))
        url_key = url.rstrip("/").lower()
        if not url or url_key in seen_urls:
            continue
        seen_urls.add(url_key)
        rows.append({
            "id": text(item.get("id")) or uuid.uuid4().hex[:10],
            "url": url,
            "title": text(first_value(item, ["title", "name", "收藏标题", "作品标题"])),
            "note": text(first_value(item, ["note", "notes", "收藏备注", "备注"])),
            "createdAt": text(first_value(item, ["createdAt", "savedAt", "收藏时间"])) or today_iso(),
        })
    return sorted(rows, key=lambda row: row["createdAt"], reverse=True)[:100]


def normalize_candidate(raw: dict[str, Any] | None) -> dict[str, Any]:
    raw = raw or {}
    handle = normalize_handle(first_value(raw, ["handle", "username", "account", "tiktok", "tiktokUrl", "profileUrl", "账号"]))
    name = text(first_value(raw, ["name", "displayName", "creator", "达人", "名称"])) or handle
    followers = parse_count(first_value(raw, ["followers", "followerCount", "粉丝数", "粉丝"]))
    avg_views = parse_count(first_value(raw, ["avgViews", "averageViews", "views", "平均播放", "平均播放量"]))
    ratio_value = parse_float(first_value(raw, ["viewFollowerRatio", "viewToFollowerRatio", "播放粉丝比"]))
    if not ratio_value and followers:
        ratio_value = round(avg_views / followers, 3)
    profile_url = normalize_url(first_value(raw, ["tiktokUrl", "profileUrl", "url", "主页链接"])) or tiktok_profile_url(handle)
    saved_works = normalize_saved_works(first_value(raw, ["savedWorks", "favoriteWorks", "作品收藏", "收藏作品", "作品链接"]))
    featured_work_id = text(first_value(raw, ["featuredWorkId", "referenceWorkId", "重点作品", "文案参考作品"]))
    if featured_work_id and not any(item["id"] == featured_work_id for item in saved_works):
        featured_work_id = ""
    created_at = text(raw.get("createdAt")) or now_iso()
    updated_at = text(raw.get("updatedAt")) or created_at
    return {
        "id": text(raw.get("id")) or stable_id(handle, name),
        "handle": handle,
        "pinned": boolish(first_value(raw, ["pinned", "pin", "starred", "置顶"])),
        "name": name,
        "creatorType": text(first_value(raw, ["creatorType", "bloggerType", "达人类型"])) or "TikTok Creator",
        "niche": text(first_value(raw, ["niche", "category", "segment", "赛道"])) or "待判断",
        "location": text(first_value(raw, ["location", "country", "city", "地区"])) or "Japan",
        "followers": followers,
        "avgViews": avg_views,
        "medianViews": parse_count(first_value(raw, ["medianViews", "中位播放", "中位播放量"])),
        "engagementRate": parse_percent(first_value(raw, ["engagementRate", "engagement", "er", "互动率"])),
        "avgLikes": parse_count(first_value(raw, ["avgLikes", "likes", "平均点赞"])),
        "avgComments": parse_count(first_value(raw, ["avgComments", "comments", "平均评论"])),
        "avgShares": parse_count(first_value(raw, ["avgShares", "shares", "平均分享"])),
        "viewFollowerRatio": round(ratio_value, 3),
        "videoFrequency": round(parse_float(first_value(raw, ["videoFrequency", "videosPerWeek", "周更频率"])), 1),
        "contentFit": parse_score(first_value(raw, ["contentFit", "内容匹配"]), 72),
        "audienceFit": parse_score(first_value(raw, ["audienceFit", "受众匹配"]), 72),
        "brandSafety": parse_score(first_value(raw, ["brandSafety", "品牌安全"]), 82),
        "collabSignal": parse_score(first_value(raw, ["collabSignal", "合作信号"]), 55),
        "contactMethod": text(first_value(raw, ["contactMethod", "contact", "联系方式"])) or "dm",
        "email": text(first_value(raw, ["email", "mail", "邮箱"])),
        "tiktokUrl": profile_url,
        "avatarUrl": normalize_url(first_value(raw, ["avatarUrl", "avatar", "profileImage", "image", "头像链接"])),
        "status": normalize_status(first_value(raw, ["status", "状态"])),
        "followUpDate": text(first_value(raw, ["followUpDate", "nextFollowUp", "跟进日期"]))[:10],
        "lastContacted": text(first_value(raw, ["lastContacted", "lastContactedAt", "最后联系"]))[:10],
        "invitationSentAt": text(first_value(raw, ["invitationSentAt", "inviteSentAt", "发送邀约时间"]))[:10],
        "connectionAt": text(first_value(raw, ["connectionAt", "connectedAt", "建联时间"]))[:10],
        "partnershipStage": normalize_choice(first_value(raw, ["partnershipStage", "合作阶段"]), PARTNERSHIP_STAGES, "none"),
        "quoteJpy": parse_count(first_value(raw, ["quoteJpy", "quote", "报价"])),
        "collabProduct": text(first_value(raw, ["collabProduct", "product", "合作产品"])),
        "sampleStatus": text(first_value(raw, ["sampleStatus", "样品状态"])) or "none",
        "sampleCostJpy": parse_count(first_value(raw, ["sampleCostJpy", "sampleCost", "样品成本"])),
        "recipientName": text(first_value(raw, ["recipientName", "收货姓名"])),
        "postalCode": text(first_value(raw, ["postalCode", "zip", "邮编"])),
        "shippingAddress": text(first_value(raw, ["shippingAddress", "address", "详细地址"])),
        "phoneNumber": text(first_value(raw, ["phoneNumber", "phone", "手机号"])),
        "orderNumber": text(first_value(raw, ["orderNumber", "orderNo", "订单编号"])),
        "shippingTracking": text(first_value(raw, ["shippingTracking", "trackingNumber", "物流单号"])),
        "shippedAt": text(first_value(raw, ["shippedAt", "发货时间"]))[:10],
        "receivedAt": text(first_value(raw, ["receivedAt", "收货时间"]))[:10],
        "videoFormat": text(first_value(raw, ["videoFormat", "contentFormat", "视频形式"])) or "short_video",
        "videoProgress": normalize_choice(first_value(raw, ["videoProgress", "视频进度"]), VIDEO_PROGRESS, "not_started"),
        "scriptDueDate": text(first_value(raw, ["scriptDueDate", "脚本日期"]))[:10],
        "draftDueDate": text(first_value(raw, ["draftDueDate", "初稿日期"]))[:10],
        "postDate": text(first_value(raw, ["postDate", "publishDate", "发布时间"]))[:10],
        "postUrl": normalize_url(first_value(raw, ["postUrl", "videoUrl", "视频链接"])),
        "savedWorks": saved_works,
        "featuredWorkId": featured_work_id,
        "sparkAdsStatus": text(first_value(raw, ["sparkAdsStatus", "sparkStatus", "Spark Ads状态"])) or "not_requested",
        "sparkAuthorizationCode": text(first_value(raw, ["sparkAuthorizationCode", "sparkCode", "Spark授权码"])),
        "usageRightsDays": parse_count(first_value(raw, ["usageRightsDays", "usageDays", "素材使用天数"])),
        "couponCode": text(first_value(raw, ["couponCode", "discountCode", "粉丝折扣码"])),
        "orders": parse_count(first_value(raw, ["orders", "orderCount", "订单数"])),
        "revenueJpy": parse_count(first_value(raw, ["revenueJpy", "revenue", "收入"])),
        "tags": normalize_list(first_value(raw, ["tags", "tag", "labels", "标签"]))[:10],
        "notes": text(first_value(raw, ["notes", "note", "备注"])),
        "contactHistory": normalize_history(first_value(raw, ["contactHistory", "history", "联系历史"])),
        "createdAt": created_at,
        "updatedAt": updated_at,
    }


def score_candidate(candidate: dict[str, Any]) -> tuple[int, dict[str, int]]:
    views = candidate.get("avgViews", 0)
    engagement = candidate.get("engagementRate", 0)
    ratio = candidate.get("viewFollowerRatio", 0)
    frequency = candidate.get("videoFrequency", 0)
    view_score = 22 if views >= 50_000 else 18 if views >= 20_000 else 13 if views >= 5_000 else 6 if views else 0
    engagement_score = 20 if engagement >= 8 else 17 if engagement >= 5 else 12 if engagement >= 2.5 else 6 if engagement else 0
    ratio_score = 18 if ratio >= 1 else 15 if ratio >= 0.5 else 10 if ratio >= 0.2 else 5 if ratio > 0 else 0
    frequency_score = 10 if frequency >= 5 else 8 if frequency >= 3 else 5 if frequency >= 1 else 2 if frequency > 0 else 0
    content_score = round(candidate.get("contentFit", 0) / 100 * 12)
    audience_score = round(candidate.get("audienceFit", 0) / 100 * 8)
    safety_score = round(candidate.get("brandSafety", 0) / 100 * 4)
    contact_score = 6 if candidate.get("email") else 4 if candidate.get("contactMethod") == "dm" else 2
    breakdown = {
        "views": view_score,
        "engagement": engagement_score,
        "ratio": ratio_score,
        "frequency": frequency_score,
        "content": content_score,
        "audience": audience_score,
        "safety": safety_score,
        "contact": contact_score,
    }
    return min(100, sum(breakdown.values())), breakdown


def tier_for(score: int) -> str:
    return "S" if score >= 84 else "A" if score >= 72 else "B" if score >= 58 else "C" if score >= 42 else "D"


def build_score_items(breakdown: dict[str, int]) -> list[dict[str, Any]]:
    labels = {
        "views": ("播放表现", 22), "engagement": ("互动率", 20), "ratio": ("播放粉丝比", 18),
        "frequency": ("更新频率", 10), "content": ("内容匹配", 12), "audience": ("受众匹配", 8),
        "safety": ("品牌安全", 4), "contact": ("可联系性", 6),
    }
    return [
        {"key": key, "label": label, "value": breakdown.get(key, 0), "max": maximum, "pct": round(breakdown.get(key, 0) / maximum * 100, 1)}
        for key, (label, maximum) in labels.items()
    ]


def build_drafts(candidate: dict[str, Any]) -> dict[str, str]:
    name = candidate.get("name") or candidate.get("handle") or "クリエイター"
    niche = candidate.get("niche") if candidate.get("niche") not in {"", "待判断"} else "ファッション"
    featured_work = next((item for item in candidate.get("savedWorks", []) if item.get("id") == candidate.get("featuredWorkId")), None)
    work_title = text(featured_work.get("title")) if featured_work else ""
    work_observation = (
        f"特に「{work_title}」の投稿が印象的で、動画のテンポや自然な着こなし表現がとても素敵だと感じました。\n\n"
        if work_title
        else f"{name}様のTikTokでの{niche}投稿を拝見し、動画のテンポや自然な着こなし表現がとても素敵だと感じました。\n\n"
    )
    format_label = "ショート動画"
    if candidate.get("videoFormat") == "live":
        format_label = "TikTok LIVE"
    elif candidate.get("videoFormat") == "photo_mode":
        format_label = "フォトモード"
    dm = (
        f"{name}様、突然のDM失礼いたします。\n\n"
        "レディースファッションブランドSOSOVEのPR担当Annieと申します。\n"
        f"{work_observation}"
        f"新作アイテムを使った{format_label}の有償コラボをご相談したく、ご連絡いたしました。"
        "商品は無料でご提供し、投稿報酬もご用意いたします。\n\n"
        "Spark Adsや素材の二次利用をご希望する場合は、期間と条件を事前にご相談いたします。"
        "ご興味がございましたら、詳細をお送りいたします。よろしくお願いいたします。"
    )
    email_observation = (
        f"特に「{work_title}」の投稿が印象的で、その世界観に合わせた新作アイテムの有償コラボをご相談したくご連絡いたしました。"
        if work_title
        else f"TikTokでの{niche}投稿を拝見し、新作アイテムの有償コラボをご相談したくご連絡いたしました。"
    )
    email = (
        f"{name}様\n\n突然のご連絡失礼いたします。SOSOVE PR担当のAnnieです。\n\n"
        f"{email_observation}"
        "無料サンプルと投稿報酬をご用意しております。動画形式、納期、Spark Ads、二次利用期間は事前に合意した上で進行いたします。\n\n"
        "ご検討いただけますと幸いです。よろしくお願いいたします。"
    )
    followup = (
        f"{name}様、先日SOSOVEのTikTokコラボについてご連絡したAnnieです。\n"
        "念のため再度ご連絡いたしました。ご興味がなければご返信は不要です。"
        "条件確認のみでも大丈夫ですので、ご都合のよい時にご確認いただけますと幸いです。"
    )
    return {"dm": dm, "email": email, "followup": followup, "emailSubject": "【SOSOVE】TikTok有償コラボのご相談"}


def build_manual_checklist(candidate: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"key": "views", "label": "确认最近 10 条视频的中位播放量，避免只看爆款"},
        {"key": "audience", "label": "确认日本受众、语言与女装购买人群匹配"},
        {"key": "sponsored", "label": "检查近期广告比例和同类品牌合作冲突"},
        {"key": "rights", "label": "发送前明确 Spark Ads、二次利用期限和授权范围"},
        {"key": "manual", "label": "TikTok 私信由人工确认发送，不做无人值守群发"},
    ]


def enrich(candidate: dict[str, Any]) -> dict[str, Any]:
    row = normalize_candidate(candidate)
    score, breakdown = score_candidate(row)
    row.update({
        "score": score,
        "tier": tier_for(score),
        "scoreBreakdownItems": build_score_items(breakdown),
        "drafts": build_drafts(row),
        "manualChecklist": build_manual_checklist(row),
    })
    return row


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        payload = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    rows = payload.get("candidates") if isinstance(payload, dict) else payload
    return [normalize_candidate(row) for row in rows] if isinstance(rows, list) else []


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATES_PATH.write_text(
        json.dumps({"updatedAt": now_iso(), "candidates": [normalize_candidate(row) for row in candidates]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def task_counts(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    today = today_iso()
    return {
        "dueToday": [row["id"] for row in candidates if row.get("followUpDate") == today],
        "overdue": [row["id"] for row in candidates if row.get("followUpDate") and row["followUpDate"] < today and row["status"] not in {"approved", "rejected"}],
        "replied": [row["id"] for row in candidates if row["status"] == "replied"],
        "negotiating": [row["id"] for row in candidates if row["status"] == "negotiating"],
        "missingMetrics": [row["id"] for row in candidates if not row.get("avgViews") or not row.get("engagementRate")],
        "samplePending": [row["id"] for row in candidates if row.get("partnershipStage") == "sample_pending"],
        "shipping": [row["id"] for row in candidates if row.get("sampleStatus") == "sent" and not row.get("receivedAt")],
        "draftReview": [row["id"] for row in candidates if row.get("videoProgress") in {"script_review", "draft_review", "revision"}],
        "publish": [row["id"] for row in candidates if row.get("partnershipStage") == "content_scheduled" and not row.get("postUrl")],
    }


def public_search_setup_state() -> dict[str, bool]:
    return {
        "googleCse": bool(os.getenv("GOOGLE_CSE_API_KEY") and (os.getenv("GOOGLE_CSE_CX") or os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID"))),
        "serpApi": bool(os.getenv("SERPAPI_API_KEY")),
    }


def build_workspace_payload() -> dict[str, Any]:
    candidates = [enrich(row) for row in load_candidates()]
    candidates.sort(key=lambda row: (bool(row.get("pinned")), row["score"], row.get("updatedAt", "")), reverse=True)
    total = len(candidates)
    cost = sum(row.get("quoteJpy", 0) + row.get("sampleCostJpy", 0) for row in candidates)
    revenue = sum(row.get("revenueJpy", 0) for row in candidates)
    return {
        "ok": True,
        "platform": "tiktok",
        "statusLabels": STATUS_LABELS,
        "partnershipStages": PARTNERSHIP_STAGES,
        "videoProgressLabels": VIDEO_PROGRESS,
        "csvFields": CSV_FIELDS,
        "stats": {
            "total": total,
            "ready": sum(1 for row in candidates if row["score"] >= 58 and row["status"] not in {"contacted", "rejected"}),
            "contacted": sum(1 for row in candidates if row["status"] in {"contacted", "replied", "negotiating", "approved"}),
            "replied": sum(1 for row in candidates if row["status"] in {"replied", "negotiating", "approved"}),
            "avgScore": round(sum(row["score"] for row in candidates) / total, 1) if total else 0,
            "estimatedCostJpy": sum(row.get("quoteJpy", 0) for row in candidates if row["score"] >= 58),
            "orders": sum(row.get("orders", 0) for row in candidates),
            "revenueJpy": revenue,
            "costJpy": cost,
            "roiPct": round((revenue - cost) / cost * 100, 1) if cost else 0,
        },
        "tasks": task_counts(candidates),
        "searchSetup": public_search_setup_state(),
        "candidates": candidates,
        "source": {"candidatePath": str(CANDIDATES_PATH), "syncedAt": now_iso()},
    }


def parse_csv_rows(csv_text: str) -> list[dict[str, Any]]:
    try:
        dialect = csv.Sniffer().sniff(csv_text[:2048])
    except csv.Error:
        dialect = csv.excel
    return [dict(row) for row in csv.DictReader(io.StringIO(csv_text), dialect=dialect)]


def preview_import_candidates(csv_text: str) -> dict[str, Any]:
    existing = {row["handle"].lower() for row in load_candidates() if row.get("handle")}
    seen: set[str] = set()
    rows = []
    counts = {"add": 0, "update": 0, "duplicate": 0, "skip": 0}
    for index, raw in enumerate(parse_csv_rows(csv_text), start=1):
        candidate = normalize_candidate(raw)
        key = candidate.get("handle", "").lower()
        action = "skip" if not key else "duplicate" if key in seen else "update" if key in existing else "add"
        if key:
            seen.add(key)
        counts[action] += 1
        rows.append({"row": index, "action": action, "candidate": enrich(candidate)})
    return {"ok": True, "summary": {**counts, "rows": len(rows)}, "rows": rows[:100]}


def import_candidates_from_csv(csv_text: str) -> dict[str, Any]:
    existing = load_candidates()
    by_handle = {row["handle"].lower(): row for row in existing if row.get("handle")}
    added = updated = skipped = 0
    for raw in parse_csv_rows(csv_text):
        candidate = normalize_candidate(raw)
        key = candidate.get("handle", "").lower()
        if not key:
            skipped += 1
            continue
        if key in by_handle:
            current = by_handle[key]
            merged = {**current, **candidate, "id": current["id"], "createdAt": current["createdAt"], "updatedAt": now_iso()}
            by_handle[key] = normalize_candidate(merged)
            updated += 1
        else:
            by_handle[key] = candidate
            added += 1
    save_candidates(list(by_handle.values()))
    return {"ok": True, "added": added, "updated": updated, "skipped": skipped, "total": len(by_handle)}


def extract_profiles(source_text: str) -> list[str]:
    handles = []
    seen: set[str] = set()
    for pattern in (TIKTOK_URL_RE, TIKTOK_AT_RE):
        for match in pattern.finditer(source_text or ""):
            handle = normalize_handle(match.group(1))
            if handle and handle.lower() not in seen:
                seen.add(handle.lower())
                handles.append(handle)
    return handles


def import_profiles_from_text(source_text: str, niche: str = "") -> dict[str, Any]:
    handles = extract_profiles(source_text)
    existing = load_candidates()
    by_handle = {row["handle"].lower(): row for row in existing if row.get("handle")}
    added = updated = 0
    for handle in handles:
        key = handle.lower()
        if key in by_handle:
            row = dict(by_handle[key])
            if niche and row.get("niche") in {"", "待判断"}:
                row["niche"] = niche
            row["updatedAt"] = now_iso()
            by_handle[key] = normalize_candidate(row)
            updated += 1
        else:
            by_handle[key] = normalize_candidate({
                "handle": handle, "name": handle, "niche": niche or "待判断", "status": "review",
                "tiktokUrl": tiktok_profile_url(handle), "notes": "从公开 TikTok 链接/handle 列表导入，资料待人工确认。",
            })
            added += 1
    save_candidates(list(by_handle.values()))
    return {"ok": True, "added": added, "updated": updated, "total": len(by_handle), "handles": handles}


def build_public_search_query(keyword: str) -> str:
    lines = [line.strip() for line in text(keyword).splitlines() if line.strip()]
    body = " OR ".join(f'"{line}"' for line in lines) if len(lines) > 1 else f'"{lines[0] if lines else "japanese fashion creator"}"'
    return f"site:tiktok.com/@ ({body})"


def read_json_url(url: str, params: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(f"{url}?{urlencode(params)}", headers={"User-Agent": "TikTokCreatorOutreach/0.1"})
    with urllib.request.urlopen(request, timeout=15) as response:
        parsed = json.loads(response.read().decode("utf-8"))
    return parsed if isinstance(parsed, dict) else {}


def public_search_preview(keyword: str, engine: str = "auto", limit: int = 10) -> dict[str, Any]:
    setup = public_search_setup_state()
    selected = engine
    if selected == "auto":
        selected = "google_cse" if setup["googleCse"] else "serpapi" if setup["serpApi"] else "google_cse"
    query = build_public_search_query(keyword)
    configured = setup["googleCse"] if selected == "google_cse" else setup["serpApi"]
    results: list[dict[str, str]] = []
    error = ""
    if configured:
        try:
            if selected == "serpapi":
                payload = read_json_url("https://serpapi.com/search.json", {"engine": "google", "q": query, "api_key": os.getenv("SERPAPI_API_KEY", ""), "num": min(30, limit), "gl": "jp", "hl": "ja"})
                source = payload.get("organic_results", [])
                results = [{"title": text(row.get("title")), "link": text(row.get("link")), "snippet": text(row.get("snippet"))} for row in source if isinstance(row, dict)][:limit]
            else:
                payload = read_json_url("https://www.googleapis.com/customsearch/v1", {"key": os.getenv("GOOGLE_CSE_API_KEY", ""), "cx": os.getenv("GOOGLE_CSE_CX") or os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID", ""), "q": query, "num": min(10, limit)})
                source = payload.get("items", [])
                results = [{"title": text(row.get("title")), "link": text(row.get("link")), "snippet": text(row.get("snippet"))} for row in source if isinstance(row, dict)][:limit]
        except (OSError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            error = str(exc)[:500]
    source_text = "\n".join(part for row in results for part in [row["title"], row["link"], row["snippet"]] if part)
    handles = extract_profiles(source_text)
    return {
        "ok": True, "configured": configured, "engine": selected, "query": query,
        "searchUrl": f"https://www.google.com/search?q={quote_plus(query)}", "resultCount": len(results),
        "handles": handles, "sourceText": source_text, "error": error, "setup": setup,
    }


def upsert_candidate(payload: dict[str, Any]) -> dict[str, Any]:
    rows = load_candidates()
    candidate = normalize_candidate(payload)
    if not candidate.get("handle"):
        return {"ok": False, "error": "missing TikTok handle"}
    found = False
    output = []
    for row in rows:
        if row["id"] == candidate["id"] or row.get("handle", "").lower() == candidate["handle"].lower():
            merged = {**row, **candidate, "id": row["id"], "createdAt": row["createdAt"], "updatedAt": now_iso()}
            if "pinned" not in payload:
                merged["pinned"] = row.get("pinned", False)
            candidate = normalize_candidate(merged)
            output.append(candidate)
            found = True
        else:
            output.append(row)
    if not found:
        output.append(candidate)
    save_candidates(output)
    return {"ok": True, "created": not found, "candidate": enrich(candidate)}


def update_candidate_status(candidate_id: str, status: str) -> dict[str, Any]:
    rows = load_candidates()
    changed = False
    normalized = normalize_status(status)
    for row in rows:
        if row["id"] == candidate_id:
            row["status"] = normalized
            row["updatedAt"] = now_iso()
            changed = True
            break
    if changed:
        save_candidates(rows)
    return {"ok": changed, "status": normalized}


def update_candidate_pin(candidate_id: str, pinned: Any) -> dict[str, Any]:
    rows = load_candidates()
    changed = False
    next_value = boolish(pinned)
    for row in rows:
        if row["id"] == candidate_id:
            row["pinned"] = next_value
            row["updatedAt"] = now_iso()
            changed = True
            break
    if changed:
        save_candidates(rows)
    return {"ok": changed, "pinned": next_value}


def mark_candidate_contacted(candidate_id: str, note: str = "", follow_up_date: str = "") -> dict[str, Any]:
    rows = load_candidates()
    changed = False
    for row in rows:
        if row["id"] == candidate_id:
            row["status"] = "contacted" if row["status"] in {"new", "review", "ready"} else row["status"]
            row["lastContacted"] = today_iso()
            row["invitationSentAt"] = row.get("invitationSentAt") or today_iso()
            row["followUpDate"] = text(follow_up_date)[:10] or (date.today() + timedelta(days=3)).isoformat()
            row["contactHistory"] = normalize_history([{
                "id": uuid.uuid4().hex[:10], "type": "contacted", "date": today_iso(),
                "note": note or "已记录 TikTok 建联", "followUpDate": row["followUpDate"],
            }, *row.get("contactHistory", [])])
            row["updatedAt"] = now_iso()
            changed = True
            break
    if changed:
        save_candidates(rows)
    return {"ok": changed}


def update_candidate_followup(candidate_id: str, follow_up_date: str) -> dict[str, Any]:
    rows = load_candidates()
    changed = False
    for row in rows:
        if row["id"] == candidate_id:
            row["followUpDate"] = text(follow_up_date)[:10]
            row["updatedAt"] = now_iso()
            changed = True
            break
    if changed:
        save_candidates(rows)
    return {"ok": changed, "followUpDate": text(follow_up_date)[:10]}


def batch_update_candidates(candidate_ids: Any, action: str, value: Any = "", confirm: str = "") -> dict[str, Any]:
    ids = {text(item) for item in candidate_ids} if isinstance(candidate_ids, list) else set()
    ids.discard("")
    if not ids:
        return {"ok": False, "error": "no candidates selected", "updated": 0}
    if action not in {"status", "tags", "followup", "delete"}:
        return {"ok": False, "error": "unsupported batch action", "updated": 0}

    rows = load_candidates()
    matched = [row for row in rows if row["id"] in ids]
    if not matched:
        return {"ok": False, "error": "candidates not found", "updated": 0}

    if action == "delete":
        if confirm != "DELETE_SELECTED":
            return {"ok": False, "error": "confirmation required", "updated": 0}
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        backup = DATA_DIR / f"candidates_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup.write_text(json.dumps({"candidates": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
        save_candidates([row for row in rows if row["id"] not in ids])
        return {"ok": True, "action": action, "deleted": len(matched), "updated": len(matched)}

    additions = normalize_list(value) if action == "tags" else []
    for row in matched:
        if action == "status":
            row["status"] = normalize_status(value)
        elif action == "tags":
            row["tags"] = list(dict.fromkeys([*row.get("tags", []), *additions]))[:10]
        elif action == "followup":
            row["followUpDate"] = text(value)[:10]
        row["updatedAt"] = now_iso()
    save_candidates(rows)
    return {"ok": True, "action": action, "updated": len(matched)}


def delete_candidate(candidate_id: str) -> dict[str, Any]:
    rows = load_candidates()
    remaining = [row for row in rows if row["id"] != candidate_id]
    if len(remaining) == len(rows):
        return {"ok": False, "error": "candidate not found"}
    save_candidates(remaining)
    return {"ok": True, "deleted": candidate_id}


def delete_all_candidates(confirm: str = "") -> dict[str, Any]:
    if confirm != "DELETE":
        return {"ok": False, "error": "confirmation required", "deleted": 0}
    rows = load_candidates()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if rows:
        backup = DATA_DIR / f"candidates_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup.write_text(json.dumps({"candidates": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    save_candidates([])
    return {"ok": True, "deleted": len(rows), "total": 0}


def build_copy_prompt(candidate: dict[str, Any], options: dict[str, Any]) -> list[dict[str, str]]:
    compact = {key: candidate.get(key) for key in ["handle", "name", "niche", "location", "followers", "avgViews", "medianViews", "engagementRate", "viewFollowerRatio", "videoFrequency", "tags", "notes", "videoFormat"]}
    featured_work = next((item for item in candidate.get("savedWorks", []) if item.get("id") == candidate.get("featuredWorkId")), None)
    if featured_work:
        compact["referenceWork"] = {key: featured_work.get(key) for key in ["title", "note", "url"]}
    return [
        {"role": "system", "content": "You write concise Japanese TikTok creator outreach copy for SOSOVE. Return JSON only with keys subject and text. Mention paid collaboration and free sample, but do not invent fees. Treat Spark Ads and usage rights as terms that require prior agreement. If referenceWork is present, naturally mention that specific post without inventing details beyond its title and note."},
        {"role": "user", "content": json.dumps({"candidate": compact, "options": options, "requirements": ["Japanese", "natural", "TikTok-specific", "personalized from referenceWork when present", "human review before sending"]}, ensure_ascii=False)},
    ]


def generate_copy_draft(payload: dict[str, Any]) -> dict[str, Any]:
    candidate = normalize_candidate(payload.get("candidate") if isinstance(payload.get("candidate"), dict) else {})
    options = payload.get("options") if isinstance(payload.get("options"), dict) else {}
    fallback = build_drafts(candidate)
    provider = text(payload.get("provider") or os.getenv("TIKTOK_OUTREACH_COPY_MODEL_PROVIDER") or os.getenv("OUTREACH_COPY_MODEL_PROVIDER") or "local").lower()
    if provider not in {"api", "model", "openai", "openai_compatible", "cpa"}:
        return {"ok": True, "provider": "local", "configured": False, "text": fallback["dm"], "subject": fallback["emailSubject"], "warnings": []}
    config_payload = dict(payload)
    config_payload["apiBaseUrl"] = payload.get("apiBaseUrl") or os.getenv("TIKTOK_OUTREACH_COPY_MODEL_BASE_URL") or os.getenv("OUTREACH_COPY_MODEL_BASE_URL")
    config_payload["model"] = payload.get("model") or os.getenv("TIKTOK_OUTREACH_COPY_MODEL_NAME") or os.getenv("OUTREACH_COPY_MODEL_NAME")
    config_payload["apiKey"] = payload.get("apiKey") or os.getenv("TIKTOK_OUTREACH_COPY_MODEL_API_KEY") or os.getenv("OUTREACH_COPY_MODEL_API_KEY")
    config = resolve_copy_model_config(config_payload)
    if not config.get("baseUrl") or not config.get("model"):
        return {"ok": True, "provider": "local", "configured": False, "text": fallback["dm"], "subject": fallback["emailSubject"], "warnings": ["模型接口未配置完整，已使用 TikTok 本地模板。"]}
    try:
        result = call_openai_compatible_copy_model(config, build_copy_prompt(candidate, options))
    except (OSError, TimeoutError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError) as exc:
        return {"ok": True, "provider": "local", "configured": False, "text": fallback["dm"], "subject": fallback["emailSubject"], "warnings": [f"模型调用失败，已使用本地模板：{exc}"]}
    return {"ok": True, "provider": "openai_compatible", "configured": True, "model": config.get("model"), "text": text(result.get("text")) or fallback["dm"], "subject": text(result.get("subject")) or fallback["emailSubject"], "warnings": []}


def test_copy_model_config(payload: dict[str, Any]) -> dict[str, Any]:
    return shared_test_copy_model_config(payload)


def classify_reply(reply_text: str) -> tuple[str, str, str]:
    rules = [
        (r"料金|費用|報酬|見積|fee|price|报价", "price", "报价/费用", "negotiating"),
        (r"興味|検討|お願い|interested|可以|合作", "interested", "有兴趣", "replied"),
        (r"商品|画像|URL|詳細|product|产品", "product", "想看产品", "replied"),
        (r"難しい|辞退|今回は|not interested|拒绝", "rejected", "拒绝合作", "rejected"),
    ]
    for pattern, key, label, status in rules:
        if re.search(pattern, reply_text, re.IGNORECASE):
            return key, label, status
    return "review", "需要人工判断", "replied"


def generate_reply_draft(payload: dict[str, Any]) -> dict[str, Any]:
    reply_text = text(payload.get("replyText"))
    candidate = normalize_candidate(payload.get("candidate") if isinstance(payload.get("candidate"), dict) else {})
    if not reply_text:
        return {"ok": False, "error": "missing reply text"}
    key, label, status = classify_reply(reply_text)
    name = candidate.get("name") or candidate.get("handle") or "クリエイター"
    drafts = {
        "price": f"{name}様、ご返信ありがとうございます。料金条件をご共有いただきありがとうございます。投稿形式、納期、Spark Adsおよび二次利用条件を含めて社内で確認し、改めてご連絡いたします。",
        "interested": f"{name}様、ご返信ありがとうございます。ご興味をお持ちいただき嬉しいです。候補商品、動画形式、報酬条件、納期、素材利用条件を整理してお送りします。",
        "product": f"{name}様、ご返信ありがとうございます。候補商品と詳細資料を整理してお送りします。気になるアイテムや撮影しやすい動画形式がございましたら教えてください。",
        "rejected": f"{name}様、ご丁寧にご返信いただきありがとうございます。承知いたしました。また企画内容が合う機会がございましたら、改めてご相談できれば幸いです。",
        "review": f"{name}様、ご返信ありがとうございます。内容を確認し、条件を整理した上で改めてご連絡いたします。",
    }
    return {"ok": True, "configured": False, "key": key, "label": label, "status": status, "draft": drafts[key], "note": f"TikTok 达人回复：{label}\n{reply_text[:400]}", "warnings": []}


def export_candidates_csv() -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in load_candidates():
        data = {field: row.get(field, "") for field in CSV_FIELDS}
        data["tags"] = "、".join(row.get("tags") or [])
        data["savedWorks"] = json.dumps(row.get("savedWorks") or [], ensure_ascii=False, separators=(",", ":"))
        writer.writerow(data)
    return output.getvalue()
