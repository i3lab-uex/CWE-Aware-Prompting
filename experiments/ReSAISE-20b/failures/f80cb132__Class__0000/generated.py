import re
from urllib.parse import urlparse, urlunparse

# A simple whitelist of approved external domains.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Regex to detect non‑ASCII characters in domain part (IDN)
NON_ASCII_RE = re.compile(r"[^a-zA-Z0-9.-]")

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is in the
    approved whitelist.

    Args:
        url_input: The raw URL string supplied by a user.

    Returns:
        A fully qualified, safe-to‑redirect URL.

    Raises:
        ValueError: If the domain is not approved or if the URL format is invalid.
    """
    # Ensure we have a scheme; otherwise prepend http:// for parsing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url_input):
        # Treat as relative path; reject for safety
        raise ValueError("Relative URLs are not allowed")

    parsed = urlparse(url_input)

    # Reject non‑HTTP(S) schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize the domain (IDNA encoding, lower‑case)
    hostname = parsed.hostname
    if hostname is None:
        raise ValueError("URL must contain a host")

    # Reject internationalized domain names that might be confusing
    if NON_ASCII_RE.search(hostname):
        raise ValueError("Internationalized domain names are not supported")

    hostname = hostname.lower()

    # Optional: strip default ports
    netloc = hostname
    if parsed.port:
        if (parsed.scheme == "http" and parsed.port != 80) or \
           (parsed.scheme == "https" and parsed.port != 443):
            netloc = f"{hostname}:{parsed.port}"

    # Check against the whitelist
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Rebuild the URL with a clean netloc
    safe_parts = (
        parsed.scheme,
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    )
    return urlunparse(safe_parts)