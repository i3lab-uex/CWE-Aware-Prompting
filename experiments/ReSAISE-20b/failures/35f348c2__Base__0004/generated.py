import re

# Pre‑compile a simple, efficient regular expression for HTTP/HTTPS URLs.
# The pattern:
#   • Starts with http:// or https://
#   • Followed by a non‑empty host (any characters except whitespace and the first slash)
#   • Followed by an optional path/query/fragment, which may contain any non‑whitespace characters
# This avoids nested quantifiers and therefore prevents catastrophic backtracking.
_HTTP_URL_RE = re.compile(
    r'^https?://[^/\s]+(?:[^\s]*)$',
    flags=re.IGNORECASE
)

def validate_path(path: str) -> bool:
    """
    Return True if `path` is a valid HTTP or HTTPS URL, otherwise False.
    No exceptions are raised; invalid input simply returns False.
    """
    if not isinstance(path, str):
        return False
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    path = path.strip()
    return bool(_HTTP_URL_RE.match(path))