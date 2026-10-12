import urllib.parse as urlparse

# Domains that are considered safe for redirection (external)
SAFE_DOMAINS = [
    "example.com",
    "trusted-site.org",
    # Add more domains as needed
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a secure redirect URL after login.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_path : str
        The user-specified path or full URL to redirect to.

    Returns
    -------
    str
        The fully-qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an allowed external domain.
    """
    # Parse the primary URL
    base_parsed = urlparse.urlparse(primary_url)

    # If next_path is a full URL, parse it; otherwise treat as relative path
    next_parsed = urlparse.urlparse(next_path)

    # Build the final URL:
    if not next_parsed.scheme and not next_parsed.netloc:
        # relative path; join with base
        final_url = urlparse.urljoin(primary_url, next_path)
    else:
        # absolute URL; keep as is
        final_url = next_parsed.geturl()

    # Parse the resulting URL to inspect its components
    final_parsed = urlparse.urlparse(final_url)

    # Ensure the scheme is http or https
    if final_parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {final_parsed.scheme}")

    # Determine the domain to validate
    target_domain = final_parsed.netloc.lower()

    # Allowed domains are the base domain or any in SAFE_DOMAINS
    allowed_domains = {base_parsed.netloc.lower()}
    allowed_domains.update({d.lower() for d in SAFE_DOMAINS})

    if target_domain not in allowed_domains:
        raise ValueError(f"Redirect to disallowed domain: {target_domain}")

    return final_url