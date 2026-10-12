import re
from urllib.parse import urlparse, urlunparse

# Approved API hosts – keep this list up‑to‑date
APPROVED_HOSTS = {
    "api.example.com",
    "api.google.com",
    "api.github.com",
}

# Regex to detect private IP ranges and localhost
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(                                   # start of string
        (?:localhost|127\.0\.0\.1) |      # localhost and loopback
        10(?:\.\d{1,3}){3} |             # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2} |  # 172.16.0.0/12
        192\.168(?:\.\d{1,3}){2} |       # 192.168.0.0/16
        169\.254(?:\.\d{1,3}){2} |       # link‑local
        ::1$                              # IPv6 loopback
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def verify_api_link(url_to_check: str) -> str:
    """
    Verify that the supplied URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated, canonicalised URL.

    Raises
    ------
    ValueError
        If the URL is not HTTP/HTTPS, resolves to an internal address,
        or does not belong to one of the approved hosts.
    """
    # Parse the URL
    parsed = urlparse(url_to_check)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Reject private or localhost IPs
    if PRIVATE_IP_REGEX.match(host):
        raise ValueError("URL points to a private or loopback address.")

    # Reject hosts that are not in the approved list
    if host.lower() not in APPROVED_HOSTS:
        raise ValueError(f"Host '{host}' is not an approved API domain.")

    # Re‑assemble the URL to ensure it is canonicalised
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        parsed.fragment,
    ))

    return cleaned