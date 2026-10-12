import urllib.parse

# Domains that are considered safe for external redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com/").
    next_param : str
        The user‑supplied target path or absolute URL.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain that is neither the same as
        `base_url` nor in :data:`ALLOWED_DOMAINS`.
    """
    # Resolve the next_param against the base URL.
    resolved_url = urllib.parse.urljoin(base_url, next_param)

    # Parse the resolved URL to inspect its components.
    parsed = urllib.parse.urlparse(resolved_url)

    # Extract the domain (netloc) and scheme.
    target_netloc = parsed.netloc.lower()
    target_scheme = parsed.scheme.lower()

    # Parse the base URL to get its domain for comparison.
    base_parsed = urllib.parse.urlparse(base_url)
    base_netloc = base_parsed.netloc.lower()

    # The redirect is allowed if:
    # 1. It uses the same domain as the base URL, or
    # 2. Its domain is in ALLOWED_DOMAINS.
    #
    # We also require that the scheme be HTTP/HTTPS to avoid
    # redirecting to file://, data:, etc.
    if target_scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {target_scheme}")

    if target_netloc == base_netloc:
        # Same‑origin redirect: safe.
        return resolved_url

    if target_netloc in {d.lower() for d in ALLOWED_DOMAINS}:
        # External but explicitly allowed domain.
        return resolved_url

    # If we reach here, the target is not safe.
    raise ValueError(
        f"Redirect to untrusted domain '{target_netloc}' is not allowed."
    )