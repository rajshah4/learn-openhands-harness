"""Shared resume-token protocol introduced for catalog exports."""
import base64
import binascii
import re


def encode_offset(offset: int) -> str:
    return base64.urlsafe_b64encode(f"v2:{offset}".encode()).decode().rstrip("=")


def decode_offset(cursor: str | None) -> int:
    if cursor is None:
        return 0
    if not isinstance(cursor, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", cursor):
        raise ValueError("invalid resume token")
    try:
        raw = base64.b64decode(cursor + "=" * (-len(cursor) % 4), altchars=b"-_", validate=True).decode("ascii")
    except (binascii.Error, UnicodeError, ValueError) as exc:
        raise ValueError("invalid resume token") from exc
    if not re.fullmatch(r"v2:[0-9]+", raw):
        raise ValueError("unsupported resume token")
    offset = int(raw[3:])
    if encode_offset(offset) != cursor:
        raise ValueError("noncanonical resume token")
    return offset
