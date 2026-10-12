import urllib.parse

# Predefined list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "cdn.example.net",
}

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_redirect_param : str
        The user‑supplied redirect target, which may be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or not in ALLOWED_DOMAINS.
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid base URL: {domain_base_url}")

    # Resolve the next redirect parameter against the base
    resolved = urllib.parse.urljoin(domain_base_url, next_redirect_param)
    parsed_resolved = urllib.parse.urlparse(resolved)

    # If the resolved URL is relative (no netloc), it stays within base domain
    if not parsed_resolved.netloc:
        # Ensure that the path does not escape using "../"
        safe_path = urllib.parse.urljoin("/", parsed_resolved.path)
        return urllib.parse.urlunparse(
            (base_parsed.scheme, base_parsed.netloc, safe_path,
             parsed_resolved.params, parsed_resolved.query, parsed_resolved.fragment)
        )

    # Absolute URL: ensure the domain is allowed
    netloc = parsed_resolved.netloc.split(":")[0]  # strip port if present
    if netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect domain '{netloc}' is not allowed")

    # Reconstruct the URL to avoid any manipulation
    return urllib.parse.urlunparse(parsed_resolved)