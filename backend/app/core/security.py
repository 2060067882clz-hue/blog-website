import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from app.core.config import settings
from app.core.exceptions import AppException


def hash_password(password: str, salt: Optional[str] = None) -> str:
    actual_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        actual_salt.encode("utf-8"),
        100_000,
    ).hex()
    return f"{actual_salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    salt, _, stored_digest = password_hash.partition("$")
    if not salt or not stored_digest:
        return False

    expected = hash_password(password, salt).partition("$")[2]
    return hmac.compare_digest(expected, stored_digest)


def _urlsafe_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def _urlsafe_decode(raw: str) -> bytes:
    padding = "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode(raw + padding)


def create_access_token(subject: str) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": subject,
        "exp": int(expires_at.timestamp()),
        "type": "access_token",
    }
    payload_segment = _urlsafe_encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        payload_segment.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    token = f"{payload_segment}.{_urlsafe_encode(signature)}"
    return token, expires_at


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload_segment, signature_segment = token.split(".", 1)
    except ValueError as exc:
        raise AppException(status_code=401, code="INVALID_TOKEN", message="登录凭证无效。") from exc

    expected_signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        payload_segment.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_urlsafe_encode(expected_signature), signature_segment):
        raise AppException(status_code=401, code="INVALID_TOKEN", message="登录凭证无效。")

    try:
        payload = json.loads(_urlsafe_decode(payload_segment))
    except json.JSONDecodeError as exc:
        raise AppException(status_code=401, code="INVALID_TOKEN", message="登录凭证无效。") from exc

    expires_at = int(payload.get("exp", 0))
    if datetime.now(timezone.utc).timestamp() >= expires_at:
        raise AppException(status_code=401, code="TOKEN_EXPIRED", message="登录已过期，请重新登录。")

    return payload
