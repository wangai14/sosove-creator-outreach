from __future__ import annotations

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from tiktok_creator_outreach import backend as tiktok_backend
from instagram_creator_outreach.backend import (
    STATIC_DIR,
    build_skill_harvest_prompt,
    build_workspace_payload,
    create_skill_harvest_plan,
    delete_all_candidates,
    delete_candidate,
    delete_skill_harvest_run,
    enrich_candidate_from_instagram_api,
    export_candidates_csv,
    generate_copy_draft,
    generate_reply_draft,
    import_discovery_candidates,
    import_candidates_from_csv,
    import_website_candidates,
    log_candidate_contact,
    now_iso,
    preview_discovery_candidates,
    preview_import_candidates,
    preview_website_candidates,
    public_search_preview,
    test_copy_model_config,
    update_candidate_followup,
    update_candidate_pin,
    update_candidate_status,
    upsert_candidate,
)


class InstagramOutreachHandler(BaseHTTPRequestHandler):
    server_version = "InstagramCreatorOutreach/0.1"

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_common_headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path in {"/tiktok", "/tiktok/", "/tiktok/index.html"}:
            self.serve_static_from(tiktok_backend.STATIC_DIR, "index.html")
            return
        if path.startswith("/tiktok/static/"):
            self.serve_static_from(tiktok_backend.STATIC_DIR, path.removeprefix("/tiktok/static/"))
            return
        if path == "/tiktok/api/health":
            self.send_json({"ok": True, "service": "tiktok-creator-outreach", "time": tiktok_backend.now_iso()})
            return
        if path == "/tiktok/api/workspace":
            self.send_json(tiktok_backend.build_workspace_payload())
            return
        if path == "/tiktok/api/candidates.csv":
            self.send_text(
                tiktok_backend.export_candidates_csv(),
                content_type="text/csv; charset=utf-8",
                filename="tiktok_creator_candidates.csv",
            )
            return
        if path in {"/", "/index.html"}:
            self.serve_static("index.html")
            return
        if path.startswith("/static/"):
            self.serve_static(path.removeprefix("/static/"))
            return
        if path == "/api/health":
            self.send_json({"ok": True, "service": "instagram-creator-outreach", "time": now_iso()})
            return
        if path == "/api/workspace":
            self.send_json(build_workspace_payload())
            return
        if path == "/api/candidates.csv":
            self.send_text(
                export_candidates_csv(),
                content_type="text/csv; charset=utf-8",
                filename="instagram_creator_candidates.csv",
            )
            return
        self.send_error_json(HTTPStatus.NOT_FOUND, "route not found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        payload = self.read_json_body()
        if self.handle_tiktok_post(parsed.path, payload):
            return
        if parsed.path == "/api/import":
            csv_text = str(payload.get("csvText", "")) if isinstance(payload, dict) else ""
            if not csv_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing csvText")
                return
            self.send_json(import_candidates_from_csv(csv_text))
            return
        if parsed.path == "/api/import/preview":
            csv_text = str(payload.get("csvText", "")) if isinstance(payload, dict) else ""
            if not csv_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing csvText")
                return
            self.send_json(preview_import_candidates(csv_text))
            return
        if parsed.path == "/api/discovery/preview":
            source_text = str(payload.get("sourceText", "")) if isinstance(payload, dict) else ""
            if not source_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing sourceText")
                return
            self.send_json(
                preview_discovery_candidates(
                    source_text,
                    keyword=str(payload.get("keyword", "")),
                    source_label=str(payload.get("sourceLabel", "pasted_results")),
                )
            )
            return
        if parsed.path == "/api/discovery/import":
            source_text = str(payload.get("sourceText", "")) if isinstance(payload, dict) else ""
            if not source_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing sourceText")
                return
            self.send_json(
                import_discovery_candidates(
                    source_text,
                    keyword=str(payload.get("keyword", "")),
                    source_label=str(payload.get("sourceLabel", "pasted_results")),
                )
            )
            return
        if parsed.path == "/api/website/preview":
            source_text = str(payload.get("sourceText", "")) if isinstance(payload, dict) else ""
            if not source_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing sourceText")
                return
            self.send_json(
                preview_website_candidates(
                    source_text,
                    keyword=str(payload.get("keyword", "")),
                )
            )
            return
        if parsed.path == "/api/website/import":
            source_text = str(payload.get("sourceText", "")) if isinstance(payload, dict) else ""
            if not source_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing sourceText")
                return
            self.send_json(
                import_website_candidates(
                    source_text,
                    keyword=str(payload.get("keyword", "")),
                )
            )
            return
        if parsed.path == "/api/public-search/preview":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            keyword = str(payload.get("keyword", ""))
            if not keyword.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing keyword")
                return
            try:
                limit = int(payload.get("limit", 10) or 10)
            except (TypeError, ValueError):
                limit = 10
            self.send_json(
                public_search_preview(
                    keyword=keyword,
                    engine=str(payload.get("engine", "auto")),
                    limit=limit,
                )
            )
            return
        if parsed.path == "/api/skill/prompt":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(build_skill_harvest_prompt(payload))
            return
        if parsed.path == "/api/skill/plan":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            result = create_skill_harvest_plan(payload)
            if not result.get("ok"):
                self.send_json(result, HTTPStatus.BAD_REQUEST)
                return
            self.send_json(result)
            return
        if parsed.path == "/api/skill/run/delete":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            result = delete_skill_harvest_run(str(payload.get("runId", "")))
            if not result.get("ok"):
                self.send_json(result, HTTPStatus.BAD_REQUEST)
                return
            self.send_json(result)
            return
        if parsed.path == "/api/copy/generate":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(generate_copy_draft(payload))
            return
        if parsed.path == "/api/copy/test":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(test_copy_model_config(payload))
            return
        if parsed.path == "/api/reply/generate":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(generate_reply_draft(payload))
            return
        if parsed.path == "/api/candidates":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(upsert_candidate(payload))
            return
        if parsed.path == "/api/candidates/status":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(update_candidate_status(str(payload.get("id", "")), str(payload.get("status", ""))))
            return
        if parsed.path == "/api/candidates/pin":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(update_candidate_pin(str(payload.get("id", "")), payload.get("pinned", False)))
            return
        if parsed.path == "/api/candidates/log":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(
                log_candidate_contact(
                    str(payload.get("id", "")),
                    note=str(payload.get("note", "")),
                    contact_type=str(payload.get("type", "contacted")),
                    follow_up_date=str(payload.get("followUpDate", "")),
                )
            )
            return
        if parsed.path == "/api/candidates/followup":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(
                update_candidate_followup(
                    str(payload.get("id", "")),
                    str(payload.get("followUpDate", "")),
                )
            )
            return
        if parsed.path == "/api/candidates/delete":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(delete_candidate(str(payload.get("id", ""))))
            return
        if parsed.path == "/api/candidates/delete-all":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(delete_all_candidates(str(payload.get("confirm", ""))))
            return
        if parsed.path == "/api/instagram/enrich":
            if not isinstance(payload, dict):
                self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
                return
            self.send_json(enrich_candidate_from_instagram_api(payload))
            return
        self.send_error_json(HTTPStatus.NOT_FOUND, "route not found")

    def handle_tiktok_post(self, path: str, payload: object) -> bool:
        if not path.startswith("/tiktok/api/"):
            return False
        if not isinstance(payload, dict):
            self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid payload")
            return True
        if path == "/tiktok/api/import":
            csv_text = str(payload.get("csvText", ""))
            if not csv_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing csvText")
            else:
                self.send_json(tiktok_backend.import_candidates_from_csv(csv_text))
            return True
        if path == "/tiktok/api/import/preview":
            csv_text = str(payload.get("csvText", ""))
            if not csv_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing csvText")
            else:
                self.send_json(tiktok_backend.preview_import_candidates(csv_text))
            return True
        if path == "/tiktok/api/discovery/import":
            source_text = str(payload.get("sourceText", ""))
            if not source_text.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing sourceText")
            else:
                self.send_json(
                    tiktok_backend.import_profiles_from_text(
                        source_text,
                        niche=str(payload.get("niche", "")),
                    )
                )
            return True
        if path == "/tiktok/api/public-search/preview":
            keyword = str(payload.get("keyword", ""))
            if not keyword.strip():
                self.send_error_json(HTTPStatus.BAD_REQUEST, "missing keyword")
            else:
                try:
                    limit = int(payload.get("limit", 10) or 10)
                except (TypeError, ValueError):
                    limit = 10
                self.send_json(
                    tiktok_backend.public_search_preview(
                        keyword=keyword,
                        engine=str(payload.get("engine", "auto")),
                        limit=max(1, min(limit, 30)),
                    )
                )
            return True
        if path == "/tiktok/api/candidates":
            self.send_json(tiktok_backend.upsert_candidate(payload))
            return True
        if path == "/tiktok/api/candidates/status":
            self.send_json(
                tiktok_backend.update_candidate_status(
                    str(payload.get("id", "")),
                    str(payload.get("status", "")),
                )
            )
            return True
        if path == "/tiktok/api/candidates/pin":
            self.send_json(
                tiktok_backend.update_candidate_pin(
                    str(payload.get("id", "")),
                    payload.get("pinned", False),
                )
            )
            return True
        if path == "/tiktok/api/candidates/contact":
            self.send_json(
                tiktok_backend.mark_candidate_contacted(
                    str(payload.get("id", "")),
                    note=str(payload.get("note", "")),
                )
            )
            return True
        if path == "/tiktok/api/candidates/followup":
            self.send_json(
                tiktok_backend.update_candidate_followup(
                    str(payload.get("id", "")),
                    str(payload.get("followUpDate", "")),
                )
            )
            return True
        if path == "/tiktok/api/candidates/batch":
            self.send_json(
                tiktok_backend.batch_update_candidates(
                    payload.get("ids", []),
                    str(payload.get("action", "")),
                    payload.get("value", ""),
                    str(payload.get("confirm", "")),
                )
            )
            return True
        if path == "/tiktok/api/copy/generate":
            self.send_json(tiktok_backend.generate_copy_draft(payload))
            return True
        if path == "/tiktok/api/copy/test":
            self.send_json(tiktok_backend.test_copy_model_config(payload))
            return True
        if path == "/tiktok/api/reply/generate":
            self.send_json(tiktok_backend.generate_reply_draft(payload))
            return True
        if path == "/tiktok/api/candidates/delete":
            self.send_json(tiktok_backend.delete_candidate(str(payload.get("id", ""))))
            return True
        if path == "/tiktok/api/candidates/delete-all":
            self.send_json(tiktok_backend.delete_all_candidates(str(payload.get("confirm", ""))))
            return True
        self.send_error_json(HTTPStatus.NOT_FOUND, "route not found")
        return True

    def serve_static(self, relative_path: str) -> None:
        self.serve_static_from(STATIC_DIR, relative_path)

    def serve_static_from(self, static_dir, relative_path: str) -> None:
        target = (static_dir / relative_path).resolve()
        try:
            target.relative_to(static_dir.resolve())
        except ValueError:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid static path")
            return
        if not target.exists() or not target.is_file():
            self.send_error_json(HTTPStatus.NOT_FOUND, "file not found")
            return

        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        content = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_common_headers(content_type=content_type, cache=False)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_common_headers(content_type="application/json; charset=utf-8", cache=False)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_text(
        self,
        text: str,
        content_type: str = "text/plain; charset=utf-8",
        filename: str = "",
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        content = text.encode("utf-8-sig")
        self.send_response(status)
        self.send_common_headers(content_type=content_type, cache=False)
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_error_json(self, status: HTTPStatus, message: str) -> None:
        self.send_json({"ok": False, "error": message}, status=status)

    def send_common_headers(
        self,
        content_type: str = "text/plain; charset=utf-8",
        cache: bool = False,
    ) -> None:
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if not cache:
            self.send_header("Cache-Control", "no-store")

    def read_json_body(self) -> object:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        body = self.rfile.read(length)
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}

    def log_message(self, format: str, *args: object) -> None:
        print(f"[instagram-creator-outreach] {self.address_string()} - {format % args}")


def run(host: str, port: int) -> None:
    ThreadingHTTPServer.allow_reuse_address = True
    server = ThreadingHTTPServer((host, port), InstagramOutreachHandler)
    print(f"Instagram Creator Outreach running at http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Instagram creator outreach workspace.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8792)
    args = parser.parse_args()
    run(args.host, args.port)


if __name__ == "__main__":
    main()
