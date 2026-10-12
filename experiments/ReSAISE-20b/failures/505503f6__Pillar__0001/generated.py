import re
from urllib.parse import urlparse, urlunparse

# Whitelist of approved domains (add or remove as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.io",
}

# Regular expression to validate a hostname (basic RFC 1123)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _is_approved_domain(hostname: str) -> bool:
    """
    Return True if the hostname is exactly one of the approved domains
    or a sub‑domain of an approved domain.
    """
    hostname = hostname.lower()
    if not HOSTNAME_RE.match(hostname):
        return False

    # Exact match
    if hostname in APPROVED_DOMAINS:
        return True

    # Sub‑domain check: only allow if the suffix matches an approved domain
    for domain in APPROVED_DOMAINS:
        if hostname.endswith("." + domain):
            return True
    return False


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that the supplied URL is safe for redirection.

    Parameters
    ----------
    input_link : str
        The user supplied URL to redirect to.

    Returns
    -------
    str
        A validated, safe‑to‑use URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL does not use an allowed scheme, is malformed,
        or its domain is not in the approved list.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_link)

    # Enforce http or https scheme
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure the netloc (host[:port]) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Separate hostname and optional port
    hostname, _, port = parsed.netloc.partition(":")
    if not _is_approved_domain(hostname):
        raise ValueError(f"Domain {hostname!r} is not approved for redirects")

    # Re‑build the URL to normalise it (e.g., strip default ports)
    netloc = hostname
    if port:
        # Only keep non‑default ports
        if (parsed.scheme == "http" and port != "80") or (
            parsed.scheme == "https" and port != "443"
        ):
            netloc = f"{hostname}:{port}"
    safe_url = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return safe_url