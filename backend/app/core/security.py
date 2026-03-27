import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

from app.core.exceptions import AuthError

# PBKDF2 迭代次数，用于增强密码哈希的抗暴力破解能力。
PBKDF2_ITERATIONS = 120000


def hash_password(password: str, salt: str = "") -> str:
    # 注册或初始化演示账号时，将明文密码转换为带盐哈希值。
    actual_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        actual_salt.encode("utf-8"),
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_sha256${actual_salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    # 登录时按原盐值重新计算哈希，并做安全比较。
    try:
        _, salt, expected_digest = stored_hash.split("$", 2)
    except ValueError:
        return False

    candidate_hash = hash_password(password=password, salt=salt)
    return hmac.compare_digest(candidate_hash, f"pbkdf2_sha256${salt}${expected_digest}")


def create_access_token(subject: str, secret_key: str, expires_in_minutes: int) -> Tuple[str, int]:
    # 这里使用轻量自定义 token 方案，便于当前阶段快速演示和联调。
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=expires_in_minutes)
    payload = {
        "sub": subject,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    encoded_payload = _base64url_encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signature = hmac.new(
        secret_key.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    token = f"{encoded_payload}.{_base64url_encode(signature)}"
    expires_in = int((expires_at - issued_at).total_seconds())
    return token, expires_in


def decode_access_token(token: str, secret_key: str) -> Dict[str, int]:
    # 解析 token 时先验签，再校验过期时间。
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
    except ValueError as exc:
        raise AuthError(code="INVALID_TOKEN", message="Token format is invalid.") from exc

    expected_signature = hmac.new(
        secret_key.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_base64url_encode(expected_signature), encoded_signature):
        raise AuthError(code="INVALID_TOKEN", message="Token signature is invalid.")

    payload_bytes = _base64url_decode(encoded_payload)
    payload = json.loads(payload_bytes.decode("utf-8"))

    now = int(datetime.now(timezone.utc).timestamp())
    if payload.get("exp", 0) < now:
        raise AuthError(code="TOKEN_EXPIRED", message="Token has expired.")

    return payload


def _base64url_encode(raw_bytes: bytes) -> str:
    # 生成适合放进 URL 和请求头中的安全字符串。
    return base64.urlsafe_b64encode(raw_bytes).rstrip(b"=").decode("utf-8")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}".encode("utf-8"))
