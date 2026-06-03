#!/usr/bin/env python3
"""
CAROL Server — Dual mode: MySQL (Docker/production) or JSON (local dev)
Serves API/webhook endpoints. Static files handled by Caddy upstream in Docker.
"""
import os, sys, json, csv, io, uuid, urllib.parse, time, hmac, hashlib, base64
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler

try:
    import jwt
    HAS_JWT = True
except ImportError:
    HAS_JWT = False
    jwt = None

try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False
    FPDF = object

# ── Config ───────────────────────────────────────────────────────────────────
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "carol")
DB_USER = os.getenv("DB_USER", "carol")
DB_PASSWORD = os.getenv("DB_PASSWORD", "carolpass")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# ── Admin Auth Config ────────────────────────────────────────────────────────
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "marco@soul23.mx")
ADMIN_NAME = os.getenv("ADMIN_NAME", "Marco Gallegos")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "") or "#Yamakasi111#"
JWT_SECRET = os.getenv("JWT_SECRET", "") or "carol-default-jwt-secret-change-me"
JWT_ALGO = "HS256"
OPEN_MODE = os.getenv("OPEN_MODE", "false").lower() == "true"

if not os.getenv("JWT_SECRET", ""):
    print("[WARN] JWT_SECRET not set via environment; using default. Set it in production!")

