import re
from urllib.parse import urlparse, ParseResult

# Predefined allowed protocols and domains
ALLOWED_SCHEMES = {"http", "https", "ftp"}
ALLOWED_DOMAINS = {
    "example.com",
    "api.example.org",
    "trusted-site.net",
}

# Regular expression to extract the domain part (without port)
DOMAIN_RE = re.compile(r"^(?P<domain>[^:]+)(?::\d+)?$")


def _extract_domain(netloc: str) -> str:
    """
    Extract the domain from a netloc string, ignoring any port number.
    Raises ValueError if the netloc is empty or malformed.
    """
    match = DOMAIN_RE.match(netloc)
    if not match:
        raise ValueError(f"Invalid netloc: {netloc!r}")
    return match.group("domain").lower()


def parse_url(url: str) -> ParseResult:
    """
    Parse a URL and validate its scheme and domain against predefined
    allowed lists.

    Parameters:
        url (str): The URL to parse.

    Returns:
        urllib.parse.ParseResult: The parsed URL object.

    Raises:
        ValueError: If the scheme is not allowed or the domain is not in
                    ALLOWED_DOMAINS.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)

    # Validate scheme
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (e.g., http, https)")
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    # Validate domain
    if not parsed.netloc:
        raise ValueError("URL must include a network location (domain)")
    domain = _extract_domain(parsed.netloc)

    if domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not allowed")

    # All checks passed; return the parsed result
    return parsed