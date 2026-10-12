import re

# Regular expression that matches a well‑formed HTTP or HTTPS URL.
# It requires the scheme (http:// or https://), followed by at least one
# non‑whitespace character. The pattern is intentionally simple to avoid
# excessive backtracking or denial‑of‑service vulnerabilities.
_HTTP_URL_RE = re.compile(
    r"^(https?://)"
    r"(?:[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+)$",
    re.IGNORECASE,
)

def verify_path_format(address: str) -> bool:
    """
    Return True if *address* is a syntactically valid HTTP or HTTPS URL,
    otherwise return False.

    The function never raises an exception; any unexpected input is treated
    as invalid.
    """
    if not isinstance(address, str):
        return False

    # Using fullmatch ensures the entire string must match the pattern.
    try:
        return _HTTP_URL_RE.fullmatch(address) is not None
    except Exception:
        # In the unlikely event that re raises an exception, treat as invalid.
        return False