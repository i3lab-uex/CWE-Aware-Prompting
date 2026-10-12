import urllib.parse
import idna

# Pre‑approved domains for redirection (example)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net"
}

def _normalize_domain(host: str) -> str:
    """
    Normalise a host name for comparison.
    Handles punycode conversion and lower‑casing.
    """
    try:
        # Convert Unicode domain to ASCII (Punycode)
        host_ascii = idna.encode(host).decode("ascii")
    except Exception:
        # If conversion fails, treat as invalid
        host_ascii = ""
    return host_ascii.lower()

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL and ensure it redirects only to
    pre‑approved domains. Returns the fully resolved, safe URL.
    
    Raises:
        ValueError: If the domain is not approved or the URL is malformed.
    """
    if not isinstance(url_input, str):
        raise ValueError("URL must be a string")

    # Parse the input URL
    parsed = urllib.parse.urlparse(url_input.strip())
    
    # Reject empty or relative URLs (e.g., "/path")
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and netloc")

    # Only allow http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Normalise and validate the domain
    host = _normalize_domain(parsed.hostname)
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct a clean URL (re‑encode path, query, fragment)
    safe_parts = (
        parsed.scheme,
        host,
        urllib.parse.quote(parsed.path, safe="/"),
        parsed.params,
        urllib.parse.quote_plus(parsed.query, safe="=&"),
        urllib.parse.quote(parsed.fragment, safe="/")
    )
    safe_url = urllib.parse.urlunparse(safe_parts)

    return safe_url