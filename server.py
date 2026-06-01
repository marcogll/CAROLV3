#!/usr/bin/env python3
"""
CAROL Server — Dual mode: MySQL (Docker/production) or JSON (local dev)
Serves API/webhook endpoints. Static files handled by Caddy upstream in Docker.
"""
import os, json, csv, io, uuid, urllib.parse, time
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ── Config ───────────────────────────────────────────────────────────────────
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "carol")
DB_USER = os.getenv("DB_USER", "carol")
DB_PASSWORD = os.getenv("DB_PASSWORD", "carolpass")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DATA_DIR = os.path.join(BASE_DIR, ".carol_data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
RESULTS_FILE = os.path.join(DATA_DIR, "results.json")

os.makedirs(DATA_DIR, exist_ok=True)

# ── Storage backend detection ────────────────────────────────────────────────
USE_MYSQL = False
MYSQL = None
DictCursor = None

if DB_HOST:
    try:
        import pymysql
        from pymysql.cursors import DictCursor as _DictCursor
        MYSQL = pymysql
        DictCursor = _DictCursor
        # Test connection
        c = pymysql.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
            charset="utf8mb4", cursorclass=_DictCursor, autocommit=True,
        )
        c.close()
        USE_MYSQL = True
        print(f"[DB] MySQL mode enabled ({DB_HOST}:{DB_PORT})")
    except Exception as e:
        print(f"[DB] MySQL not available ({e}), falling back to JSON files.")
else:
    print("[DB] DB_HOST not set, using JSON file storage.")

# ── JSON helpers (fallback) ──────────────────────────────────────────────────
def _load(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _now_iso():
    return datetime.now().isoformat()

# ── MySQL helpers ────────────────────────────────────────────────────────────
def get_conn():
    if not USE_MYSQL:
        return None
    return MYSQL.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, charset="utf8mb4", cursorclass=DictCursor, autocommit=True,
    )

