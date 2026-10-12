import urllib.parse

# Domains that are explicitly allowed for redirects even if they are not the primary domain
SAFE_DOMAINS = ["example.com", "trustedpartner.org"]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Construct a safe redirect URL based on the user supplied `next_path`.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_path : str
        The path or full URL the user wishes to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside of `primary_url`'s domain or any
        domain listed in ``SAFE_DOMAINS``.
    """
    # Parse the primary base URL
    base_parsed = urllib.parse.urlparse(primary_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("primary_url must be a fully qualified URL")

    # Resolve next_path relative to the base
    resolved = urllib.parse.urljoin(primary_url, next_path)

    # Parse the resolved URL to validate
    target_parsed = urllib.parse.urlparse(resolved)

    # Ensure the scheme is HTTP(S) only
    if target_parsed.scheme not in ("http", "https"):
        raise ValueError("Redirect scheme must be http or https")

    # Normalise host to lower case for comparison
    target_host = target_parsed.hostname.lower() if target_parsed.hostname else ""

    # Allow the primary domain or any of the SAFE_DOMAINS
    allowed_domains = {base_parsed.hostname.lower()}
    allowed_domains.update(domain.lower() for domain in SAFE_DOMAINS)

    if target_host not in allowed_domains:
        raise ValueError(f"Redirect to untrusted domain: {target_host}")

    # Return the fully qualified redirect URL
    return resolved