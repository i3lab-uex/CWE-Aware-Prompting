import urllib.parse

# Domains that are explicitly allowed for redirects outside the app's own domain.
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URI for post‑login navigation.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_path : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application’s domain or an allowed external domain.
    """
    # Parse the primary URL once to extract its components
    base = urllib.parse.urlparse(primary_url)

    # Resolve the next_path relative to the primary URL
    resolved = urllib.parse.urljoin(primary_url, next_path)
    parsed_resolved = urllib.parse.urlparse(resolved)

    # If the resolved URL has a scheme (i.e., is absolute)
    if parsed_resolved.scheme in ("http", "https"):
        # If the netloc matches the primary host or is in SAFE_DOMAINS, it's allowed
        if parsed_resolved.netloc == base.netloc or any(
            parsed_resolved.netloc.endswith(domain) for domain in SAFE_DOMAINS
        ):
            return resolved

    # If the resolved URL is relative (no scheme), it's automatically safe
    if not parsed_resolved.scheme:
        return resolved

    # Any other case is disallowed
    raise ValueError(
        f"Redirect URL '{resolved}' is not allowed. "
        f"Allowed domains: {base.netloc} and {', '.join(SAFE_DOMAINS)}."
    )