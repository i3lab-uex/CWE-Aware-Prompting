import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved external domains (add or remove as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe.example.net"
}

# Regular expression to validate a basic URL structure
_URL_RE = re.compile(
    r"^(?P<scheme>https?)://(?P<netloc>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE
)

def process_url_redirect(input_url: str) -> str:
    """
    Validate a user supplied URL and return a safe, fully‑qualified redirect URL.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A validated and safe redirect URL that uses http or https.

    Raises
    ------
    ValueError
        If the input URL is malformed, has an unsupported scheme,
        or its domain is not in ``APPROVED_DOMAINS``.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    match = _URL_RE.match(input_url.strip())
    if not match:
        raise ValueError("Malformed URL")

    scheme = match.group("scheme").lower()
    netloc = match.group("netloc")
    path = match.group("path") or ""

    # Normalize the domain: strip port, convert to lower case
    domain = netloc.split(":")[0].lower()

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑construct the URL to ensure it has a consistent format
    safe_url = urlunparse((scheme, netloc, path, "", "", ""))
    return safe_url