import re
from urllib.parse import urlparse, urlunparse

# Whitelist of fully qualified domain names (FQDNs) that are considered safe for redirection.
# Subdomains of these domains are also allowed. Add or remove entries as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net"
}

# Regular expression to detect potentially dangerous schemes (e.g., javascript, data)
INVALID_SCHEMES = re.compile(r"^(javascript|data):", re.IGNORECASE)


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user-provided URL and ensure it points to an approved domain.

    Parameters
    ----------
    input_link : str
        The URL supplied by the user for redirection.

    Returns
    -------
    str
        A sanitized and safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL does not use an approved domain or contains a disallowed scheme.
    """
    if not input_link:
        raise ValueError("Empty URL provided")

    # Parse the URL. If scheme is missing, treat it as a relative path.
    parsed = urlparse(input_link)

    # Reject disallowed schemes
    if parsed.scheme and INVALID_SCHEMES.match(parsed.scheme):
        raise ValueError("Disallowed URL scheme")

    # If the URL is relative (no network location), consider it safe.
    if not parsed.netloc:
        # Ensure the path does not contain harmful fragments or query parameters
        # that could lead to XSS when rendered in a template.
        safe_path = re.sub(r"[<>&\"']", "", parsed.path)
        return urlunparse(("", "", safe_path, "", "", ""))

    # Normalise the domain: strip port and lower-case
    domain = parsed.netloc.split(":")[0].lower()

    # Allow the domain itself or any subdomain of an approved domain
    if not any(domain == ad or domain.endswith("." + ad) for ad in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL, preserving only safe components
    sanitized = parsed._replace(
        scheme="https" if parsed.scheme in ("http", "https") else parsed.scheme,
        path=re.sub(r"[<>&\"']", "", parsed.path),
    )
    return urlunparse(sanitized)