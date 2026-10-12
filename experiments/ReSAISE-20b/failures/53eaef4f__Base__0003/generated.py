import urllib.parse

# Domains that are considered safe for redirection (e.g. third‑party OAuth providers)
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL from `next_path` relative to the application
    base URL `primary_url`.

    Parameters
    ----------
    primary_url : str
        Base application URL (e.g. "https://app.example.com")
    next_path : str
        User supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe URL that the user will be redirected to.

    Raises
    ------
    ValueError
        If `next_path` resolves outside the application domain or to an untrusted
        external domain.
    """
    # Parse primary URL once for reference
    base_parsed = urllib.parse.urlparse(primary_url)

    # Resolve next_path against the base URL
    resolved = urllib.parse.urljoin(primary_url, next_path)

    # Parse the resolved URL to inspect components
    parsed = urllib.parse.urlparse(resolved)

    # If the scheme is missing (relative path), re‑join to ensure full URL
    if not parsed.scheme:
        resolved = urllib.parse.urljoin(primary_url, next_path)
        parsed = urllib.parse.urlparse(resolved)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Check host against the primary domain or allowed safe domains
    host = parsed.hostname
    if not host:
        raise ValueError("Redirect URL must contain a hostname")

    # Normalize primary domain (strip www)
    def normalize(hostname: str) -> str:
        return hostname.lower().lstrip("www.")

    primary_domain = normalize(base_parsed.hostname)
    target_domain = normalize(host)

    # If the target domain is the same as primary or in SAFE_DOMAINS, allow
    if (
        target_domain == primary_domain
        or target_domain in {normalize(d) for d in SAFE_DOMAINS}
    ):
        return resolved

    # Otherwise, reject the redirect
    raise ValueError(
        f"Redirect to untrusted domain '{target_domain}' is not allowed"
    )