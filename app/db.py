import sqlite3
import re
import os
import bcrypt
from datetime import datetime
from pathlib import Path

# Database path in data/ directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "schemate.db"


def get_db_connection():
    """Establish and return a SQLite database connection with row factory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initialize database tables for users, conversations, and messages."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            sources_json TEXT,
            audio_blob BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # User Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            preferred_language TEXT DEFAULT 'en',
            date_of_birth TEXT,
            age INTEGER,
            gender TEXT,
            state TEXT,
            district TEXT,
            occupation TEXT,
            annual_family_income REAL,
            education_level TEXT,
            social_category TEXT,
            disability_status TEXT,
            marital_status TEXT,
            additional_attributes TEXT,
            onboarding_completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # Saved Schemes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scheme_id TEXT NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'saved',
            notes TEXT DEFAULT '',
            checklist_json TEXT DEFAULT '[]',
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, scheme_id)
        );
    """)

    # Safe migration: verify checklist_json exists if table was created earlier
    cursor.execute("PRAGMA table_info(saved_schemes);")
    columns = [col[1] for col in cursor.fetchall()]
    if "checklist_json" not in columns:
        cursor.execute("ALTER TABLE saved_schemes ADD COLUMN checklist_json TEXT DEFAULT '[]';")

    conn.commit()
    conn.close()


# Ensure DB is initialized upon import
init_db()