def _make_token(payload: dict) -> str:
    if HAS_JWT:
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    # fallback simple HMAC token
    msg = json.dumps(payload, sort_keys=True)
    sig = hmac.new(JWT_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return base64.urlsafe_b64encode(f"{msg}.{sig}".encode()).decode().rstrip("=")

def _decode_token(token: str) -> dict:
    if HAS_JWT:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    # fallback
    try:
        padded = token + "=" * (4 - len(token) % 4)
        decoded = base64.urlsafe_b64decode(padded).decode()
        msg, sig = decoded.rsplit(".", 1)
        expected = hmac.new(JWT_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise ValueError("Invalid signature")
        payload = json.loads(msg)
        if "exp" in payload and time.time() > payload["exp"]:
            raise ValueError("Token expired")
        return payload
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DATA_DIR = os.path.join(BASE_DIR, ".carol_data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
RESULTS_FILE = os.path.join(DATA_DIR, "results.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
AUDIT_FILE = os.path.join(DATA_DIR, "audit_logs.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")
API_KEYS_FILE = os.path.join(DATA_DIR, "api_keys.json")

# ── Report engine (optional) ─────────────────────────────────────────────────
REPORT_ENGINE = None
try:
    sys.path.insert(0, os.path.join(BASE_DIR, "reports"))
    import report_engine
    REPORT_ENGINE = report_engine
except Exception as _report_err:
    print(f"[WARN] Report engine not available: {_report_err}")

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
    except Exception as e:
        print(f"[DB] MySQL not available ({e}), falling back to JSON files.")

print(f"[DB] Mode: {'MySQL' if USE_MYSQL else 'JSON files'} ({DB_HOST or 'no host'})")

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

def _clean_key(value):
    return str(value or "").strip().lower()

def _audit_log(action: str, target_type: str, target_id: str, user_email: str, detail: str = ""):
    entry = {
        "id": str(uuid.uuid4()),
        "action": action,
        "target_type": target_type,
        "target_id": target_id,
        "user_email": user_email,
        "detail": detail,
        "timestamp": _now_iso(),
    }
    if USE_MYSQL:
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id VARCHAR(36) PRIMARY KEY,
                        action VARCHAR(50),
                        target_type VARCHAR(50),
                        target_id VARCHAR(36),
                        user_email VARCHAR(255),
                        detail TEXT,
                        timestamp DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                cur.execute("""
                    INSERT INTO audit_logs (id, action, target_type, target_id, user_email, detail, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (entry["id"], entry["action"], entry["target_type"], entry["target_id"],
                      entry["user_email"], entry["detail"], entry["timestamp"]))
            conn.close()
        except Exception as e:
            print(f"[AUDIT ERROR] {e}")
    else:
        logs = _load(AUDIT_FILE)
        logs.append(entry)
        _save(AUDIT_FILE, logs)

def _hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# ── API Keys helpers ────────────────────────────────────────────────────────

def _generate_api_key() -> str:
    return "carol_" + hashlib.sha256(os.urandom(32)).hexdigest()[:48]

def _hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def _load_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        return []
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_api_keys(keys):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)

def _find_api_key_by_hash(key_hash: str):
    if USE_MYSQL:
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM api_keys WHERE key_hash = %s", (key_hash,))
                row = cur.fetchone()
            conn.close()
            if row:
                return row
        except Exception:
            pass
    for k in _load_api_keys():
        if k.get("key_hash") == key_hash:
            return k
    return None

def store_api_key(api_key: dict):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO api_keys (id, name, key_hash, key_prefix, role, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (api_key["id"], api_key["name"], api_key["key_hash"], api_key["key_prefix"],
                  api_key["role"], api_key["created_by"], api_key["created_at"]))
        conn.close()
    else:
        keys = _load_api_keys()
        keys.append(api_key)
        _save_api_keys(keys)

def delete_api_key(key_id: str):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM api_keys WHERE id = %s", (key_id,))
        conn.close()
    else:
        keys = _load_api_keys()
        keys = [k for k in keys if k.get("id") != key_id]
        _save_api_keys(keys)

def get_api_keys():
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM api_keys ORDER BY created_at DESC")
            rows = cur.fetchall()
        conn.close()
        return rows
    return sorted(_load_api_keys(), key=lambda x: x.get("created_at", ""), reverse=True)

def update_api_key_last_used(key_id: str):
    now = _now_iso()
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("UPDATE api_keys SET last_used_at = %s WHERE id = %s", (now, key_id))
        conn.close()
    else:
        keys = _load_api_keys()
        for k in keys:
            if k.get("id") == key_id:
                k["last_used_at"] = now
                break
        _save_api_keys(keys)

def _load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def _find_user_by_email(email: str):
    email = email.strip().lower()
    for u in _load_users():
        if u.get("email", "").strip().lower() == email:
            return u
    return None

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
                        answers_json JSON,
                        stored_at DATETIME,
                        deleted_at DATETIME,
                        deleted_by VARCHAR(255),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_candidate_id (candidate_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                # Migrate: add columns if missing
                for col_sql in [
                    "ALTER TABLE results ADD COLUMN answers_json JSON AFTER wrong_question_ids_json",
                    "ALTER TABLE results ADD COLUMN deleted_at DATETIME AFTER stored_at",
                    "ALTER TABLE results ADD COLUMN deleted_by VARCHAR(255) AFTER deleted_at",
                ]:
                    try:
                        cur.execute(col_sql)
                    except Exception:
                        pass
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id VARCHAR(36) PRIMARY KEY,
                        action VARCHAR(50),
                        target_type VARCHAR(50),
                        target_id VARCHAR(36),
                        user_email VARCHAR(255),
                        detail TEXT,
                        timestamp DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_sessions (
                        id VARCHAR(36) PRIMARY KEY,
                        candidate_id VARCHAR(36),
                        level VARCHAR(50),
                        levels_json JSON,
                        level_index INT DEFAULT 0,
                        answers_json JSON,
                        current_q INT DEFAULT 0,
                        seconds_left INT,
                        seconds_total INT,
                        started_at DATETIME,
                        last_saved_at DATETIME,
                        submitted BOOLEAN DEFAULT FALSE,
                        all_results_json JSON,
                        status VARCHAR(50) DEFAULT 'active',
                        answer_key_json JSON,
                        questions_json JSON,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_candidate_id (candidate_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                # Add new columns if missing (migration)
                for col, typedef in [("answer_key_json", "JSON"), ("questions_json", "JSON")]:
                    try:
                        cur.execute(f"ALTER TABLE quiz_sessions ADD COLUMN {col} {typedef}")
                    except Exception:
                        pass  # Column already exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS api_keys (
                        id VARCHAR(36) PRIMARY KEY,
                        name VARCHAR(255),
                        key_hash VARCHAR(64),
                        key_prefix VARCHAR(12),
                        role VARCHAR(50) DEFAULT 'viewer',
                        created_by VARCHAR(255),
                        created_at DATETIME,
                        last_used_at DATETIME
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                # Backfill: fix results with empty candidate_id from candidate_json
                try:
                    cur.execute("SELECT id, candidate_json FROM results WHERE candidate_id IS NULL OR candidate_id = ''")
                    empty_rows = cur.fetchall()
                    if empty_rows:
                        for row in empty_rows:
                            cj = json.loads(row.get("candidate_json") or "{}")
                            cid = cj.get("candidate_id") or cj.get("id") or ""
                            if cid:
                                cur.execute("UPDATE results SET candidate_id = %s WHERE id = %s", (cid, row["id"]))
                        print(f"[DB] Backfilled candidate_id for {len(empty_rows)} results")
                except Exception as e:
                    print(f"[DB] Backfill warning: {e}")
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
                 category_breakdown_json, wrong_question_ids_json, answers_json, stored_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                result["id"],
                result.get("candidate", {}).get("candidate_id", ""),
                result.get("submitted_at", _now_iso()),
                json.dumps(result.get("candidate", {}), ensure_ascii=False),
                json.dumps(result.get("assessment", {}), ensure_ascii=False),
                json.dumps(result.get("results", {}), ensure_ascii=False),
                json.dumps(result.get("category_breakdown", {}), ensure_ascii=False),
                json.dumps(result.get("wrong_question_ids", []), ensure_ascii=False),
                json.dumps(result.get("answers", {}), ensure_ascii=False),
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

def get_results(include_deleted=False):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            if include_deleted:
                cur.execute("SELECT * FROM results ORDER BY created_at DESC")
            else:
                cur.execute("SELECT * FROM results WHERE deleted_at IS NULL ORDER BY created_at DESC")
            rows = cur.fetchall()
        conn.close()
        for r in rows:
            r["candidate"] = json.loads(r.get("candidate_json") or "{}")
            r["assessment"] = json.loads(r.get("assessment_json") or "{}")
            r["results"] = json.loads(r.get("results_json") or "{}")
            cat_bd = json.loads(r.get("category_breakdown_json") or "{}")
            if not cat_bd:
                cr = r["results"].get("categories_results", {})
                cat_bd = {k: {"correct": v.get("score", 0), "total": v.get("total", 0), "pct": v.get("pct_score", v.get("pct", 0))} for k, v in cr.items()}
            r["category_breakdown"] = cat_bd
            r["wrong_question_ids"] = json.loads(r.get("wrong_question_ids_json") or "[]")
            r["answers"] = json.loads(r.get("answers_json") or "{}")
        return rows
    rows = _load(RESULTS_FILE)
    if not include_deleted:
        rows = [r for r in rows if not r.get("deleted_at")]
    return rows

def get_result_by_id(result_id, include_deleted=False):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            if include_deleted:
                cur.execute("SELECT * FROM results WHERE id = %s", (result_id,))
            else:
                cur.execute("SELECT * FROM results WHERE id = %s AND deleted_at IS NULL", (result_id,))
            row = cur.fetchone()
        conn.close()
        if row:
            row["candidate"] = json.loads(row.get("candidate_json") or "{}")
            row["assessment"] = json.loads(row.get("assessment_json") or "{}")
            row["results"] = json.loads(row.get("results_json") or "{}")
            cat_bd = json.loads(row.get("category_breakdown_json") or "{}")
            if not cat_bd:
                cr = row["results"].get("categories_results", {})
                cat_bd = {k: {"correct": v.get("score", 0), "total": v.get("total", 0), "pct": v.get("pct_score", v.get("pct", 0))} for k, v in cr.items()}
            row["category_breakdown"] = cat_bd
            row["wrong_question_ids"] = json.loads(row.get("wrong_question_ids_json") or "[]")
            row["answers"] = json.loads(row.get("answers_json") or "{}")
        return row
    for r in _load(RESULTS_FILE):
        if r.get("id") == result_id and (include_deleted or not r.get("deleted_at")):
            return r
    return None

def get_results_by_candidate_id(candidate_id, include_deleted=False):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            if include_deleted:
                cur.execute("SELECT * FROM results WHERE candidate_id = %s ORDER BY submitted_at DESC", (candidate_id,))
            else:
                cur.execute("SELECT * FROM results WHERE candidate_id = %s AND deleted_at IS NULL ORDER BY submitted_at DESC", (candidate_id,))
            rows = cur.fetchall()
            # Fallback: search inside candidate_json for candidate_id
            if not rows:
                like_id = f'%"{candidate_id}"%'
                if include_deleted:
                    cur.execute("SELECT * FROM results WHERE candidate_json LIKE %s ORDER BY submitted_at DESC", (like_id,))
                else:
                    cur.execute("SELECT * FROM results WHERE candidate_json LIKE %s AND deleted_at IS NULL ORDER BY submitted_at DESC", (like_id,))
                rows = cur.fetchall()
            # Fallback: look up candidate email and match by email in candidate_json
            if not rows:
                cur.execute("SELECT contact_email FROM candidates WHERE candidate_id = %s", (candidate_id,))
                cand = cur.fetchone()
                if cand and cand.get("contact_email"):
                    like_email = f'%{cand["contact_email"]}%'
                    if include_deleted:
                        cur.execute("SELECT * FROM results WHERE candidate_json LIKE %s ORDER BY submitted_at DESC", (like_email,))
                    else:
                        cur.execute("SELECT * FROM results WHERE candidate_json LIKE %s AND deleted_at IS NULL ORDER BY submitted_at DESC", (like_email,))
                    rows = cur.fetchall()
        conn.close()
        for r in rows:
            r["candidate"] = json.loads(r.get("candidate_json") or "{}")
            r["assessment"] = json.loads(r.get("assessment_json") or "{}")
            r["results"] = json.loads(r.get("results_json") or "{}")
            cat_bd = json.loads(r.get("category_breakdown_json") or "{}")
            if not cat_bd:
                cr = r["results"].get("categories_results", {})
                cat_bd = {k: {"correct": v.get("score", 0), "total": v.get("total", 0), "pct": v.get("pct_score", v.get("pct", 0))} for k, v in cr.items()}
            r["category_breakdown"] = cat_bd
            r["wrong_question_ids"] = json.loads(r.get("wrong_question_ids_json") or "[]")
            r["answers"] = json.loads(r.get("answers_json") or "{}")
        return rows
    rows = _load(RESULTS_FILE)
    return [r for r in rows if r.get("candidate", {}).get("candidate_id") == candidate_id and (include_deleted or not r.get("deleted_at"))]

def soft_delete_result(result_id, user_email):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("UPDATE results SET deleted_at = %s, deleted_by = %s WHERE id = %s", (_now_iso(), user_email, result_id))
        conn.close()
    else:
        results = _load(RESULTS_FILE)
        for r in results:
            if r.get("id") == result_id:
                r["deleted_at"] = _now_iso()
                r["deleted_by"] = user_email
                break
        _save(RESULTS_FILE, results)
    _audit_log("delete", "result", result_id, user_email, f"Soft-deleted result {result_id}")

def delete_candidate_record(candidate_id, user_email):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM candidates WHERE id = %s OR candidate_id = %s", (candidate_id, candidate_id))
            deleted = cur.rowcount
        conn.close()
    else:
        candidates = _load(CANDIDATES_FILE)
        remaining = [
            c for c in candidates
            if c.get("id") != candidate_id and c.get("candidate_id") != candidate_id
        ]
        deleted = len(candidates) - len(remaining)
        _save(CANDIDATES_FILE, remaining)
    if deleted:
        _audit_log("delete", "candidate", candidate_id, user_email, f"Deleted candidate {candidate_id}")
    return deleted

def soft_delete_results_by_candidate(candidate_id, user_email):
    if USE_MYSQL:
        conn = get_conn()
        like_candidate_id = f'%"{candidate_id}"%'
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE results
                SET deleted_at = %s, deleted_by = %s
                WHERE deleted_at IS NULL
                  AND (candidate_id = %s OR candidate_json LIKE %s)
                """,
                (_now_iso(), user_email, candidate_id, like_candidate_id),
            )
            deleted = cur.rowcount
        conn.close()
    else:
        results = _load(RESULTS_FILE)
        deleted = 0
        for r in results:
            candidate = r.get("candidate") or {}
            if not r.get("deleted_at") and (
                r.get("candidate_id") == candidate_id
                or candidate.get("candidate_id") == candidate_id
                or candidate.get("id") == candidate_id
            ):
                r["deleted_at"] = _now_iso()
                r["deleted_by"] = user_email
                deleted += 1
        _save(RESULTS_FILE, results)
    if deleted:
        _audit_log("delete", "results", candidate_id, user_email, f"Soft-deleted {deleted} results for candidate {candidate_id}")
    return deleted

# ── Session storage helpers ──────────────────────────────────────────────────

def store_session(session):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO quiz_sessions
                (id, candidate_id, level, levels_json, level_index, answers_json, current_q,
                 seconds_left, seconds_total, started_at, last_saved_at, submitted, all_results_json, status,
                 answer_key_json, questions_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session["id"],
                session.get("candidate_id", ""),
                session.get("level", ""),
                json.dumps(session.get("levels", []), ensure_ascii=False),
                session.get("level_index", 0),
                json.dumps(session.get("answers", {}), ensure_ascii=False),
                session.get("current_q", 0),
                session.get("seconds_left", 0),
                session.get("seconds_total", 0),
                session.get("started_at", _now_iso()),
                session.get("last_saved_at", _now_iso()),
                session.get("submitted", False),
                json.dumps(session.get("all_results", []), ensure_ascii=False),
                session.get("status", "active"),
                json.dumps(session.get("answer_key", {}), ensure_ascii=False),
                json.dumps(session.get("questions", []), ensure_ascii=False),
            ))
        conn.close()
    else:
        sessions = _load(SESSIONS_FILE)
        sessions.append(session)
        _save(SESSIONS_FILE, sessions)

def update_session(session_id, fields):
    now = _now_iso()
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            # Build dynamic SET clause
            set_parts = []
            values = []
            for key, val in fields.items():
                if key in ("answers", "levels", "all_results"):
                    set_parts.append(f"{key}_json = %s")
                    values.append(json.dumps(val, ensure_ascii=False))
                elif key in ("answer_key", "questions"):
                    set_parts.append(f"{key}_json = %s")
                    values.append(json.dumps(val, ensure_ascii=False))
                elif key == "current_q":
                    set_parts.append("current_q = %s")
                    values.append(val)
                elif key == "level_index":
                    set_parts.append("level_index = %s")
                    values.append(val)
                elif key == "seconds_left":
                    set_parts.append("seconds_left = %s")
                    values.append(val)
                elif key == "submitted":
                    set_parts.append("submitted = %s")
                    values.append(val)
                elif key == "status":
                    set_parts.append("status = %s")
                    values.append(val)
            if set_parts:
                set_parts.append("last_saved_at = %s")
                values.append(now)
                values.append(session_id)
                sql = f"UPDATE quiz_sessions SET {', '.join(set_parts)} WHERE id = %s"
                cur.execute(sql, values)
        conn.close()
    else:
        sessions = _load(SESSIONS_FILE)
        for s in sessions:
            if s.get("id") == session_id:
                for key, val in fields.items():
                    s[key] = val
                s["last_saved_at"] = now
                break
        _save(SESSIONS_FILE, sessions)

def get_session(session_id):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM quiz_sessions WHERE id = %s", (session_id,))
            row = cur.fetchone()
        conn.close()
        if row:
            row["levels"] = json.loads(row.get("levels_json") or "[]")
            row["answers"] = json.loads(row.get("answers_json") or "{}")
            row["all_results"] = json.loads(row.get("all_results_json") or "[]")
            row["answer_key"] = json.loads(row.get("answer_key_json") or "{}")
            row["questions"] = json.loads(row.get("questions_json") or "[]")
        return row
    for s in _load(SESSIONS_FILE):
        if s.get("id") == session_id:
            return s
    return None

def get_active_session(candidate_id):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM quiz_sessions WHERE candidate_id = %s AND submitted = FALSE ORDER BY last_saved_at DESC LIMIT 1",
                (candidate_id,),
            )
            row = cur.fetchone()
        conn.close()
        if row:
            row["levels"] = json.loads(row.get("levels_json") or "[]")
            row["answers"] = json.loads(row.get("answers_json") or "{}")
            row["all_results"] = json.loads(row.get("all_results_json") or "[]")
            row["answer_key"] = json.loads(row.get("answer_key_json") or "{}")
            row["questions"] = json.loads(row.get("questions_json") or "[]")
        return row
    sessions = _load(SESSIONS_FILE)
    active = [s for s in sessions if s.get("candidate_id") == candidate_id and not s.get("submitted")]
    if not active:
        return None
    active.sort(key=lambda x: x.get("last_saved_at", ""), reverse=True)
    return active[0]

def get_stats():
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM results WHERE deleted_at IS NULL")
            total = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) as passed FROM results WHERE deleted_at IS NULL AND JSON_EXTRACT(results_json, '$.passed') = TRUE")
            passed = cur.fetchone()["passed"]
            cur.execute("SELECT AVG(JSON_EXTRACT(results_json, '$.pct_score')) as avg FROM results WHERE deleted_at IS NULL")
            avg_row = cur.fetchone()
            avg = round(avg_row["avg"] or 0, 1)
            cur.execute("SELECT COUNT(*) as pending FROM results WHERE deleted_at IS NULL AND JSON_EXTRACT(results_json, '$.passed') = FALSE")
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
    results = [r for r in _load(RESULTS_FILE) if not r.get("deleted_at")]
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
            cur.execute("SELECT candidate_json, assessment_json, results_json, category_breakdown_json FROM results WHERE deleted_at IS NULL")
            rows = cur.fetchall()
        conn.close()
        out = []
        for r in rows:
            c = json.loads(r["candidate_json"] or "{}")
            cat = json.loads(r["category_breakdown_json"] or "{}")
            scores = {k: v.get("pct", 0) for k, v in cat.items()}
            if not scores:
                res_obj = json.loads(r["results_json"] or "{}")
                cr = res_obj.get("categories_results", {})
                scores = {k: v.get("pct_score", v.get("pct", 0)) for k, v in cr.items()}
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
        if r.get("deleted_at"):
            continue
        c = r.get("candidate", {})
        cat = r.get("category_breakdown", {})
        scores = {k: v.get("pct", 0) for k, v in cat.items()}
        if not scores:
            cr = r.get("results", {}).get("categories_results", {})
            scores = {k: v.get("pct_score", v.get("pct", 0)) for k, v in cr.items()}
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

def get_audit_logs(limit=200):
    if USE_MYSQL:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
        conn.close()
        return rows
    logs = _load(AUDIT_FILE)
    return sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "CAROL v3 — Reporte de Evaluación", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}} - CAROL Assessment System", align="C")

