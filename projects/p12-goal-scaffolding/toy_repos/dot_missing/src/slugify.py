"""Small slugify utility with one planted gap: dots are stripped."""

from __future__ import annotations

import re
import unicodedata


def slugify(value: str | None) -> str:
    if not value:
        return ""

    text = str(value).replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text