# ==========================================
# Authentication & Validation Helpers
# ==========================================

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def validate_email(email: str) -> bool:
    """Validate email syntax."""
    return bool(email and re.match(EMAIL_REGEX, email.strip()))


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    Requires at least 6 characters.
    """
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def register_user(email: str, name: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Register a new user account.
    Returns (success: bool, message: str, user_dict: dict | None)
    """
    email = email.strip().lower()
    name = name.strip()

    if not name:
        return False, "Please enter your full name.", None

    if not validate_email(email):
        return False, "Please enter a valid email address.", None

    is_valid_pw, pw_msg = validate_password(password)
    if not is_valid_pw:
        return False, pw_msg, None

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists. Please login.", None

        pw_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (email, name, pw_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        user = {"id": user_id, "email": email, "name": name}
        conn.close()
        return True, "Account created successfully!", user
    except Exception as e:
        conn.close()
        return False, f"Registration error: {e}", None


def authenticate_user(email: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Authenticate user with email and password.
    Returns (success: bool, message: str, user_dict: dict | None)
    """
    email = email.strip().lower()
    if not email or not password:
        return False, "Please provide both email and password.", None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, password_hash FROM users WHERE LOWER(email) = ?", (email,))
    user_row = cursor.fetchone()
    conn.close()

    if not user_row:
        return False, "Invalid email or password.", None

    if check_password(password, user_row["password_hash"]):
        user = {
            "id": user_row["id"],
            "email": user_row["email"],
            "name": user_row["name"]
        }
        return True, "Login successful!", user
    else:
        return False, "Invalid email or password.", None


# ==========================================
# Conversation & Chat Storage
# ==========================================

def get_user_conversations(user_id: int) -> list[dict]:
    """Fetch all conversations for a specific user, newest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, user_id, title, created_at, updated_at 
        FROM conversations 
        WHERE user_id = ? 
        ORDER BY updated_at DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_conversation(user_id: int, conversation_id: str, title: str) -> bool:
    """Create a new conversation record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO conversations (id, user_id, title) VALUES (?, ?, ?)",
            (conversation_id, user_id, title)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def update_conversation_title(conversation_id: str, user_id: int, new_title: str) -> bool:
    """Update title and timestamp of a conversation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
        (new_title, conversation_id, user_id)
    )
    conn.commit()
    conn.close()
    return True


def delete_conversation(conversation_id: str, user_id: int) -> bool:
    """Delete a conversation and its messages for an authorized user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM messages WHERE conversation_id = ? AND user_id = ?",
        (conversation_id, user_id)
    )
    cursor.execute(
        "DELETE FROM conversations WHERE id = ? AND user_id = ?",
        (conversation_id, user_id)
    )
    conn.commit()
    conn.close()
    return True


def get_conversation_messages(conversation_id: str, user_id: int) -> list[dict]:
    """Fetch all messages for a given conversation strictly scoped to the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, conversation_id, role, content, sources_json, audio_blob, created_at 
        FROM messages 
        WHERE conversation_id = ? AND user_id = ? 
        ORDER BY id ASC
        """,
        (conversation_id, user_id)
    )
    rows = cursor.fetchall()
    conn.close()

    import json
    messages = []
    for r in rows:
        sources = None
        if r["sources_json"]:
            try:
                sources = json.loads(r["sources_json"])
            except Exception:
                sources = None
        messages.append({
            "id": r["id"],
            "role": r["role"],
            "content": r["content"],
            "sources": sources,
            "audio": r["audio_blob"],
            "created_at": r["created_at"]
        })
    return messages


def add_message(user_id: int, conversation_id: str, role: str, content: str, sources=None, audio_blob=None) -> int:
    """Save a user or assistant message to database and update conversation timestamp."""
    import json
    sources_json = json.dumps(sources) if sources else None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO messages (conversation_id, user_id, role, content, sources_json, audio_blob)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (conversation_id, user_id, role, content, sources_json, audio_blob)
    )
    cursor.execute(
        "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
        (conversation_id, user_id)
    )
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return msg_id


# ==========================================
# User Profile & Onboarding Storage
# ==========================================

def get_user_profile(user_id: int) -> dict | None:
    """Fetch user profile record for a given user id. Returns None if not found."""
    import json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    profile = dict(row)
    # Parse additional_attributes JSON safely
    if profile.get("additional_attributes"):
        try:
            profile["additional_attributes"] = json.loads(profile["additional_attributes"])
        except Exception:
            profile["additional_attributes"] = {}
    else:
        profile["additional_attributes"] = {}

    return profile


def save_user_profile(user_id: int, profile_data: dict) -> bool:
    """
    Save or update user profile. Prevents duplicate records.
    Profile data dict can contain:
    preferred_language, date_of_birth, age, gender, state, district,
    occupation, annual_family_income, education_level, social_category,
    disability_status, marital_status, additional_attributes, onboarding_completed.
    """
    import json
    conn = get_db_connection()
    cursor = conn.cursor()

    existing = get_user_profile(user_id)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Serialize additional attributes if dict
    add_attr = profile_data.get("additional_attributes")
    if isinstance(add_attr, dict):
        add_attr_str = json.dumps(add_attr)
    elif isinstance(add_attr, str):
        add_attr_str = add_attr
    else:
        add_attr_str = json.dumps({})

    # Compute or fallback fields
    preferred_language = profile_data.get("preferred_language") or (existing.get("preferred_language") if existing else "en")
    date_of_birth = profile_data.get("date_of_birth", existing.get("date_of_birth") if existing else None)
    age = profile_data.get("age", existing.get("age") if existing else None)
    gender = profile_data.get("gender", existing.get("gender") if existing else None)
    state = profile_data.get("state", existing.get("state") if existing else None)
    district = profile_data.get("district", existing.get("district") if existing else None)
    occupation = profile_data.get("occupation", existing.get("occupation") if existing else None)
    annual_family_income = profile_data.get("annual_family_income", existing.get("annual_family_income") if existing else None)
    education_level = profile_data.get("education_level", existing.get("education_level") if existing else None)
    social_category = profile_data.get("social_category", existing.get("social_category") if existing else None)
    disability_status = profile_data.get("disability_status", existing.get("disability_status") if existing else None)
    marital_status = profile_data.get("marital_status", existing.get("marital_status") if existing else None)
    onboarding_completed = 1 if profile_data.get("onboarding_completed") else (existing.get("onboarding_completed", 0) if existing else 0)

    try:
        if existing:
            cursor.execute(
                """
                UPDATE user_profiles SET
                    preferred_language = ?,
                    date_of_birth = ?,
                    age = ?,
                    gender = ?,
                    state = ?,
                    district = ?,
                    occupation = ?,
                    annual_family_income = ?,
                    education_level = ?,
                    social_category = ?,
                    disability_status = ?,
                    marital_status = ?,
                    additional_attributes = ?,
                    onboarding_completed = ?,
                    updated_at = ?
                WHERE user_id = ?
                """,
                (
                    preferred_language,
                    date_of_birth,
                    age,
                    gender,
                    state,
                    district,
                    occupation,
                    annual_family_income,
                    education_level,
                    social_category,
                    disability_status,
                    marital_status,
                    add_attr_str,
                    onboarding_completed,
                    now,
                    user_id
                )
            )
        else:
            cursor.execute(
                """
                INSERT INTO user_profiles (
                    user_id,
                    preferred_language,
                    date_of_birth,
                    age,
                    gender,
                    state,
                    district,
                    occupation,
                    annual_family_income,
                    education_level,
                    social_category,
                    disability_status,
                    marital_status,
                    additional_attributes,
                    onboarding_completed,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    preferred_language,
                    date_of_birth,
                    age,
                    gender,
                    state,
                    district,
                    occupation,
                    annual_family_income,
                    education_level,
                    social_category,
                    disability_status,
                    marital_status,
                    add_attr_str,
                    onboarding_completed,
                    now,
                    now
                )
            )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print(f"Error saving user profile: {e}")
        return False