def init_db():
    if not USE_MYSQL:
        return
    for attempt in range(12):
        try:
            conn = MYSQL.connect(
                host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
                charset="utf8mb4", cursorclass=DictCursor, autocommit=True,
            )
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.close()

            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS candidates (
                        id VARCHAR(36) PRIMARY KEY,
                        candidate_id VARCHAR(36) UNIQUE,
                        survey_id VARCHAR(100),
                        full_name VARCHAR(255),
                        employee_id VARCHAR(100),
                        birth_year INT,
                        birth_month INT,
                        department VARCHAR(100),
                        job_role VARCHAR(100),
                        years_experience INT,
                        self_evaluation INT,
                        company_name VARCHAR(255),
                        contact_email VARCHAR(255),
                        assigned_level VARCHAR(50),
                        status VARCHAR(50) DEFAULT 'registered',
                        registered_at DATETIME,
                        submitted_at DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS results (
                        id VARCHAR(36) PRIMARY KEY,
                        candidate_id VARCHAR(36),
                        submitted_at DATETIME,
                        candidate_json JSON,
                        assessment_json JSON,
                        results_json JSON,
                        category_breakdown_json JSON,
                        wrong_question_ids_json JSON,
                        stored_at DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_candidate_id (candidate_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
            conn.close()
            print("[DB] Tables initialized successfully.")
            return
        except Exception as e:
            print(f"[DB] Waiting for MySQL... ({attempt+1}/12): {e}")
            time.sleep(3)
    raise RuntimeError("Could not connect to MySQL after 12 attempts.")

# ── Unified storage helpers ──────────────────────────────────────────────────
def store_candidate(candidate):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            sql = """
                INSERT INTO candidates
                (id, candidate_id, survey_id, full_name, employee_id, birth_year, birth_month,
                 department, job_role, years_experience, self_evaluation, company_name, contact_email,
                 assigned_level, status, registered_at, submitted_at)
                VALUES
                (%(id)s, %(candidate_id)s, %(survey_id)s, %(full_name)s, %(employee_id)s, %(birth_year)s, %(birth_month)s,
                 %(department)s, %(job_role)s, %(years_experience)s, %(self_evaluation)s, %(company_name)s, %(contact_email)s,
                 %(assigned_level)s, %(status)s, %(registered_at)s, %(submitted_at)s)
            """
            cur.execute(sql, candidate)
        conn.close()
    else:
        candidates = _load(CANDIDATES_FILE)
        candidates.append(candidate)
        _save(CANDIDATES_FILE, candidates)

def store_result(result):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO results
                (id, candidate_id, submitted_at, candidate_json, assessment_json, results_json,
                 category_breakdown_json, wrong_question_ids_json, stored_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                result["id"],
                result.get("candidate", {}).get("candidate_id", ""),
                result.get("submitted_at", _now_iso()),
                json.dumps(result.get("candidate", {}), ensure_ascii=False),
                json.dumps(result.get("assessment", {}), ensure_ascii=False),
                json.dumps(result.get("results", {}), ensure_ascii=False),
                json.dumps(result.get("category_breakdown", {}), ensure_ascii=False),
                json.dumps(result.get("wrong_question_ids", []), ensure_ascii=False),
                _now_iso(),
            ))
        conn.close()
    else:
        results = _load(RESULTS_FILE)
        results.append(result)
        _save(RESULTS_FILE, results)

def get_candidates():
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM candidates ORDER BY created_at DESC")
            rows = cur.fetchall()
        conn.close()
        return rows
    return _load(CANDIDATES_FILE)

def get_results():
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM results ORDER BY created_at DESC")
            rows = cur.fetchall()
        conn.close()
        # Flatten JSON columns for frontend compatibility
        for r in rows:
            r["candidate"] = json.loads(r.get("candidate_json") or "{}")
            r["assessment"] = json.loads(r.get("assessment_json") or "{}")
            r["results"] = json.loads(r.get("results_json") or "{}")
            r["category_breakdown"] = json.loads(r.get("category_breakdown_json") or "{}")
            r["wrong_question_ids"] = json.loads(r.get("wrong_question_ids_json") or "[]")
        return rows
    return _load(RESULTS_FILE)

def get_result_by_id(result_id):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM results WHERE id = %s", (result_id,))
            row = cur.fetchone()
        conn.close()
        if row:
            row["candidate"] = json.loads(row.get("candidate_json") or "{}")
            row["assessment"] = json.loads(row.get("assessment_json") or "{}")
            row["results"] = json.loads(row.get("results_json") or "{}")
            row["category_breakdown"] = json.loads(row.get("category_breakdown_json") or "{}")
            row["wrong_question_ids"] = json.loads(row.get("wrong_question_ids_json") or "[]")
        return row
    for r in _load(RESULTS_FILE):
        if r.get("id") == result_id:
            return r
    return None

def get_stats():
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM results")
            total = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) as passed FROM results WHERE JSON_EXTRACT(results_json, '$.passed') = TRUE")
            passed = cur.fetchone()["passed"]
            cur.execute("SELECT AVG(JSON_EXTRACT(results_json, '$.pct_score')) as avg FROM results")
            avg_row = cur.fetchone()
            avg = round(avg_row["avg"] or 0, 1)
            cur.execute("SELECT COUNT(*) as pending FROM results WHERE JSON_EXTRACT(results_json, '$.passed') = FALSE")
            pending = cur.fetchone()["pending"]
            cur.execute("SELECT COUNT(*) as c FROM candidates")
            total_candidates = cur.fetchone()["c"]
        conn.close()
        return {
            "total_evaluated": total,
            "total_candidates": total_candidates,
            "pass_rate": round(passed / total * 100, 1) if total else 0,
            "avg_score": avg,
            "pending_reviews": pending,
        }
    results = _load(RESULTS_FILE)
    candidates = _load(CANDIDATES_FILE)
    total = len(results)
    passed = sum(1 for r in results if r.get("results", {}).get("passed", False))
    avg = 0
    if total:
        avg = round(sum(r.get("results", {}).get("pct_score", 0) for r in results) / total, 1)
    return {
        "total_evaluated": total,
        "total_candidates": len(candidates),
        "pass_rate": round(passed / total * 100, 1) if total else 0,
        "avg_score": avg,
        "pending_reviews": sum(1 for r in results if not r.get("results", {}).get("passed", False)),
    }

def get_heatmap_rows():
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT candidate_json, assessment_json, results_json, category_breakdown_json FROM results")
            rows = cur.fetchall()
        conn.close()
        out = []
        for r in rows:
            c = json.loads(r["candidate_json"] or "{}")
            cat = json.loads(r["category_breakdown_json"] or "{}")
            scores = {k: v.get("pct", 0) for k, v in cat.items()}
            avg = round(sum(scores.values()) / len(scores), 1) if scores else 0
            out.append({
                "name": c.get("full_name", "—"),
                "employee_id": c.get("employee_id", "—"),
                "level": json.loads(r["assessment_json"] or "{}").get("level", "—"),
                "categories": scores,
                "avg": avg,
                "passed": json.loads(r["results_json"] or "{}").get("passed", False),
            })
        return out
    out = []
    for r in _load(RESULTS_FILE):
        c = r.get("candidate", {})
        cat = r.get("category_breakdown", {})
        scores = {k: v.get("pct", 0) for k, v in cat.items()}
        avg = round(sum(scores.values()) / len(scores), 1) if scores else 0
        out.append({
            "name": c.get("full_name", "—"),
            "employee_id": c.get("employee_id", "—"),
            "level": r.get("assessment", {}).get("level", "—"),
            "categories": scores,
            "avg": avg,
            "passed": r.get("results", {}).get("passed", False),
        })
    return out

def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "candidate_id", "full_name", "employee_id", "department", "job_role",
        "company_name", "contact_email", "level", "score_pct", "earned_pts", "max_pts", "passed",
        "correct_answers", "time_seconds", "submitted_at"
    ])
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM results ORDER BY created_at DESC")
            rows = cur.fetchall()
        conn.close()
        for r in rows:
            c = json.loads(r.get("candidate_json") or "{}")
            a = json.loads(r.get("assessment_json") or "{}")
            res = json.loads(r.get("results_json") or "{}")
            writer.writerow([
                c.get("candidate_id", ""), c.get("full_name", ""), c.get("employee_id", ""),
                c.get("department", ""), c.get("job_role", ""),
                c.get("company_name", ""), c.get("contact_email", ""),
                a.get("level", ""), res.get("pct_score", ""), res.get("earned_pts", ""),
                res.get("max_pts", ""), "APROBADO" if res.get("passed") else "NO_APROBADO",
                res.get("correct_answers", ""), res.get("time_seconds", ""),
                r.get("submitted_at", ""),
            ])
    else:
        for r in _load(RESULTS_FILE):
            c = r.get("candidate", {})
            a = r.get("assessment", {})
            res = r.get("results", {})
            writer.writerow([
                c.get("candidate_id", ""), c.get("full_name", ""), c.get("employee_id", ""),
                c.get("department", ""), c.get("job_role", ""),
                c.get("company_name", ""), c.get("contact_email", ""),
                a.get("level", ""), res.get("pct_score", ""), res.get("earned_pts", ""),
                res.get("max_pts", ""), "APROBADO" if res.get("passed") else "NO_APROBADO",
                res.get("correct_answers", ""), res.get("time_seconds", ""),
                r.get("submitted_at", ""),
            ])
    return output.getvalue().encode("utf-8")

