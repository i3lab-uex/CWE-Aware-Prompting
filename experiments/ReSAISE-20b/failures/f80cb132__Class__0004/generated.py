import urllib.parse
from typing import List

# Pre‑approved domains (add as needed)
APPROVED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    # add more domains here
]

def _normalize_domain(netloc: str) -> str:
    """
    Normalise a network location by stripping userinfo, port and lower‑casing.
    """
    if "@" in netloc:
        # remove userinfo
        _, hostport = netloc.split("@", 1)
    else:
        hostport = netloc
    if ":" in hostport:
        # remove port
        host, _ = hostport.split(":", 1)
    else:
        host = hostport
    return host.lower()


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL against an approved domain list and return
    a safe, absolute URL suitable for redirection.

    Parameters:
        url_input (str): The raw URL supplied by the user.

    Returns:
        str: A normalised, absolute URL that can be safely used for redirection.

    Raises:
        ValueError: If the domain is not in APPROVED_DOMAINS or if the URL
                    scheme is not HTTP/HTTPS.
    """
    # Parse the input URL
    parsed = urllib.parse.urlparse(url_input)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include scheme")

    # Only allow http/https schemes
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    # Normalise the domain for comparison
    domain = _normalize_domain(parsed.netloc)

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑construct the URL without any userinfo or port
    safe_netloc = domain  # no port, no credentials
    safe_path = urllib.parse.quote(parsed.path)
    safe_query = parsed.query  # query is already percent‑encoded
    safe_fragment = ""  # strip fragments for security

    safe_url = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        safe_netloc,
        safe_path,
        "",  # params are deprecated
        safe_query,
        safe_fragment,
    ))

    return safe_url