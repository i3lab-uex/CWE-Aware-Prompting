import re
from urllib.parse import urlparse, ParseResult

# Predefined allowed schemes and domains (example list)
ALLOWED_SCHEMES = {"http", "https"}
ALLOWED_DOMAINS  = {
    "example.com",
    "api.example.org",
    "localhost",          # allow localhost for dev
}

# Regular expression to extract domain part from netloc (handles optional port)
DOMAIN_RE = re.compile(r"^(?:[^@]+@)?(?P<host>[^:]+)(?::\d+)?$")

def _extract_domain(netloc: str) -> str:
    """
    Extract the host part from a netloc, ignoring userinfo and port.
    """
    match = DOMAIN_RE.match(netloc)
    if not match:
        raise ValueError(f"Invalid netloc: {netloc!r}")
    return match.group("host").lower()

def parse_url(url: str) -> ParseResult:
    """
    Parse a URL and validate that its scheme and host are allowed.

    Parameters
    ----------
    url : str
        The URL to be parsed.

    Returns
    -------
    urllib.parse.ParseResult
        The parsed URL object.

    Raises
    ------
    ValueError
        If the scheme or domain is not in the allowed sets.
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    parsed = urlparse(url)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    # Validate host
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    host = _extract_domain(parsed.netloc)

    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not allowed")

    # All checks passed; return the parsed URL
    return parsed

# Example usage (commented out)
# if __name__ == "__main__":
#     try:
#         p = parse_url("https://api.example.org/v1/resource")
#         print(p)
#     except ValueError as e:
#         print(f"URL validation failed: {e}")