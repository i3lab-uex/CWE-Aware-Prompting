import urllib.parse
import idna

# Predefined safe domains (ASCII form, case‑insensitive)
SAFE_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local",
}

def _canonical_domain(netloc: str) -> str:
    """
    Convert a network location part to its canonical ASCII form.
    Handles IDN (punycode) and removes port numbers.
    """
    # Strip userinfo if present
    if "@" in netloc:
        _, host_port = netloc.rsplit("@", 1)
    else:
        host_port = netloc

    # Separate port
    if ":" in host_port:
        host, _port = host_port.split(":", 1)
    else:
        host = host_port

    # Convert Unicode domain to punycode
    return idna.encode(host).decode("ascii").lower()

def process_user_redirect(input_url: str) -> str:
    """
    Accept a user supplied URL and return it only if its domain is in the
    whitelist. The function normalises the URL to avoid subtle open‑redirect
    attacks and raises ValueError otherwise.

    Args:
        input_url (str): The URL supplied by the user.

    Returns:
        str: A fully qualified, safe URL that can be used for redirection.

    Raises:
        ValueError: If the domain is not in SAFE_DOMAINS or if the URL
                    scheme is missing/unsupported.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(input_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and host")

    # Only allow http/https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Canonicalise the domain
    domain = _canonical_domain(parsed.netloc)

    if domain not in SAFE_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for redirection")

    # Reconstruct the URL to ensure it is fully qualified and normalized
    safe_url = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url