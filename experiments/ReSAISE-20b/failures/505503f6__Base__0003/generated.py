import re
from urllib.parse import urlparse, urlunparse, ParseResult

# A list of approved external domains (case‑insensitive).
# Add or remove domains as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regular expression to detect IP addresses (IPv4 & IPv6)
IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if the host string is an IP address."""
    return bool(IP_REGEX.match(host))


def _extract_domain(host: str) -> str:
    """
    Extract the registered domain (e.g. example.com) from a host.
    This is a very simple approach: split on dots and take the last two parts.
    For production code, consider using tldextract or a public suffix list.
    """
    parts = host.lower().split(".")
    if len(parts) < 2:
        return host.lower()
    # Handle cases like sub.example.co.uk -> example.co.uk
    return ".".join(parts[-2:])


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user‑provided URL and return it if it is safe for redirection.

    Parameters
    ----------
    input_link : str
        The URL provided by the user.

    Returns
    -------
    str
        A validated, safe‑to‑use URL suitable for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain or IP address.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    # Parse the URL. If parsing fails, raise an error.
    parsed = urlparse(input_link)

    # Reject relative URLs or missing scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Reject URLs that point to an IP address
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("Redirects to IP addresses are disallowed")

    # Extract the registered domain and check against approved list
    domain = _extract_domain(host)
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑assemble the URL to ensure it has no unsafe fragments
    safe_url = ParseResult(
        scheme=parsed.scheme.lower(),
        netloc=host,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment="",  # strip fragments
    ).geturl()

    return safe_url


# Example usage (uncomment to test):
# try:
#     print(validate_safe_redirect("https://example.com/path?query=1"))
# except ValueError as e:
#     print("Invalid redirect:", e)