def set_user_language(user_id: int, preferred_language: str) -> bool:
    """Quickly update or initialize language preference for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT user_id FROM user_profiles WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        cursor.execute(
            "UPDATE user_profiles SET preferred_language = ?, updated_at = ? WHERE user_id = ?",
            (preferred_language, now, user_id)
        )
    else:
        cursor.execute(
            """
            INSERT INTO user_profiles (user_id, preferred_language, onboarding_completed, created_at, updated_at)
            VALUES (?, ?, 0, ?, ?)
            """,
            (user_id, preferred_language, now, now)
        )
    conn.commit()
    conn.close()
    return True


def is_onboarding_completed(user_id: int) -> bool:
    """Check whether a user has finished onboarding."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT onboarding_completed FROM user_profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row["onboarding_completed"] == 1:
        return True
    return False


# ==========================================
# Saved Schemes Storage
# ==========================================

def save_scheme(user_id: int, scheme_id: str, status: str = "saved", notes: str = "") -> tuple[bool, str]:
    """
    Save a scheme for an authenticated user.
    Prevents duplicate saves using the UNIQUE(user_id, scheme_id) constraint.
    Returns (success: bool, message: str).
    """
    if not user_id or not scheme_id:
        return False, "Invalid user or scheme ID."

    scheme_id = str(scheme_id).strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if already saved
        cursor.execute(
            "SELECT id FROM saved_schemes WHERE user_id = ? AND scheme_id = ?",
            (user_id, scheme_id)
        )
        if cursor.fetchone():
            conn.close()
            return True, "Scheme is already saved in your collection."

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO saved_schemes (user_id, scheme_id, saved_at, status, notes, checklist_json)
            VALUES (?, ?, ?, ?, ?, '[]')
            """,
            (user_id, scheme_id, now, status, notes)
        )
        conn.commit()
        conn.close()
        return True, "Scheme saved successfully!"
    except sqlite3.IntegrityError as ie:
        conn.close()
        # If it's a unique constraint violation, it's already saved
        if "UNIQUE" in str(ie).upper():
            return True, "Scheme is already saved."
        print(f"Integrity error saving scheme: {ie}")
        return False, f"Integrity error: {ie}"
    except Exception as e:
        conn.close()
        return False, f"Failed to save scheme: {e}"


def unsave_scheme(user_id: int, scheme_id: str) -> bool:
    """Remove a scheme from the user's saved list."""
    if not user_id or not scheme_id:
        return False

    scheme_id = str(scheme_id).strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM saved_schemes WHERE user_id = ? AND scheme_id = ?",
            (user_id, scheme_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print(f"Error unsaving scheme: {e}")
        return False


def is_scheme_saved(user_id: int, scheme_id: str) -> bool:
    """Check if a specific scheme is saved by the user."""
    if not user_id or not scheme_id:
        return False

    scheme_id = str(scheme_id).strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM saved_schemes WHERE user_id = ? AND scheme_id = ?",
        (user_id, scheme_id)
    )
    row = cursor.fetchone()
    conn.close()
    return bool(row)


def get_saved_scheme_ids(user_id: int) -> set[str]:
    """Fetch all saved scheme IDs for a user as a set for O(1) membership checks."""
    if not user_id:
        return set()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT scheme_id FROM saved_schemes WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return {str(r["scheme_id"]) for r in rows}


def get_user_saved_schemes(user_id: int) -> list[dict]:
    """Fetch all saved scheme records for a specific user, newest first."""
    if not user_id:
        return []

    import json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, user_id, scheme_id, saved_at, status, notes, checklist_json
        FROM saved_schemes
        WHERE user_id = ?
        ORDER BY saved_at DESC, id DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        checklist = []
        if r["checklist_json"]:
            try:
                checklist = json.loads(r["checklist_json"])
            except Exception:
                checklist = []
        results.append({
            "id": r["id"],
            "user_id": r["user_id"],
            "scheme_id": str(r["scheme_id"]),
            "saved_at": r["saved_at"],
            "status": r["status"],
            "notes": r["notes"] or "",
            "checklist": checklist,
        })
    return results


def update_saved_scheme_notes(user_id: int, scheme_id: str, notes: str) -> bool:
    """Update personal notes for a saved scheme."""
    if not user_id or not scheme_id:
        return False

    scheme_id = str(scheme_id).strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE saved_schemes SET notes = ? WHERE user_id = ? AND scheme_id = ?",
            (notes.strip(), user_id, scheme_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print(f"Error updating scheme notes: {e}")
        return False


def update_saved_scheme_checklist(user_id: int, scheme_id: str, checklist: list[str]) -> bool:
    """Persistently update the document checklist for a saved scheme."""
    if not user_id or not scheme_id:
        return False

    import json
    scheme_id = str(scheme_id).strip()
    checklist_str = json.dumps(checklist)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE saved_schemes SET checklist_json = ? WHERE user_id = ? AND scheme_id = ?",
            (checklist_str, user_id, scheme_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print(f"Error updating scheme checklist: {e}")
        return False


