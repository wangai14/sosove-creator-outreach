import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from instagram_creator_outreach import backend


class InstagramCreatorOutreachBackendTests(unittest.TestCase):
    def test_parse_count_supports_common_creator_notation(self):
        self.assertEqual(backend.parse_count("12.5k"), 12500)
        self.assertEqual(backend.parse_count("3.2万"), 32000)
        self.assertEqual(backend.parse_count("9,800"), 9800)

    def test_score_rewards_micro_creator_with_strong_engagement(self):
        candidate = backend.normalize_candidate(
            {
                "handle": "petite_test",
                "followers": "18,000",
                "engagementRate": "5.5%",
                "contentFit": 90,
                "audienceFit": 88,
                "brandSafety": 92,
                "collabSignal": 70,
                "contactMethod": "email",
                "tags": "低身長、着回し",
                "notes": "Good comment quality",
                "topPosts": "150cmコーデ",
            }
        )

        score, breakdown = backend.score_candidate(candidate)

        self.assertGreaterEqual(score, 80)
        self.assertEqual(breakdown["followers"], 18)
        self.assertEqual(breakdown["contact"], 6)

    def test_drafts_are_personalized_for_candidate(self):
        candidate = backend.normalize_candidate(
            {
                "handle": "office_creator",
                "name": "Rina",
                "niche": "オフィスカジュアル",
                "topPosts": ["週5コーデ"],
                "tags": ["通勤", "きれいめ"],
            }
        )

        drafts = backend.build_outreach_drafts(candidate)

        self.assertIn("Rinaさん", drafts["dm"])
        self.assertIn("週5コーデ", drafts["dm"])
        self.assertIn("通勤", drafts["email"])
        self.assertIn("SOSOVE", drafts["emailSubject"])

    def test_copy_generation_local_provider_returns_ready_text(self):
        result = backend.generate_copy_draft(
            {
                "provider": "local",
                "candidate": {
                    "handle": "office_creator",
                    "name": "Rina",
                    "niche": "office fashion",
                    "tags": ["office", "onepiece"],
                },
                "options": {
                    "scenario": "product_seed",
                    "tone": "warm",
                    "length": "short",
                    "productLabel": "office onepiece",
                },
            }
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["provider"], "local")
        self.assertFalse(result["configured"])
        self.assertIn("SOSOVE", result["text"])
        self.assertIn("Rina", result["text"])
        self.assertIn("subject", result)

    def test_copy_generation_uses_openai_compatible_model_when_configured(self):
        with patch.object(
            backend,
            "call_openai_compatible_copy_model",
            return_value={"subject": "Model subject", "text": "Model generated outreach"},
        ) as model_call:
            result = backend.generate_copy_draft(
                {
                    "provider": "api",
                    "apiBaseUrl": "https://api.example.com/v1",
                    "model": "example-chat",
                    "apiKey": "test-key",
                    "candidate": {"handle": "creator_one", "name": "Aki"},
                    "options": {"scenario": "reels", "tone": "polite"},
                }
            )

        self.assertTrue(result["ok"])
        self.assertTrue(result["configured"])
        self.assertEqual(result["provider"], "openai_compatible")
        self.assertEqual(result["model"], "example-chat")
        self.assertEqual(result["text"], "Model generated outreach")
        self.assertEqual(result["subject"], "Model subject")
        model_call.assert_called_once()

    def test_copy_model_config_test_uses_openai_compatible_adapter(self):
        with patch.object(
            backend,
            "call_openai_compatible_copy_model",
            return_value={"subject": "ok", "text": "ok"},
        ) as model_call:
            result = backend.test_copy_model_config(
                {
                    "provider": "api",
                    "apiBaseUrl": "https://api.example.com/v1",
                    "model": "example-chat",
                    "apiKey": "test-key",
                }
            )

        self.assertTrue(result["ok"])
        self.assertTrue(result["configured"])
        self.assertEqual(result["provider"], "openai_compatible")
        self.assertEqual(result["model"], "example-chat")
        model_call.assert_called_once()

    def test_copy_model_config_supports_cpa_proxy_mode(self):
        config = backend.resolve_copy_model_config(
            {
                "provider": "cpa",
                "apiBaseUrl": "http://proxy.example.com/v1",
                "model": "gpt-5.5",
                "apiKey": "test-key",
            }
        )
        headers = {}
        backend.apply_model_auth_header(headers, config)

        self.assertEqual(config["compatMode"], "cpa")
        self.assertEqual(config["authMode"], "bearer")
        self.assertEqual(headers["Authorization"], "Bearer test-key")

    def test_reply_generation_local_provider_classifies_and_drafts(self):
        result = backend.generate_reply_draft(
            {
                "provider": "local",
                "candidate": {"handle": "creator_one", "name": "Aki"},
                "replyText": "料金はいくらになりますか？",
            }
        )

        self.assertTrue(result["ok"])
        self.assertFalse(result["configured"])
        self.assertEqual(result["key"], "price")
        self.assertEqual(result["status"], "negotiating")
        self.assertIn("Akiさん", result["draft"])

    def test_reply_generation_uses_openai_compatible_model_when_configured(self):
        with patch.object(
            backend,
            "call_openai_compatible_copy_model",
            return_value={"subject": "", "text": "Model generated reply"},
        ) as model_call:
            result = backend.generate_reply_draft(
                {
                    "provider": "api",
                    "apiBaseUrl": "https://api.example.com/v1",
                    "model": "example-chat",
                    "apiKey": "test-key",
                    "candidate": {"handle": "creator_one", "name": "Aki"},
                    "replyText": "興味があります。前向きに検討したいです。",
                }
            )

        self.assertTrue(result["ok"])
        self.assertTrue(result["configured"])
        self.assertEqual(result["provider"], "openai_compatible")
        self.assertEqual(result["model"], "example-chat")
        self.assertEqual(result["draft"], "Model generated reply")
        self.assertEqual(result["key"], "interested")
        model_call.assert_called_once()

    def test_copy_model_auth_modes_support_cpa_variants(self):
        headers = {}
        backend.apply_model_auth_header(headers, {"apiKey": "test-key", "authMode": "x-api-key"})
        self.assertEqual(headers["X-API-Key"], "test-key")

        headers = {}
        backend.apply_model_auth_header(headers, {"apiKey": "Bearer test-key", "authMode": "authorization"})
        self.assertEqual(headers["Authorization"], "Bearer test-key")

    def test_import_csv_merges_by_handle(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                result = backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate,contactMethod,tags\n"
                    "creator_one,Aki,12000,4.2,email,通勤\n"
                )
                self.assertEqual(result["added"], 1)

                result = backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate,contactMethod,tags\n"
                    "creator_one,Aki Updated,15000,4.5,email,通勤\n"
                )
                self.assertEqual(result["updated"], 1)

                rows = backend.load_candidates()
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["followers"], 15000)
                self.assertEqual(rows[0]["name"], "Aki Updated")

    def test_import_preview_flags_updates_and_csv_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate\ncreator_one,Aki,12000,4.2\n"
                )
                preview = backend.preview_import_candidates(
                    "handle,name,followers,engagementRate\n"
                    "creator_one,Aki Updated,15000,4.5\n"
                    "creator_two,Mio,9000,5.1\n"
                    "creator_two,Mio Again,9100,5.2\n"
                )

        self.assertEqual(preview["summary"]["update"], 1)
        self.assertEqual(preview["summary"]["add"], 1)
        self.assertEqual(preview["summary"]["duplicate_csv"], 1)
        self.assertEqual([row["action"] for row in preview["rows"]], ["update", "add", "duplicate_csv"])

    def test_contact_log_sets_followup_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate\ncreator_one,Aki,12000,4.2\n"
                )
                rows = backend.load_candidates(use_samples=False)
                result = backend.log_candidate_contact(
                    rows[0]["id"],
                    note="Sent first DM",
                    follow_up_date="2026-06-26",
                )
                updated = backend.load_candidates(use_samples=False)[0]

        self.assertTrue(result["ok"])
        self.assertEqual(updated["status"], "contacted")
        self.assertEqual(updated["followUpDate"], "2026-06-26")
        self.assertEqual(updated["contactHistory"][0]["note"], "Sent first DM")

    def test_delete_candidate_removes_candidate_from_local_pool(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate\n"
                    "creator_one,Aki,12000,4.2\n"
                    "creator_two,Mio,9000,5.1\n"
                )
                rows = backend.load_candidates(use_samples=False)
                result = backend.delete_candidate(rows[0]["id"])
                remaining = backend.load_candidates(use_samples=False)

        self.assertTrue(result["ok"])
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]["handle"], "creator_two")

    def test_pin_candidate_persists_and_sorts_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate\n"
                    "high_score,Aki,50000,6.0\n"
                    "pinned_creator,Mio,1000,1.0\n"
                )
                rows = backend.load_candidates(use_samples=False)
                pinned_row = next(row for row in rows if row["handle"] == "pinned_creator")
                result = backend.update_candidate_pin(pinned_row["id"], True)
                enriched = backend.enrich_candidates(backend.load_candidates(use_samples=False))

        self.assertTrue(result["ok"])
        self.assertTrue(result["pinned"])
        self.assertEqual(enriched[0]["handle"], "pinned_creator")
        self.assertTrue(enriched[0]["pinned"])

    def test_upsert_preserves_pin_when_payload_omits_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate,pinned\n"
                    "creator_one,Aki,12000,4.2,true\n"
                )
                backend.upsert_candidate({"handle": "creator_one", "name": "Aki Updated", "notes": "profile enriched"})
                updated = backend.load_candidates(use_samples=False)[0]

        self.assertEqual(updated["name"], "Aki Updated")
        self.assertTrue(updated["pinned"])

    def test_delete_all_candidates_clears_local_pool(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate\n"
                    "creator_one,Aki,12000,4.2\n"
                    "creator_two,Mio,9000,5.1\n"
                )
                result = backend.delete_all_candidates("DELETE")
                remaining = backend.load_candidates(use_samples=False)

        self.assertTrue(result["ok"])
        self.assertEqual(result["deleted"], 2)
        self.assertEqual(result["total"], 0)
        self.assertTrue(result["backup"])
        self.assertEqual(remaining, [])

    def test_delete_all_candidates_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,name,followers,engagementRate\n"
                    "creator_one,Aki,12000,4.2\n"
                    "creator_two,Mio,9000,5.1\n"
                )
                result = backend.delete_all_candidates()
                remaining = backend.load_candidates(use_samples=False)

        self.assertFalse(result["ok"])
        self.assertEqual(result["deleted"], 0)
        self.assertEqual(len(remaining), 2)

    def test_partnership_tracking_fields_are_saved_and_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                result = backend.upsert_candidate(
                    {
                        "handle": "creator_roi",
                        "partnershipStage": "已发帖",
                        "invitationSentAt": "2026-06-25",
                        "connectionAt": "2026-06-26",
                        "bloggerId": "creator_roi_001",
                        "creatorType": "fashion_micro",
                        "quoteJpy": "45000",
                        "collabProduct": "summer onepiece",
                        "sampleStatus": "已发货",
                        "sampleCostJpy": "5000",
                        "recipientName": "Aki Sato",
                        "postalCode": "150-0001",
                        "shippingAddress": "Tokyo sample address",
                        "phoneNumber": "+81 90-0000-0000",
                        "orderNumber": "SO-10086",
                        "shippingTracking": "JP123",
                        "shippedAt": "2026-06-28",
                        "receivedAt": "2026-06-30",
                        "postDate": "2026-07-02",
                        "videoProgress": "拍摄中",
                        "postUrl": "https://www.instagram.com/p/example/",
                        "couponCode": "MIKA10",
                        "orders": "12",
                        "revenueJpy": "96000",
                    }
                )
                payload = backend.build_workspace_payload()
                csv_text = backend.export_candidates_csv()

        candidate = result["candidate"]
        stats = payload["stats"]
        self.assertEqual(candidate["partnershipStage"], "posted")
        self.assertEqual(candidate["sampleStatus"], "sent")
        self.assertEqual(candidate["invitationSentAt"], "2026-06-25")
        self.assertEqual(candidate["connectionAt"], "2026-06-26")
        self.assertEqual(candidate["bloggerId"], "creator_roi_001")
        self.assertEqual(candidate["creatorType"], "fashion_micro")
        self.assertEqual(candidate["quoteJpy"], 45000)
        self.assertEqual(candidate["collabProduct"], "summer onepiece")
        self.assertEqual(candidate["recipientName"], "Aki Sato")
        self.assertEqual(candidate["postalCode"], "150-0001")
        self.assertEqual(candidate["shippingAddress"], "Tokyo sample address")
        self.assertEqual(candidate["phoneNumber"], "+81 90-0000-0000")
        self.assertEqual(candidate["orderNumber"], "SO-10086")
        self.assertEqual(candidate["shippedAt"], "2026-06-28")
        self.assertEqual(candidate["receivedAt"], "2026-06-30")
        self.assertEqual(candidate["videoProgress"], "filming")
        self.assertEqual(stats["partnershipOrders"], 12)
        self.assertEqual(stats["partnershipRevenueJpy"], 96000)
        self.assertEqual(stats["partnershipCostJpy"], 50000)
        self.assertIn("bloggerId", csv_text)
        self.assertIn("creator_roi_001", csv_text)
        self.assertIn("orderNumber", csv_text)
        self.assertIn("SO-10086", csv_text)
        self.assertIn("recipientName", csv_text)
        self.assertIn("Aki Sato", csv_text)
        self.assertIn("phoneNumber", csv_text)
        self.assertIn("couponCode", csv_text)
        self.assertIn("MIKA10", csv_text)

    def test_tracking_fields_can_be_imported_with_chinese_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.import_candidates_from_csv(
                    "handle,发送邀约时间,建联时间,博主id,博主类型,主页链接,头像链接,报价,合作产品,收货姓名,邮编,详细地址,手机号,订单编号,发货时间,收货时间,视频进度,粉丝折扣码\n"
                    "creator_cn,2026-06-25,2026-06-26,BID-9,穿搭博主,https://www.instagram.com/creator_cn/,https://cdn.example.com/creator_cn.jpg,30000,连衣裙,山田花子,150-0001,Tokyo,+81 90-9999-9999,ORD-9,2026-06-27,2026-06-29,初稿待审,FAN10\n"
                )
                row = backend.load_candidates(use_samples=False)[0]
                csv_text = backend.export_candidates_csv()

        self.assertEqual(row["invitationSentAt"], "2026-06-25")
        self.assertEqual(row["connectionAt"], "2026-06-26")
        self.assertEqual(row["bloggerId"], "BID-9")
        self.assertEqual(row["creatorType"], "穿搭博主")
        self.assertEqual(row["avatarUrl"], "https://cdn.example.com/creator_cn.jpg")
        self.assertEqual(row["quoteJpy"], 30000)
        self.assertEqual(row["collabProduct"], "连衣裙")
        self.assertEqual(row["recipientName"], "山田花子")
        self.assertEqual(row["postalCode"], "150-0001")
        self.assertEqual(row["shippingAddress"], "Tokyo")
        self.assertEqual(row["phoneNumber"], "+81 90-9999-9999")
        self.assertEqual(row["orderNumber"], "ORD-9")
        self.assertEqual(row["shippedAt"], "2026-06-27")
        self.assertEqual(row["receivedAt"], "2026-06-29")
        self.assertEqual(row["videoProgress"], "draft_review")
        self.assertEqual(row["couponCode"], "FAN10")
        self.assertIn("avatarUrl", csv_text)
        self.assertIn("https://cdn.example.com/creator_cn.jpg", csv_text)

    def test_workspace_payload_includes_score_breakdown_items(self):
        payload = backend.build_workspace_payload()
        first = payload["candidates"][0]

        self.assertIn("scoreBreakdownItems", first)
        self.assertGreater(len(first["scoreBreakdownItems"]), 0)
        self.assertIn("max", first["scoreBreakdownItems"][0])

    def test_extract_instagram_profiles_filters_non_profile_paths(self):
        rows = backend.extract_instagram_profiles(
            "https://www.instagram.com/style_creator/ "
            "https://www.instagram.com/p/ABC123/ "
            "https://instagram.com/reel/XYZ/ "
            "@petite.daily"
        )

        handles = [row["handle"] for row in rows]
        self.assertIn("style_creator", handles)
        self.assertIn("petite.daily", handles)
        self.assertNotIn("p", handles)
        self.assertNotIn("reel", handles)

    def test_discovery_preview_and_import_dedupes_handles(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                text = (
                    "Result A https://www.instagram.com/style_creator/ "
                    "Result B @style_creator "
                    "Result C instagram.com/office_daily_jp/"
                )
                preview = backend.preview_discovery_candidates(text, keyword="通勤コーデ")
                result = backend.import_discovery_candidates(text, keyword="通勤コーデ")
                rows = backend.load_candidates(use_samples=False)

        self.assertEqual(preview["summary"]["add"], 2)
        self.assertEqual(preview["summary"]["duplicate_source"], 1)
        self.assertEqual(result["added"], 2)
        self.assertEqual(result["skipped"], 1)
        self.assertEqual({row["handle"] for row in rows}, {"style_creator", "office_daily_jp"})
        self.assertTrue(all(row["status"] == "review" for row in rows))

    def test_public_search_preview_falls_back_to_manual_search_link_without_keys(self):
        with patch.dict("os.environ", {}, clear=True):
            preview = backend.public_search_preview("tokyo fashion", engine="google_cse", limit=5)

        self.assertTrue(preview["ok"])
        self.assertFalse(preview["configured"])
        self.assertIn('site:instagram.com "tokyo fashion"', preview["query"])
        self.assertIn("google.com/search", preview["searchUrl"])

    def test_public_search_preview_extracts_profiles_from_api_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ), patch.dict(
                "os.environ",
                {"GOOGLE_CSE_API_KEY": "key", "GOOGLE_CSE_CX": "cx"},
                clear=True,
            ), patch.object(
                backend,
                "read_json_url",
                return_value={
                    "items": [
                        {
                            "title": "Tokyo style creator",
                            "link": "https://www.instagram.com/tokyo_style_creator/",
                            "snippet": "fashion blogger japan",
                        }
                    ]
                },
            ):
                preview = backend.public_search_preview("tokyo fashion", engine="google_cse", limit=5)

        self.assertTrue(preview["configured"])
        self.assertEqual(preview["summary"]["add"], 1)
        self.assertEqual(preview["rows"][0]["candidate"]["handle"], "tokyo_style_creator")

    def test_website_preview_extracts_creator_profile_from_public_page(self):
        html = """
        <html>
          <head>
            <title>胡蝶蘭aki PR profile</title>
            <meta name="description" content="美容・健康・ライフスタイル。平均ER 10%。">
            <meta property="og:image" content="/assets/ayako.jpg">
          </head>
          <body>
            Instagram https://www.instagram.com/ayako38aksa/reels/
            フォロワー 1.9万人 企業PR・アンバサダー実績あり リール対応
            contact@example.com
          </body>
        </html>
        """
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ), patch.object(backend, "ensure_public_fetch_url", return_value=None), patch.object(
                backend, "read_public_html", return_value=html
            ):
                preview = backend.preview_website_candidates("https://creator.example/profile")
                result = backend.import_website_candidates("https://creator.example/profile")
                rows = backend.load_candidates(use_samples=False)

        candidate = preview["rows"][0]["candidate"]
        self.assertEqual(preview["summary"]["add"], 1)
        self.assertEqual(candidate["handle"], "ayako38aksa")
        self.assertEqual(candidate["followers"], 19000)
        self.assertEqual(candidate["engagementRate"], 10)
        self.assertEqual(candidate["email"], "contact@example.com")
        self.assertEqual(candidate["avatarUrl"], "https://creator.example/assets/ayako.jpg")
        self.assertEqual(result["added"], 1)
        self.assertEqual(rows[0]["handle"], "ayako38aksa")

    def test_website_preview_reads_profile_links_from_html_attributes(self):
        html = """
        <html>
          <head><title>Creator media kit</title></head>
          <body>
            <a href="https://www.instagram.com/link_only_creator/">Instagram</a>
            <a href="mailto:hello@example.com">Contact</a>
            followers 24.5k ER 4.8%
          </body>
        </html>
        """
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ), patch.object(backend, "ensure_public_fetch_url", return_value=None), patch.object(
                backend, "read_public_html", return_value=html
            ):
                preview = backend.preview_website_candidates("https://creator.example/profile")

        candidate = preview["rows"][0]["candidate"]
        self.assertEqual(preview["summary"]["add"], 1)
        self.assertEqual(candidate["handle"], "link_only_creator")
        self.assertEqual(candidate["email"], "hello@example.com")
        self.assertEqual(candidate["followers"], 24500)
        self.assertEqual(candidate["engagementRate"], 4.8)

    def test_website_preview_does_not_fetch_instagram_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                preview = backend.preview_website_candidates("https://www.instagram.com/ayako38aksa/reels/")

        self.assertEqual(preview["summary"]["add"], 1)
        self.assertEqual(preview["rows"][0]["candidate"]["handle"], "ayako38aksa")
        self.assertIn("Instagram 页面未自动抓取", preview["rows"][0]["candidate"]["notes"])

    def test_instagram_graph_setup_state_reads_env_without_exposing_token(self):
        with patch.dict(
            "os.environ",
            {
                "META_ACCESS_TOKEN": "secret-token",
                "META_IG_USER_ID": "17841400000000000",
                "META_GRAPH_API_VERSION": "v25.0",
            },
            clear=True,
        ):
            setup = backend.instagram_graph_setup_state()

        self.assertTrue(setup["configured"])
        self.assertTrue(setup["accessToken"])
        self.assertTrue(setup["ownUserId"])
        self.assertNotIn("secret-token", str(setup))

    def test_instagram_login_token_is_auto_detected(self):
        with patch.dict(
            "os.environ",
            {
                "META_ACCESS_TOKEN": "IGAA-test-token",
                "META_GRAPH_API_VERSION": "v25.0",
            },
            clear=True,
        ):
            config = backend.resolve_instagram_graph_config()
            setup = backend.instagram_graph_setup_state()

        self.assertEqual(config["mode"], "instagram_login")
        self.assertEqual(config["baseUrl"], "https://graph.instagram.com")
        self.assertTrue(setup["configured"])
        self.assertFalse(setup["businessDiscovery"])

    def test_instagram_login_enrichment_rejects_other_handles_with_clear_error(self):
        with patch.dict(
            "os.environ",
            {
                "META_ACCESS_TOKEN": "IGAA-test-token",
                "META_GRAPH_API_VERSION": "v25.0",
            },
            clear=True,
        ), patch.object(
            backend,
            "read_meta_graph_url",
            return_value={
                "id": "178000",
                "username": "own_shop",
                "account_type": "BUSINESS",
                "followers_count": 22,
            },
        ) as graph_call:
            result = backend.fetch_instagram_graph_profile("creator_one")

        self.assertFalse(result["ok"])
        self.assertIn("只能补全授权账号 @own_shop", result["error"])
        graph_call.assert_called_once()
        self.assertEqual(graph_call.call_args.args[1], "me")

    def test_instagram_login_enrichment_updates_authorized_account(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ), patch.dict(
                "os.environ",
                {
                    "META_ACCESS_TOKEN": "IGAA-test-token",
                    "META_GRAPH_API_VERSION": "v25.0",
                },
                clear=True,
            ), patch.object(
                backend,
                "read_meta_graph_url",
                return_value={
                    "id": "178000",
                    "username": "own_shop",
                    "name": "Own Shop",
                    "biography": "Tokyo fashion #ootdjapan",
                    "followers_count": 22,
                    "media_count": 3,
                    "profile_picture_url": "https://cdn.example.com/own.jpg",
                    "website": "https://example.com",
                },
            ):
                backend.import_candidates_from_csv("handle,name,followers\nown_shop,own_shop,0\n")
                result = backend.enrich_candidate_from_instagram_api({"handle": "own_shop"})
                row = backend.load_candidates(use_samples=False)[0]

        self.assertTrue(result["ok"])
        self.assertEqual(row["name"], "Own Shop")
        self.assertEqual(row["followers"], 22)
        self.assertEqual(row["avatarUrl"], "https://cdn.example.com/own.jpg")

    def test_instagram_api_enrichment_updates_candidate_from_business_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ), patch.dict(
                "os.environ",
                {
                    "META_ACCESS_TOKEN": "secret-token",
                    "META_IG_USER_ID": "17841400000000000",
                    "META_GRAPH_API_VERSION": "v25.0",
                },
                clear=True,
            ), patch.object(
                backend,
                "read_meta_graph_url",
                return_value={
                    "business_discovery": {
                        "username": "creator_one",
                        "name": "Aki Creator",
                        "biography": "Tokyo fashion creator hello@example.com #ootdjapan",
                        "followers_count": 32100,
                        "media_count": 88,
                        "profile_picture_url": "https://cdn.example.com/avatar.jpg",
                        "website": "https://creator.example",
                    }
                },
            ) as graph_call:
                backend.import_candidates_from_csv("handle,name,followers,notes\ncreator_one,creator_one,0,old note\n")
                result = backend.enrich_candidate_from_instagram_api({"handle": "creator_one"})
                row = backend.load_candidates(use_samples=False)[0]

        self.assertTrue(result["ok"])
        self.assertFalse(result["created"])
        self.assertEqual(row["name"], "Aki Creator")
        self.assertEqual(row["followers"], 32100)
        self.assertEqual(row["avatarUrl"], "https://cdn.example.com/avatar.jpg")
        self.assertEqual(row["email"], "hello@example.com")
        self.assertIn("old note", row["notes"])
        self.assertIn("Instagram Graph API", row["notes"])
        graph_call.assert_called_once()
        args = graph_call.call_args.args
        self.assertEqual(args[1], "17841400000000000")
        self.assertIn("business_discovery.username(creator_one)", args[2]["fields"])

    def test_skill_harvest_options_normalize_panel_payload(self):
        options = backend.skill_harvest_options(
            {
                "sourceMode": "unknown",
                "market": "",
                "language": "",
                "niche": "",
                "minFollowers": "1万",
                "maxFollowers": "8万",
                "perTermLimit": "999",
                "rawTarget": "120",
                "topTarget": "200",
                "seedTerms": "#40代ファッション, #40代ファッション\n#大人カジュアル",
                "exclusionRules": "店员/スタッフ\n男性达人\n品牌店铺号",
                "fullAngle": False,
            }
        )

        self.assertEqual(options["sourceMode"], "instagram")
        self.assertEqual(options["market"], "Japan")
        self.assertEqual(options["minFollowers"], 10000)
        self.assertEqual(options["maxFollowers"], 80000)
        self.assertEqual(options["perTermLimit"], 200)
        self.assertEqual(options["rawTarget"], 120)
        self.assertEqual(options["topTarget"], 120)
        self.assertEqual(options["seedTerms"], ["#40代ファッション", "#大人カジュアル"])
        self.assertEqual(options["exclusionRules"], ["店员/スタッフ", "男性达人", "品牌店铺号"])
        self.assertFalse(options["fullAngle"])

    def test_skill_harvest_prompt_contains_guardrails_and_seeds(self):
        result = backend.build_skill_harvest_prompt(
            {
                "sourceMode": "hybrid",
                "seedTerms": "#40代ファッション\n#きれいめカジュアル",
                "topTarget": 20,
                "rawTarget": 60,
                "strictFilter": True,
                "exclusionRules": "店员/スタッフ\n男性达人\n美容院/服务号",
            }
        )

        self.assertTrue(result["ok"])
        self.assertIn("$instagram-dm-outreach", result["prompt"])
        self.assertIn("Google/public search", result["prompt"])
        self.assertIn("#40代ファッション", result["prompt"])
        self.assertIn("strict female creator filter", result["prompt"])
        self.assertIn("采集阶段先跳过", result["prompt"])
        self.assertIn("店员/スタッフ", result["prompt"])
        self.assertIn("男性达人", result["prompt"])
        self.assertIn("不私信", result["prompt"])
        self.assertEqual(result["options"]["topTarget"], 20)

    def test_skill_harvest_runs_summarize_progress_and_raw_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            run_id = "2026-07-08_panel_test"
            (output_dir / f"instagram_harvest_progress_{run_id}.csv").write_text(
                "source_term,status,updated_at\n#40代ファッション,done,2026-07-08T10:00:00\n#大人カジュアル,pending,\n",
                encoding="utf-8",
            )
            (output_dir / f"raw_instagram_harvest_{run_id}_working.csv").write_text(
                "handle,profile_url\ncreator_one,https://www.instagram.com/creator_one/\ncreator_one,\ncreator_two,\n",
                encoding="utf-8",
            )
            with patch.object(backend, "SKILL_HARVEST_OUTPUT_DIR", output_dir):
                runs = backend.list_skill_harvest_runs()

        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["runId"], run_id)
        self.assertEqual(runs[0]["progressRows"], 2)
        self.assertEqual(runs[0]["rawRows"], 3)
        self.assertEqual(runs[0]["uniqueHandles"], 2)
        self.assertEqual(runs[0]["statusCounts"]["done"], 1)
        self.assertEqual(runs[0]["statusCounts"]["pending"], 1)

    def test_delete_skill_harvest_run_removes_only_run_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            run_id = "2026-07-08_panel_delete"
            run_files = [
                output_dir / f"instagram_discovery_plan_{run_id}.csv",
                output_dir / f"instagram_harvest_progress_{run_id}.csv",
                output_dir / f"raw_instagram_harvest_{run_id}_working.csv",
                output_dir / f"raw_instagram_harvest_{run_id}_deduped.csv",
            ]
            for path in run_files:
                path.write_text("x\n", encoding="utf-8")
            seen_path = output_dir / "seen_creators.csv"
            seen_path.write_text("handle\ncreator_one\n", encoding="utf-8")

            with patch.object(backend, "SKILL_HARVEST_OUTPUT_DIR", output_dir):
                result = backend.delete_skill_harvest_run(run_id)

            self.assertTrue(result["ok"])
            self.assertEqual(len(result["deleted"]), 4)
            self.assertTrue(seen_path.exists())
            self.assertTrue(all(not path.exists() for path in run_files))

    def test_delete_skill_harvest_run_rejects_invalid_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            with patch.object(backend, "SKILL_HARVEST_OUTPUT_DIR", output_dir):
                result = backend.delete_skill_harvest_run("../seen_creators")

        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "invalid runId")

    def test_workspace_payload_contains_discovery_and_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                payload = backend.build_workspace_payload()

        self.assertTrue(payload["ok"])
        self.assertGreater(len(payload["discovery"]["hashtags"]), 0)
        self.assertGreater(len(payload["skillPanel"]["defaultExclusions"]), 0)
        self.assertTrue(payload["skillPanel"]["defaultExclusions"][0].startswith("#"))
        self.assertIn("#ショップスタッフ除外", payload["skillPanel"]["defaultExclusions"])
        self.assertGreater(len(payload["candidates"]), 0)
        self.assertIn("dm", payload["candidates"][0]["drafts"])


if __name__ == "__main__":
    unittest.main()