# ── Handler ──────────────────────────────────────────────────────────────────
class CarolHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parsed = urllib.parse.urlparse(path)
        clean = urllib.parse.unquote(parsed.path)
        if clean.startswith("/"):
            clean = clean[1:]
        target = os.path.join(WEB_DIR, clean)
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        return target

    def log_message(self, fmt, *args):
        print(f"[{_now_iso()}] {self.address_string()} {fmt % args}")

    def _send_json(self, status, data):
        def _serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
        body = json.dumps(data, ensure_ascii=False, default=_serialize).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path

        # ── Webhook: Registration ──
        if path == "/webhook/carol-registration":
            payload = self._read_body()
            respondent = payload.get("respondent", {})
            computed = payload.get("computed", {})
            cid = str(uuid.uuid4())
            candidate = {
                "id": cid,
                "candidate_id": cid,
                "survey_id": payload.get("survey_id", "carol_registration_v2"),
                "full_name": respondent.get("full_name", ""),
                "employee_id": respondent.get("employee_id", ""),
                "birth_year": respondent.get("birth_year"),
                "birth_month": respondent.get("birth_month"),
                "department": respondent.get("department", ""),
                "job_role": respondent.get("job_role", ""),
                "years_experience": respondent.get("years_experience"),
                "self_evaluation": respondent.get("self_evaluation"),
                "company_name": respondent.get("company_name", ""),
                "contact_email": respondent.get("contact_email", ""),
                "assigned_level": computed.get("assigned_level", "basic"),
                "status": "registered",
                "registered_at": _now_iso(),
                "submitted_at": payload.get("submitted_at", _now_iso()),
            }
            store_candidate(candidate)
            level = candidate["assigned_level"]
            self._send_json(200, {
                "success": True,
                "candidate_id": cid,
                "assigned_level": level,
                "assessment_url": f"/?level={level}&cid={cid}",
                "message_es": f"Tu evaluación asignada es Nivel {level.capitalize()}. ¡Buena suerte!"
            })
            return

        # ── Webhook: Results ──
        if path == "/webhook/carol-results":
            payload = self._read_body()
            result = {
                "id": str(uuid.uuid4()),
                "submitted_at": payload.get("submitted_at", _now_iso()),
                "candidate": payload.get("candidate", {}),
                "assessment": payload.get("assessment", {}),
                "results": payload.get("results", {}),
                "category_breakdown": payload.get("category_breakdown", {}),
                "wrong_question_ids": payload.get("wrong_question_ids", []),
                "stored_at": _now_iso(),
            }
            store_result(result)
            self._send_json(200, {"success": True, "stored": True, "id": result["id"]})
            return

        self._send_json(404, {"error": "Not found"})

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # ── API: Stats ──
        if path == "/api/stats":
            self._send_json(200, get_stats())
            return

        # ── API: Candidates ──
        if path == "/api/candidates":
            self._send_json(200, get_candidates())
            return

        # ── API: Results ──
        if path == "/api/results":
            level = qs.get("level", [None])[0]
            dept = qs.get("department", [None])[0]
            passed_q = qs.get("passed", [None])[0]
            data = get_results()
            filtered = []
            for r in data:
                a = r.get("assessment", {})
                c = r.get("candidate", {})
                res = r.get("results", {})
                if level and a.get("level") != level:
                    continue
                if dept and c.get("department") != dept:
                    continue
                if passed_q is not None:
                    target = passed_q.lower() in ("true", "1", "yes")
                    if res.get("passed") != target:
                        continue
                filtered.append(r)
            self._send_json(200, filtered)
            return

        # ── API: Single Result ──
        if path.startswith("/api/result/"):
            result_id = path.split("/")[-1]
            row = get_result_by_id(result_id)
            if row:
                self._send_json(200, row)
            else:
                self._send_json(404, {"error": "Result not found"})
            return

        # ── API: Heatmap data ──
        if path == "/api/heatmap":
            self._send_json(200, get_heatmap_rows())
            return

        # ── API: Export CSV ──
        if path == "/api/export.csv":
            body = export_csv()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=carol_results.csv")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        # Fallback to static files
        super().do_GET()


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import socket
    init_db()
    class ReusableTCPServer(HTTPServer):
        allow_reuse_address = True
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            super().server_bind()
    with ReusableTCPServer((HOST, PORT), CarolHandler) as httpd:
        mode = "MySQL" if USE_MYSQL else "JSON"
        print(f"CAROL server running at http://{HOST}:{PORT}/ [{mode} mode]")
        print(f"  → Web root: {WEB_DIR}")
        print("  → Endpoints:")
        print(f"     POST /webhook/carol-registration")
        print(f"     POST /webhook/carol-results")
        print(f"     GET  /api/stats")
        print(f"     GET  /api/candidates")
        print(f"     GET  /api/results")
        print(f"     GET  /api/heatmap")
        print(f"     GET  /api/export.csv")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
