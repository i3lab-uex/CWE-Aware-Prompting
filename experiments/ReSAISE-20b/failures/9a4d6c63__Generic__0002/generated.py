import re
from urllib.parse import urlparse, ParseResult

# Predefined allowed schemes and domains
ALLOWED_SCHEMES = {"http", "https"}
ALLOWED_DOMAINS = {
    "example.com",
    "api.example.org",
    "localhost",  # allow localhost for local testing
}

# Regular expression to validate a hostname (RFC 1035)
HOSTNAME_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.[A-Za-z0-9-]{1,63})*$"
)

def _is_valid_hostname(hostname: str) -> bool:
    """Check if the hostname is a valid domain name."""
    return HOSTNAME_REGEX.match(hostname) is not None

def parse_url(url: str) -> ParseResult:
    """
    Parse and validate a URL.

    Parameters
    ----------
    url : str
        The URL to be parsed and validated.

    Returns
    -------
    urllib.parse.ParseResult
        A fully parsed URL object.

    Raises
    ------
    ValueError
        If the scheme is not in ALLOWED_SCHEMES, or if the hostname does
        not match a known allowed domain or is malformed.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(
            f"Unsupported scheme '{parsed.scheme}'. "
            f"Allowed schemes: {', '.join(ALLOWED_SCHEMES)}"
        )

    # Validate host
    hostname = parsed.hostname or ""
    if not _is_valid_hostname(hostname):
        raise ValueError(f"Invalid hostname '{hostname}'")

    # Check if host is in allowed domains or ends with an allowed domain
    if hostname not in ALLOWED_DOMAINS:
        # allow subdomains of the allowed domains
        if not any(hostname.endswith("." + domain) for domain in ALLOWED_DOMAINS):
            raise ValueError(
                f"Hostname '{hostname}' is not in the list of allowed domains: "
                f"{', '.join(ALLOWED_DOMAINS)}"
            )

    # Return the parsed URL object (ParseResult is immutable)
    return parsed