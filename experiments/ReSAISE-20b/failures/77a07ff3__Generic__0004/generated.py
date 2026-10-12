import re
from urllib.parse import urlparse, urlunparse

# List of fully qualified domains that are allowed for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net"
}

# Regular expression to extract the hostname (without port) from a netloc
_NETLOC_RE = re.compile(r"^(?P<host>[^:]+)(?::(?P<port>\d+))?$")


def _normalize_host(hostname: str) -> str:
    """
    Normalize hostname to lowercase for comparison.
    """
    return hostname.lower()


def _is_allowed_domain(hostname: str) -> bool:
    """
    Return True if the hostname is an exact match or a subdomain of one
    of the ALLOWED_DOMAINS.
    """
    host = _normalize_host(hostname)
    for allowed in ALLOWED_DOMAINS:
        if host == allowed or host.endswith("." + allowed):
            return True
    return False


def process_url_redirect(input_url: str) -> str:
    """
    Validate a user‑supplied URL and ensure it redirects only to an approved domain.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        A safe, normalized URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or points to a disallowed domain.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host and optional port
    match = _NETLOC_RE.match(parsed.netloc)
    if not match:
        raise ValueError("Malformed netloc in URL")

    host = match.group("host")
    port = match.group("port")

    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of approved domains")

    # Reconstruct a clean URL: keep scheme, host, port (if present), path,
    # query, and fragment. Normalize path to avoid directory traversal.
    safe_netloc = host
    if port:
        safe_netloc += f":{port}"

    # Avoid relative paths that could lead to path traversal
    safe_path = re.sub(r"//+", "/", parsed.path)

    sanitized = urlunparse(
        (
            parsed.scheme,
            safe_netloc,
            safe_path,
            "",  # params are deprecated
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized