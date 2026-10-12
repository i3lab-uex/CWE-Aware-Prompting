import re

# Compile the regex once at import time.  The pattern is simple enough that it
# does not suffer from catastrophic backtracking, but we still keep the
# expression minimal to avoid any unnecessary complexity.
_URL_RE = re.compile(r"^(https?://)[^\s]+$", re.IGNORECASE)


def validate_path(path: str) -> bool:
    """
    Return True if *path* is a syntactically valid http or https URL,
    otherwise return False.  No exceptions are raised for invalid input.
    """
    # Reject non‑string inputs early; this keeps the function safe from
    # accidental misuse and avoids a TypeError inside re.match.
    if not isinstance(path, str):
        return False

    # The regex matches only URLs that start with http:// or https://
    # followed by at least one non‑whitespace character.
    return bool(_URL_RE.match(path))