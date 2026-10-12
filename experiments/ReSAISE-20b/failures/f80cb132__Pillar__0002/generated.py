import re
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Pre‑approved external domains (exact matches or subdomains)
# ------------------------------------------------------------------
APPROVED_DOMAINS = [
    "example.com",
    "trusted.org",
    "secure.net",
]

# Regular expression to match a host that ends with an approved domain
APPROVED_DOMAIN_RE = re.compile(
    r"^(?:(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+)?"
    r"(" + "|".join(re.escape(d) for d in APPROVED_DOMAINS) + r")$",
    re.IGNORECASE,
)

def _is_approved_domain(host: str) -> bool:
    """
    Return True if the host is exactly an approved domain or a sub‑domain of one.
    """
    return bool(APPROVED_DOMAIN_RE.match(host))

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL and return a safe, fully qualified redirect URL.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A validated and safe‑to‑use URL for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not approved.
    """
    if not isinstance(url_input, str):
        raise ValueError("URL must be a string")

    # Parse the input URL
    parsed = urlparse(url_input.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    # Only allow http/https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalise the host (lowercase, strip trailing dot)
    host = parsed.hostname.lower().rstrip(".")
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to avoid any surprises (e.g., missing path)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))

    return safe_url

# ------------------------------------------------------------------
# Example usage
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print(secure_user_redirect("https://sub.example.com/page?x=1"))
    except ValueError as e:
        print(f"Redirect blocked: {e}")