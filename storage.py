from datetime import datetime
from zoneinfo import ZoneInfo
import os, json

from gspread.auth import service_account_from_dict
from gspread.utils import ValueInputOption

from dotenv import load_dotenv

load_dotenv()

SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "").strip()


if not SHEET_ID:
    raise RuntimeError("Please set the GOOGLE_SHEET_ID environment variable.")


# --- AUTHORIZATION ---------------------------------------------------
def _authorize():
    raw = os.getenv("SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise RuntimeError("SERVICE_ACCOUNT_JSON not set.")
    cred_dict = json.loads(raw)
    return service_account_from_dict(cred_dict, scopes=SCOPE)

def _get_sheet():
    client = _authorize()
    workbook = client.open_by_key(SHEET_ID)
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "").strip()
    return workbook.worksheet(sheet_name) if sheet_name else workbook.sheet1


def append_row(mood: int, note: str = "") -> bool:
    try:
        sheet = _get_sheet()
    except Exception:
        return False
    timestamp = datetime.now(tz=ZoneInfo("US/Pacific")).isoformat(sep=" ", timespec="seconds")
    row = [timestamp, mood, note]
    try:
        sheet.append_row(row, value_input_option=ValueInputOption.user_entered)
        return True
    except Exception:
        return False

def get_counts_between(start_date: str, end_date: str) -> dict[int, int]:
    counts = {i: 0 for i in range(1, 6)}
    try:
        client = _authorize()
        sheet = client.open_by_key(SHEET_ID).sheet1
        all_records = sheet.get_all_records()
    except Exception:
        return counts
    for rec in all_records:
        ts = rec.get("timestamp", "")
        if not ts:
            continue
        date_part = str(ts)[:10]
        if not (start_date <= date_part <= end_date):
            continue
        try:
            mood_val = int(rec.get("mood", 0))
        except ValueError:
            continue
        if 1 <= mood_val <= 5:
            counts[mood_val] += 1
    return counts


def get_latest_notes() -> dict[int, str]:
    """
    Returns a dict {1: latest_note_for_mood1, 2: …, …, 5: …}.
    """
    client = _authorize()
    sheet = client.open_by_key(SHEET_ID).sheet1
    records = sheet.get_all_records()  # each record should have "timestamp","mood","note"
    latest = {}
    for rec in records:
        mood_val = int(rec.get("mood", 0))
        note_text = rec.get("note", "") or ""
        ts = str(rec.get("timestamp", ""))
        if not note_text or not ts:
            continue
        if (
            mood_val not in latest
            or ts > latest[mood_val][0]
        ):
            latest[mood_val] = (ts, note_text)
    # Convert to just note‐text + default to empty string if none:
    return {i: latest.get(i, ("", ""))[1] for i in range(1, 6)}