def generate_pdf(result):
    if not HAS_FPDF:
        return None

    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    c = result.get("candidate", {})
    a = result.get("assessment", {})
    res = result.get("results", {})

    # Candidate Info
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Información del Candidato", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 8, f"Nombre: {c.get('full_name', '—')}", border=0)
    pdf.cell(95, 8, f"ID: {c.get('employee_id', '—')}", ln=True)
    pdf.cell(95, 8, f"Empresa: {c.get('company_name', '—')}", border=0)
    pdf.cell(95, 8, f"Email: {c.get('contact_email', '—')}", ln=True)
    pdf.cell(95, 8, f"Departamento: {c.get('department', '—')}", border=0)
    pdf.cell(95, 8, f"Puesto: {c.get('job_role', '—')}", ln=True)
    pdf.ln(5)

    # Results Info
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Resultados de la Evaluación", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 8, f"Nivel: {a.get('level_name', '—')}", border=0)
    status = "APROBADO" if res.get("passed") else "NO APROBADO"
    pdf.cell(95, 8, f"Estatus: {status}", ln=True)
    pdf.cell(95, 8, f"Puntaje: {res.get('pct_score', 0)}%", border=0)
    pdf.cell(95, 8, f"Correctas: {res.get('correct_answers', 0)} / {a.get('total_questions', '—')}", ln=True)
    m = (res.get("time_seconds", 0) or 0) // 60
    s = (res.get("time_seconds", 0) or 0) % 60
    pdf.cell(95, 8, f"Tiempo: {m}m {s}s", border=0)
    pdf.cell(95, 8, f"Fecha: {result.get('submitted_at', '—')[:10]}", ln=True)
    pdf.ln(5)

    # Category Breakdown
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Desempeño por Categoría", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 8, "Categoría", border=1)
    pdf.cell(40, 8, "Puntaje", border=1, align='C')
    pdf.cell(40, 8, "Correctas", border=1, ln=True, align='C')

    pdf.set_font("Helvetica", "", 10)
    cats = result.get("category_breakdown", {})
    for cat, st in cats.items():
        pdf.cell(100, 8, cat, border=1)
        pdf.cell(40, 8, f"{st.get('pct', 0)}%", border=1, align='C')
        pdf.cell(40, 8, f"{st.get('correct', 0)}/{st.get('total', 0)}", border=1, ln=True, align='C')

    return pdf.output()

