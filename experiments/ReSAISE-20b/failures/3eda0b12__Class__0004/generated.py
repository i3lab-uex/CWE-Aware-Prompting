import re
from urllib.parse import urlparse, urljoin

# Domains that are considered safe for external redirects
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    target_param : str
        The URL path or full URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified redirect URL that is guaranteed to stay within the
        application domain or one of the permitted external domains.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain that is not the application
        itself or an allowed external domain.
    """
    # Normalize main_url to avoid double slashes and trailing spaces
    base = main_url.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", base):
        raise ValueError("main_url must be a valid absolute URL")

    # Resolve the target relative to the base
    resolved = urljoin(base, target_param)

    parsed_resolved = urlparse(resolved)
    parsed_base = urlparse(base)

    # 1. If the resolved URL is a relative path, prepend base
    if not parsed_resolved.scheme:
        # This should never happen because urljoin will always produce a scheme
        resolved = base.rstrip("/") + "/" + target_param.lstrip("/")
        parsed_resolved = urlparse(resolved)

    # 2. Ensure the resolved URL stays within the application or permitted domains
    if parsed_resolved.netloc == parsed_base.netloc:
        # Same host: safe
        return resolved

    # Check if the domain is in the whitelist of permitted external domains
    host = parsed_resolved.hostname or ""
    if host.lower() in {d.lower() for d in PERMITTED_DOMAINS}:
        return resolved

    # If none of the above, reject
    raise ValueError(
        f"Redirect target '{resolved}' is not allowed: "
        f"domain '{host}' is outside the permitted scope."
    )