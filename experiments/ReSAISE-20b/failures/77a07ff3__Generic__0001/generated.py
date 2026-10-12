import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Pre‑approved external domains (add as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to detect suspicious patterns (e.g. IP addresses, subdomains not allowed)
DOMAIN_PATTERN = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")

def _normalize_domain(domain: str) -> str:
    """
    Normalise the domain by removing leading/trailing whitespace,
    converting to lowercase, and stripping any port.
    """
    domain = domain.strip().lower()
    # Remove port if present
    if ":" in domain:
        domain, _ = domain.split(":", 1)
    return domain

def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitise a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the domain is not in `APPROVED_DOMAINS` or the URL format is invalid.
    """
    if not isinstance(input_url, str) or not input_url.strip():
        raise ValueError("URL must be a non‑empty string")

    # Parse the URL; if scheme is missing, assume http
    parsed = urlparse(input_url.strip())
    if not parsed.scheme:
        # Prepend http:// to allow parsing of relative URLs
        parsed = urlparse("http://" + input_url.strip())

    # Ensure we have a network location
    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain")

    # Normalise and validate the domain
    domain = _normalize_domain(parsed.netloc)
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑construct a clean URL (scheme + domain + path/query/fragment)
    cleaned = ParseResult(
        scheme=parsed.scheme,
        netloc=domain,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment=parsed.fragment
    )
    return urlunparse(cleaned)