def export_csv(result_id=None):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "candidate_id", "full_name", "employee_id", "department", "job_role",
        "company_name", "contact_email", "level", "score_pct", "earned_pts", "max_pts", "passed",
        "correct_answers", "time_seconds", "submitted_at"
    ])

    if result_id:
        res = get_result_by_id(result_id)
        rows = [res] if res else []
    else:
        rows = get_results()

    for r in rows:
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
    def _get_token_payload(self):
        # Check X-API-Key header first
        api_key = self.headers.get("X-API-Key", "")
        if api_key:
            key_hash = _hash_api_key(api_key)
            api_key_obj = _find_api_key_by_hash(key_hash)
            if api_key_obj:
                update_api_key_last_used(api_key_obj["id"])
                return {
                    "sub": api_key_obj.get("created_by", "api"),
                    "name": api_key_obj.get("name", "API Key"),
                    "role": api_key_obj.get("role", "viewer"),
                }
        # Check JWT token
        auth = self.headers.get("Authorization", "")
        if not auth and "?" in self.path:
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            auth = qs.get("token", [""])[0]
        if auth.startswith("Bearer "):
            auth = auth.split(" ", 1)[1]
        if auth:
            try:
                return _decode_token(auth)
            except Exception:
                pass
        return None

    def _is_admin(self):
        payload = self._get_token_payload()
        return payload is not None and payload.get("role") == "admin"

    def _is_authenticated(self):
        return self._get_token_payload() is not None

    def _current_user(self):
        payload = self._get_token_payload()
        if not payload:
            return None
        return {
            "email": payload.get("sub"),
            "name": payload.get("name"),
            "role": payload.get("role"),
        }

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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
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
            print(f"[WEBHOOK /webhook/carol-registration] stored candidate id={cid} email={candidate['contact_email']} mode={'MySQL' if USE_MYSQL else 'JSON'}")
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
            print(f"[WEBHOOK /webhook/carol-results] received payload for candidate: {payload.get('candidate', {}).get('contact_email', 'unknown')}")
            candidate_info = payload.get("candidate", {})
            matched_candidate = None

            # Validation logic
            if not OPEN_MODE:
                candidate_id = _clean_key(candidate_info.get("candidate_id") or candidate_info.get("id"))
                email = _clean_key(candidate_info.get("contact_email"))
                emp_id = _clean_key(candidate_info.get("employee_id"))
                full_name = _clean_key(candidate_info.get("full_name"))

                candidates = get_candidates()
                for c in candidates:
                    if (
                        (candidate_id and candidate_id in (_clean_key(c.get("candidate_id")), _clean_key(c.get("id"))))
                        or (email and email == _clean_key(c.get("contact_email")))
                        or (emp_id and emp_id == _clean_key(c.get("employee_id")))
                        or (full_name and full_name == _clean_key(c.get("full_name")))
                    ):
                        matched_candidate = c
                        break

                if not matched_candidate:
                    print(f"[WEBHOOK REJECTED] Candidate not registered: cid={candidate_id}, email={email}, emp_id={emp_id}, name={full_name}")
                    self._send_json(403, {"error": "Candidato no registrado. Contacte a su administrador."})
                    return
            elif candidate_info.get("candidate_id"):
                matched_candidate = next(
                    (
                        c for c in get_candidates()
                        if _clean_key(c.get("candidate_id")) == _clean_key(candidate_info.get("candidate_id"))
                        or _clean_key(c.get("id")) == _clean_key(candidate_info.get("candidate_id"))
                    ),
                    None,
                )

            if matched_candidate:
                candidate_info = {**candidate_info, "candidate_id": matched_candidate.get("candidate_id") or matched_candidate.get("id")}

            result = {
                "id": str(uuid.uuid4()),
                "submitted_at": payload.get("submitted_at", _now_iso()),
                "candidate": candidate_info,
                "assessment": payload.get("assessment", {}),
                "results": payload.get("results", {}),
                "category_breakdown": payload.get("category_breakdown", {}),
                "wrong_question_ids": payload.get("wrong_question_ids", []),
                "answers": payload.get("answers", {}),
                "stored_at": _now_iso(),
            }
            store_result(result)
            print(f"[WEBHOOK STORED] Result id={result['id']} mode={'MySQL' if USE_MYSQL else 'JSON'}")
            self._send_json(200, {"success": True, "stored": True, "id": result["id"]})
            return

        # ── Auth: Login ──
        if path == "/api/auth/login":
            payload = self._read_body()
            email = payload.get("email", "").strip().lower()
            password = payload.get("password", "")
            # Super-admin
            if email == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
                exp = datetime.utcnow() + timedelta(hours=24)
                token = _make_token({
                    "sub": email,
                    "name": ADMIN_NAME,
                    "role": "admin",
                    "exp": int(exp.timestamp()),
                })
                self._send_json(200, {
                    "success": True,
                    "token": token,
                    "user": {"email": ADMIN_EMAIL, "name": ADMIN_NAME, "role": "admin"}
                })
                return
            # JSON users
            user = _find_user_by_email(email)
            if user and user.get("password_hash") == _hash_pw(password):
                exp = datetime.utcnow() + timedelta(hours=24)
                token = _make_token({
                    "sub": user["email"],
                    "name": user["name"],
                    "role": user.get("role", "viewer"),
                    "exp": int(exp.timestamp()),
                })
                self._send_json(200, {
                    "success": True,
                    "token": token,
                    "user": {"email": user["email"], "name": user["name"], "role": user.get("role", "viewer")}
                })
                return
            self._send_json(401, {"success": False, "error": "Credenciales inválidas"})
            return

        # ── Quiz Session: Create ──
        if path == "/api/session/create":
            payload = self._read_body()
            sid = str(uuid.uuid4())
            session = {
                "id": sid,
                "candidate_id": payload.get("candidate_id", ""),
                "level": payload.get("level", ""),
                "levels": payload.get("levels", []),
                "level_index": payload.get("level_index", 0),
                "answers": payload.get("answers", {}),
                "current_q": payload.get("current_q", 0),
                "seconds_left": payload.get("seconds_left", 0),
                "seconds_total": payload.get("seconds_total", 0),
                "started_at": payload.get("started_at", _now_iso()),
                "last_saved_at": _now_iso(),
                "submitted": False,
                "all_results": payload.get("all_results", []),
                "status": "active",
            }
            store_session(session)
            self._send_json(200, {"success": True, "session_id": sid})
            return

        # ── Quiz Session: Save ──
        if path == "/api/session/save":
            payload = self._read_body()
            sid = payload.get("session_id", "")
            if not sid:
                self._send_json(400, {"error": "session_id required"})
                return
            fields = {}
            if "answers" in payload:
                fields["answers"] = payload["answers"]
            if "current_q" in payload:
                fields["current_q"] = payload["current_q"]
            if "seconds_left" in payload:
                fields["seconds_left"] = payload["seconds_left"]
            if "all_results" in payload:
                fields["all_results"] = payload["all_results"]
            if "level_index" in payload:
                fields["level_index"] = payload["level_index"]
            update_session(sid, fields)
            self._send_json(200, {"success": True, "saved_at": _now_iso()})
            return

        # ── Quiz Session: Submit ──
        if path == "/api/session/submit":
            payload = self._read_body()
            sid = payload.get("session_id", "")
            if not sid:
                self._send_json(400, {"error": "session_id required"})
                return
            fields = {"submitted": True, "status": "completed"}
            if "all_results" in payload:
                fields["all_results"] = payload["all_results"]
            update_session(sid, fields)
            self._send_json(200, {"success": True})
            return

        # ── Users: Create ──
        if path == "/api/users":
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            payload = self._read_body()
            name = payload.get("name", "").strip()
            email = payload.get("email", "").strip().lower()
            password = payload.get("password", "")
            role = payload.get("role", "viewer")
            if not name or not email or not password:
                self._send_json(400, {"error": "Nombre, email y contraseña son obligatorios"})
                return
            if role not in ("admin", "viewer"):
                role = "viewer"
            users = _load_users()
            if any(u.get("email", "").strip().lower() == email for u in users):
                self._send_json(409, {"error": "El usuario ya existe"})
                return
            users.append({
                "id": str(uuid.uuid4()),
                "name": name,
                "email": email,
                "password_hash": _hash_pw(password),
                "role": role,
                "created_at": _now_iso(),
            })
            _save_users(users)
            self._send_json(201, {"success": True, "message": "Usuario creado"})
            return

        # ── API Keys: Create ──
        if path == "/api/api-keys":
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            payload = self._read_body()
            name = payload.get("name", "").strip()
            role = payload.get("role", "viewer")
            if not name:
                self._send_json(400, {"error": "Nombre es obligatorio"})
                return
            if role not in ("admin", "viewer"):
                role = "viewer"
            raw_key = _generate_api_key()
            key_hash = _hash_api_key(raw_key)
            user = self._current_user()
            api_key = {
                "id": str(uuid.uuid4()),
                "name": name,
                "key_hash": key_hash,
                "key_prefix": raw_key[:12],
                "role": role,
                "created_by": user.get("email") if user else "unknown",
                "created_at": _now_iso(),
                "last_used_at": None,
            }
            store_api_key(api_key)
            _audit_log("create", "api_key", api_key["id"], user.get("email", "unknown"), f"Created API key '{name}' [{role}]")
            self._send_json(201, {
                "success": True,
                "message": "API key creada. Guárdala, no se volverá a mostrar.",
                "api_key": raw_key,
                "key_id": api_key["id"],
                "name": name,
                "role": role,
            })
            return

        self._send_json(404, {"error": "Not found"})

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)
        # ── Users: Delete ──
        if path.startswith("/api/users/"):
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            parts = path.split("/")
            if len(parts) < 4:
                self._send_json(400, {"error": "Invalid request"})
                return
            user_id = parts[3]
            users = _load_users()
            new_users = [u for u in users if u.get("id") != user_id]
            if len(new_users) == len(users):
                self._send_json(404, {"error": "Usuario no encontrado"})
                return
            _save_users(new_users)
            self._send_json(200, {"success": True, "message": "Usuario eliminado"})
            return
        # ── Results: Soft Delete ──
        if path.startswith("/api/result/"):
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            parts = path.split("/")
            if len(parts) < 4:
                self._send_json(400, {"error": "Invalid request"})
                return
            result_id = parts[3]
            user = self._current_user()
            user_email = user.get("email") if user else "unknown"
            result = get_result_by_id(result_id, include_deleted=True)
            soft_delete_result(result_id, user_email)
            candidate_deleted = 0
            results_deleted = 0
            delete_candidate = (qs.get("delete_candidate", ["false"])[0].lower() == "true")
            if delete_candidate and result:
                candidate = result.get("candidate") or {}
                candidate_id = candidate.get("candidate_id") or candidate.get("id") or result.get("candidate_id")
                if candidate_id:
                    results_deleted = soft_delete_results_by_candidate(candidate_id, user_email)
                    candidate_deleted = delete_candidate_record(candidate_id, user_email)
            self._send_json(200, {
                "success": True,
                "message": "Evaluación eliminada (soft delete)",
                "candidate_deleted": candidate_deleted,
                "results_deleted": results_deleted,
            })
            return
        # ── Candidates: Delete ──
        if path.startswith("/api/candidates/"):
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            parts = path.split("/")
            if len(parts) < 4:
                self._send_json(400, {"error": "Invalid request"})
                return
            cid = parts[3]
            user = self._current_user()
            user_email = user.get("email", "unknown") if user else "unknown"
            results_deleted = 0
            if qs.get("delete_results", ["false"])[0].lower() == "true":
                results_deleted = soft_delete_results_by_candidate(cid, user_email)
            delete_candidate_record(cid, user_email)
            self._send_json(200, {
                "success": True,
                "message": "Candidato eliminado",
                "results_deleted": results_deleted,
            })
            return
        # ── Candidates: Cleanup ghosts ──
        if path == "/api/candidates/cleanup-ghosts":
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            count = 0
            if USE_MYSQL:
                conn = get_conn()
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM candidates WHERE full_name = '' OR full_name IS NULL")
                    count = cur.rowcount
                conn.close()
            else:
                cands = _load(CANDIDATES_FILE)
                ghosts = [c for c in cands if not c.get("full_name")]
                count = len(ghosts)
                cands = [c for c in cands if c.get("full_name")]
                _save(CANDIDATES_FILE, cands)
            _audit_log("cleanup", "candidates", "ghosts", self._current_user().get("email", "unknown"), f"Cleaned {count} ghost candidates")
            self._send_json(200, {"success": True, "deleted": count})
            return
        # ── API Keys: Delete ──
        if path.startswith("/api/api-keys/"):
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            parts = path.split("/")
            if len(parts) < 4:
                self._send_json(400, {"error": "Invalid request"})
                return
            key_id = parts[3]
            user = self._current_user()
            delete_api_key(key_id)
            _audit_log("delete", "api_key", key_id, user.get("email") if user else "unknown", "Deleted API key")
            self._send_json(200, {"success": True, "message": "API key eliminada"})
            return
        self._send_json(404, {"error": "Not found"})

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # ── Auth: Me ──
        if path == "/api/auth/me":
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                try:
                    token = auth.split(" ", 1)[1]
                    decoded = _decode_token(token)
                    self._send_json(200, {
                        "success": True,
                        "user": {"email": decoded.get("sub"), "name": decoded.get("name"), "role": decoded.get("role")}
                    })
                    return
                except Exception:
                    pass
            self._send_json(401, {"success": False, "error": "No autorizado"})
            return

        # ── API: Stats ──
        if path == "/api/stats":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            self._send_json(200, get_stats())
            return

        # ── API: Candidates ──
        if path == "/api/candidates" or path == "/api/admin/candidates":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            self._send_json(200, get_candidates())
            return

        # ── API: Candidates with evaluation stats ──
        if path == "/api/candidates/stats":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            candidates = get_candidates()
            results = get_results()
            # Build email→candidate_id lookup
            email_to_cid = {}
            for c in candidates:
                email = (c.get("contact_email") or "").lower()
                if email:
                    email_to_cid[email] = c.get("candidate_id")
            stats_map = {}
            for r in results:
                cid = r.get("candidate_id") or (r.get("candidate") or {}).get("candidate_id")
                # Fallback: match by email from candidate_json
                if not cid:
                    cj = r.get("candidate") or {}
                    email = (cj.get("contact_email") or "").lower()
                    if email and email in email_to_cid:
                        cid = email_to_cid[email]
                if not cid:
                    continue
                if cid not in stats_map:
                    stats_map[cid] = {"evaluations": 0, "scores": [], "passed": 0, "last_date": None, "last_level": None}
                s = stats_map[cid]
                s["evaluations"] += 1
                score = (r.get("results") or {}).get("pct_score", 0)
                s["scores"].append(score)
                if (r.get("results") or {}).get("passed"):
                    s["passed"] += 1
                submitted = r.get("submitted_at")
                if submitted and (not s["last_date"] or submitted > s["last_date"]):
                    s["last_date"] = submitted
                    s["last_level"] = (r.get("assessment") or {}).get("level")
            for c in candidates:
                cid = c.get("candidate_id")
                s = stats_map.get(cid, {"evaluations": 0, "scores": [], "passed": 0, "last_date": None, "last_level": None})
                c["eval_count"] = s["evaluations"]
                c["avg_score"] = round(sum(s["scores"]) / len(s["scores"]), 1) if s["scores"] else 0
                c["passed_count"] = s["passed"]
                c["last_eval_date"] = s["last_date"]
                c["last_level"] = s["last_level"]
            self._send_json(200, candidates)
            return

        # ── API: Results ──
        if path == "/api/results" or path == "/api/admin/results":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
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

        # ── API: Single Result (JSON, PDF, or CSV) ──
        if path.startswith("/api/result/"):
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return

            parts = path.split("/")
            # Handle /api/result/{id} or /api/result/{id}/pdf or /api/result/{id}/csv
            result_id = parts[3]
            is_pdf = path.endswith("/pdf")
            is_csv = path.endswith("/csv")

            row = get_result_by_id(result_id)
            if not row:
                self._send_json(404, {"error": "Result not found"})
                return

            if is_pdf:
                if not HAS_FPDF:
                    self._send_json(500, {"error": "FPDF not installed"})
                    return
                body = generate_pdf(row)
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f"attachment; filename=report_{result_id}.pdf")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
            elif is_csv:
                body = export_csv(result_id)
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", f"attachment; filename=result_{result_id}.csv")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
            else:
                self._send_json(200, row)
            return

        # ── API: Report HTML view ──
        if path.startswith("/api/report/") and path.endswith("/view"):
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            parts = path.split("/")
            result_id = parts[3]
            row = get_result_by_id(result_id)
            if not row:
                self._send_json(404, {"error": "Result not found"})
                return
            # Merge candidate info from candidates table if missing fields
            cand = row.get("candidate", {})
            if not cand.get("department") or not cand.get("job_role"):
                candidates = get_candidates()
                email = (cand.get("contact_email") or "").lower()
                emp_id = cand.get("employee_id")
                full_match = None
                for cc in candidates:
                    if email and (cc.get("contact_email") or "").lower() == email:
                        full_match = cc
                        break
                    if emp_id and cc.get("employee_id") == emp_id:
                        full_match = cc
                        break
                if full_match:
                    for field in ["department", "job_role", "years_experience", "company_name"]:
                        if not cand.get(field) and full_match.get(field):
                            cand[field] = full_match[field]
                    row["candidate"] = cand
            report_path = os.path.join(WEB_DIR, "report_email_template.html")
            if not os.path.exists(report_path):
                self._send_json(404, {"error": "Report template not found"})
                return
            try:
                with open(report_path, "r", encoding="utf-8") as f:
                    html = f.read()
                # Embed data into HTML so JS doesn't need a second auth call
                data_json = json.dumps(row, default=str)
                data_json = data_json.replace("</script>", "<\\/script>")
                embed_script = f"<script>window.__REPORT_DATA__={data_json};</script>"
                html = html.replace("</head>", embed_script + "</head>")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html.encode())))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(html.encode())
            except Exception as e:
                print(f"[REPORT VIEW ERROR] {e}")
                self._send_json(500, {"error": str(e)})
            return

        # ── API: Heatmap data ──
        if path == "/api/heatmap":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            self._send_json(200, get_heatmap_rows())
            return

        # ── API: Candidate Results (by candidate_id) ──
        if path.startswith("/api/candidate/") and path.endswith("/results"):
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            parts = path.split("/")
            candidate_id = parts[3]
            self._send_json(200, get_results_by_candidate_id(candidate_id))
            return

        # ── API: Quiz Session (single) ──
        if path.startswith("/api/session/") and not path.startswith("/api/session/active"):
            parts = path.split("/")
            if len(parts) >= 4:
                session_id = parts[3]
                session = get_session(session_id)
                if session:
                    self._send_json(200, {"success": True, "session": session})
                    return
                self._send_json(404, {"error": "Session not found"})
                return

        # ── API: Quiz Session (active) ──
        if path == "/api/session/active":
            candidate_id = qs.get("candidate_id", [None])[0]
            if not candidate_id:
                self._send_json(400, {"error": "candidate_id required"})
                return
            session = get_active_session(candidate_id)
            self._send_json(200, {"success": True, "session": session})
            return

        # ── API: Users ──
        if path == "/api/users":
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            users = _load_users()
            # Never expose password_hash
            safe = [{k: v for k, v in u.items() if k != "password_hash"} for u in users]
            self._send_json(200, safe)
            return

        # ── API: Audit Logs ──
        if path == "/api/audit/logs":
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            self._send_json(200, get_audit_logs())
            return

        # ── API: API Keys ──
        if path == "/api/api-keys":
            if not self._is_admin():
                self._send_json(403, {"error": "Forbidden"})
                return
            keys = get_api_keys()
            safe = [{k: v for k, v in k_item.items() if k != "key_hash"} for k_item in keys]
            self._send_json(200, safe)
            return

        # ── API: Reports — Full session analysis ──
        if path.startswith("/api/reports/session/"):
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            parts = path.split("/")
            session_id = parts[4] if len(parts) > 4 else ""
            session = get_session(session_id)
            if not session:
                self._send_json(404, {"error": "Session not found"})
                return
            candidate_id = session.get("candidate_id", "")
            candidate = None
            for c in get_candidates():
                if c.get("candidate_id") == candidate_id:
                    candidate = c
                    break
            results = get_results_by_candidate_id(candidate_id)
            all_sessions = []
            if USE_MYSQL:
                conn = get_conn()
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM quiz_sessions WHERE candidate_id = %s ORDER BY started_at DESC", (candidate_id,))
                    all_sessions = cur.fetchall()
                conn.close()
                for s in all_sessions:
                    s["levels"] = json.loads(s.get("levels_json") or "[]")
                    s["answers"] = json.loads(s.get("answers_json") or "{}")
                    s["all_results"] = json.loads(s.get("all_results_json") or "[]")
                    s["answer_key"] = json.loads(s.get("answer_key_json") or "{}")
                    s["questions"] = json.loads(s.get("questions_json") or "[]")
            else:
                all_sessions = [s for s in _load(SESSIONS_FILE) if s.get("candidate_id") == candidate_id]
            total_time = sum(s.get("seconds_total", 0) - s.get("seconds_left", 0) for s in all_sessions if s.get("submitted"))
            total_questions = sum(len(s.get("answers", {})) for s in all_sessions if s.get("submitted"))
            scores = [r.get("results", {}).get("pct_score", 0) for r in results if r.get("results", {}).get("pct_score") is not None]
            self._send_json(200, {
                "success": True,
                "session": session,
                "candidate": candidate,
                "results": results,
                "total_sessions": len(all_sessions),
                "completed_sessions": sum(1 for s in all_sessions if s.get("submitted")),
                "total_time_seconds": total_time,
                "total_questions_answered": total_questions,
                "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
                "best_score": max(scores) if scores else 0,
                "attempts": len(results),
            })
            return

        # ── API: Reports — Search by applicant data ──
        if path == "/api/reports/search":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            name = qs.get("name", [None])[0]
            email = qs.get("email", [None])[0]
            phone = qs.get("phone", [None])[0]
            emp_id = qs.get("employee_id", [None])[0]
            all_candidates = get_candidates()
            matched = all_candidates
            if name:
                name_lower = name.lower()
                matched = [c for c in matched if name_lower in (c.get("full_name") or "").lower()]
            if email:
                email_lower = email.lower()
                matched = [c for c in matched if email_lower in (c.get("contact_email") or "").lower()]
            if emp_id:
                emp_lower = emp_id.lower()
                matched = [c for c in matched if emp_lower in (c.get("employee_id") or "").lower()]
            if phone:
                phone_clean = phone.replace(" ", "").replace("-", "")
                matched = [c for c in matched if phone_clean in (c.get("phone") or "").replace(" ", "").replace("-", "")]
            results_all = get_results()
            output = []
            for c in matched:
                cid = c.get("candidate_id", "")
                c_email = (c.get("contact_email") or "").lower()
                c_results = [r for r in results_all if
                    r.get("candidate", {}).get("candidate_id") == cid
                    or r.get("candidate_id") == cid
                    or (c_email and (r.get("candidate") or {}).get("contact_email", "").lower() == c_email)
                    or (cid and cid in json.dumps(r.get("candidate_json") or "", ensure_ascii=False))
                ]
                scores = [r.get("results", {}).get("pct_score", 0) for r in c_results if r.get("results", {}).get("pct_score") is not None]
                output.append({
                    "candidate": c,
                    "total_evaluations": len(c_results),
                    "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
                    "best_score": max(scores) if scores else 0,
                    "last_evaluation": c_results[0].get("submitted_at") if c_results else None,
                    "levels_taken": list(set(r.get("assessment", {}).get("level", "") for r in c_results)),
                })
            self._send_json(200, {"success": True, "results": output, "total": len(output)})
            return

        # ── API: Report PDF ──
        if path.startswith("/api/report/") and path.endswith("/pdf"):
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
            result_id = path.split("/")[3]
            if not REPORT_ENGINE:
                self._send_json(503, {"error": "Report engine not available. Missing dependencies (reportlab/matplotlib)."})
                return
            row = get_result_by_id(result_id)
            if not row:
                self._send_json(404, {"error": "Result not found"})
                return
            try:
                import tempfile
                is_unified = row.get("assessment", {}).get("type") == "unified_sme" or row.get("assessment_type") == "unified_sme"
                if is_unified:
                    candidate_id = row.get("candidate", {}).get("candidate_id", "")
                    related = get_results_by_candidate_id(candidate_id)
                    # Filter to only levels that exist for this candidate
                    related = [r for r in related if r.get("assessment", {}).get("level") in ("basic", "medium", "advanced")]
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp_path = tmp.name
                    REPORT_ENGINE.generate_unified_report(related, tmp_path)
                else:
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp_path = tmp.name
                    REPORT_ENGINE.generate_single_report(row, tmp_path)
                with open(tmp_path, "rb") as f:
                    body = f.read()
                os.unlink(tmp_path)
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="carol_report_{result_id}.pdf"')
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                print(f"[REPORT ERROR] {e}")
                self._send_json(500, {"error": "Failed to generate report", "detail": str(e)})
            return

        # ── API: Export CSV ──
        if path == "/api/export.csv":
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized"})
                return
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
        if path == "/":
            self.path = "/carol_platform.html"
        elif path in ("/admin", "/dashboard"):
            self.path = "/admin.html"

        # Serve any static file from web/ directory
        clean_path = urllib.parse.urlparse(self.path).path
        if clean_path.startswith("/"):
            clean_path = clean_path[1:]
        target = os.path.join(WEB_DIR, clean_path)
        if os.path.isfile(target):
            ext = os.path.splitext(target)[1].lower()
            ct = {".html":"text/html",".css":"text/css",".js":"application/javascript",
                  ".svg":"image/svg+xml",".json":"application/json",".png":"image/png",
                  ".jpg":"image/jpeg",".ico":"image/x-icon",".woff2":"font/woff2"}.get(ext,"application/octet-stream")
            with open(target, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

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
        print(f"     POST /api/session/create")
        print(f"     POST /api/session/save")
        print(f"     POST /api/session/submit")
        print(f"     GET  /api/session/active")
        print(f"     GET  /api/session/<id>")
        print(f"     GET  /api/stats")
        print(f"     GET  /api/candidates")
        print(f"     GET  /api/results")
        print(f"     GET  /api/heatmap")
        print(f"     GET  /api/export.csv")
        print(f"     GET  /api/reports/session/<id>")
        print(f"     GET  /api/reports/search?name=&email=&phone=&employee_id=")
        print(f"     GET  /api/api-keys")
        print(f"     POST /api/api-keys")
        print(f"     DELETE /api/api-keys/<id>")
        print(f"     GET  /api/auth/me")
        print(f"     POST /api/auth/login")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
