import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tiktok_creator_outreach import backend


class TikTokCreatorOutreachBackendTests(unittest.TestCase):
    def test_normalizes_tiktok_profile_url(self):
        row = backend.normalize_candidate({"tiktokUrl": "https://www.tiktok.com/@creator.jp/video/123"})
        self.assertEqual(row["handle"], "creator.jp")
        self.assertEqual(row["tiktokUrl"], "https://www.tiktok.com/@creator.jp/video/123")

    def test_import_isolated_candidate_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                result = backend.import_candidates_from_csv(
                    "handle,name,followers,avgViews,engagementRate\ncreator_one,Aki,12000,30000,5.2\n"
                )
                rows = backend.load_candidates()

        self.assertEqual(result["added"], 1)
        self.assertEqual(rows[0]["handle"], "creator_one")
        self.assertEqual(rows[0]["avgViews"], 30000)

    def test_profile_text_import_deduplicates_handles(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                result = backend.import_profiles_from_text(
                    "https://www.tiktok.com/@creator_one @creator_one https://www.tiktok.com/@creator_two"
                )
                rows = backend.load_candidates()

        self.assertEqual(result["added"], 2)
        self.assertEqual({row["handle"] for row in rows}, {"creator_one", "creator_two"})

    def test_workspace_contains_tiktok_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.upsert_candidate({"handle": "creator_one", "name": "Aki", "niche": "fashion"})
                payload = backend.build_workspace_payload()

        self.assertEqual(payload["platform"], "tiktok")
        self.assertIn("TikTok", payload["candidates"][0]["drafts"]["dm"])

    def test_delete_all_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.upsert_candidate({"handle": "creator_one"})
                denied = backend.delete_all_candidates()
                deleted = backend.delete_all_candidates("DELETE")

        self.assertFalse(denied["ok"])
        self.assertTrue(deleted["ok"])
        self.assertEqual(deleted["deleted"], 1)

    def test_tiktok_score_prioritizes_views_ratio_and_engagement(self):
        strong = backend.normalize_candidate(
            {
                "handle": "strong_creator",
                "followers": 12000,
                "avgViews": 36000,
                "medianViews": 28000,
                "engagementRate": 7.2,
                "videoFrequency": 4,
                "email": "hello@example.com",
            }
        )
        weak = backend.normalize_candidate(
            {
                "handle": "large_but_weak",
                "followers": 180000,
                "avgViews": 5000,
                "engagementRate": 1.2,
                "videoFrequency": 0.5,
            }
        )

        strong_score, breakdown = backend.score_candidate(strong)
        weak_score, _ = backend.score_candidate(weak)

        self.assertGreater(strong_score, weak_score)
        self.assertEqual(breakdown["views"], 18)
        self.assertEqual(breakdown["ratio"], 18)

    def test_partnership_and_spark_fields_are_saved_and_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                result = backend.upsert_candidate(
                    {
                        "handle": "spark_creator",
                        "partnershipStage": "draft_review",
                        "quoteJpy": 45000,
                        "videoFormat": "short_video",
                        "videoProgress": "script_review",
                        "sparkAdsStatus": "approved",
                        "sparkAuthorizationCode": "SPARK-123",
                        "usageRightsDays": 30,
                    }
                )
                csv_text = backend.export_candidates_csv()

        row = result["candidate"]
        self.assertEqual(row["partnershipStage"], "draft_review")
        self.assertEqual(row["sparkAdsStatus"], "approved")
        self.assertEqual(row["usageRightsDays"], 30)
        self.assertIn("sparkAuthorizationCode", csv_text)
        self.assertIn("SPARK-123", csv_text)

    def test_saved_works_are_normalized_deduplicated_and_exported(self):
        saved_works = json.dumps(
            [
                {"url": "https://www.tiktok.com/@creator/video/101", "title": "Look 1", "note": "Good pacing"},
                {"url": "https://www.tiktok.com/@creator/video/101", "title": "Duplicate"},
                {"url": "https://www.tiktok.com/@creator/video/202", "title": "Look 2"},
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                result = backend.upsert_candidate({"handle": "work_creator", "savedWorks": saved_works})
                persisted = backend.load_candidates()[0]
                exported = next(csv.DictReader(io.StringIO(backend.export_candidates_csv())))

        self.assertEqual(len(result["candidate"]["savedWorks"]), 2)
        self.assertEqual(len(persisted["savedWorks"]), 2)
        self.assertEqual(persisted["savedWorks"][0]["title"], "Look 1")
        self.assertEqual(len(json.loads(exported["savedWorks"])), 2)

    def test_featured_work_personalizes_local_draft_and_model_prompt(self):
        row = backend.normalize_candidate(
            {
                "handle": "reference_creator",
                "savedWorks": [{"id": "work-1", "url": "https://www.tiktok.com/@reference_creator/video/101", "title": "春夏コーデ"}],
                "featuredWorkId": "work-1",
            }
        )

        self.assertIn("春夏コーデ", backend.build_drafts(row)["dm"])
        self.assertIn("春夏コーデ", backend.build_drafts(row)["email"])
        prompt = backend.build_copy_prompt(row, {})
        self.assertIn("referenceWork", prompt[1]["content"])

    def test_batch_update_and_delete_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                first = backend.upsert_candidate({"handle": "batch_one"})["candidate"]
                second = backend.upsert_candidate({"handle": "batch_two"})["candidate"]
                backend.batch_update_candidates([first["id"], second["id"]], "status", "ready")
                backend.batch_update_candidates([first["id"]], "tags", "priority, fashion")
                backend.batch_update_candidates([first["id"]], "followup", "2026-07-20")
                denied = backend.batch_update_candidates([second["id"]], "delete")
                deleted = backend.batch_update_candidates([second["id"]], "delete", confirm="DELETE_SELECTED")
                rows = backend.load_candidates()

        self.assertFalse(denied["ok"])
        self.assertTrue(deleted["ok"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "ready")
        self.assertEqual(rows[0]["tags"], ["priority", "fashion"])
        self.assertEqual(rows[0]["followUpDate"], "2026-07-20")

    def test_task_board_tracks_missing_metrics_and_draft_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            with patch.object(backend, "DATA_DIR", data_dir), patch.object(
                backend, "CANDIDATES_PATH", data_dir / "candidates.json"
            ):
                backend.upsert_candidate(
                    {
                        "handle": "task_creator",
                        "avgViews": 0,
                        "engagementRate": 0,
                        "videoProgress": "draft_review",
                    }
                )
                payload = backend.build_workspace_payload()

        candidate_id = payload["candidates"][0]["id"]
        self.assertIn(candidate_id, payload["tasks"]["missingMetrics"])
        self.assertIn(candidate_id, payload["tasks"]["draftReview"])

    def test_local_copy_mentions_tiktok_and_spark_terms(self):
        result = backend.generate_copy_draft(
            {
                "provider": "local",
                "candidate": {"handle": "creator_one", "name": "Aki", "niche": "fashion"},
            }
        )

        self.assertTrue(result["ok"])
        self.assertIn("TikTok", result["text"])
        self.assertIn("Spark Ads", result["text"])


if __name__ == "__main__":
    unittest.main()
