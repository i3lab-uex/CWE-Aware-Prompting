import urllib.parse

# Example allowed external domains (adjust as needed)
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.org",
    "cdn.safe-site.net"
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a secure redirect URL by appending `redirect_param` to
    `app_base_url`. The resulting URL is validated to ensure it points
    either within the base domain or to a whitelisted external domain.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        The path or full URL the user wishes to be redirected to after
        login. This may be a relative path ("/dashboard") or an absolute URL.

    Returns
    -------
    str
        The fully resolved redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the redirect URL resolves outside the base domain and is not in
        `ALLOWED_DOMAINS`, or if it cannot be parsed.
    """
    # Parse base URL once
    try:
        base_parsed = urllib.parse.urlparse(app_base_url)
    except Exception as exc:
        raise ValueError(f"Invalid base URL: {app_base_url}") from exc

    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Base URL must include scheme and domain: {app_base_url}")

    # Resolve redirect_param against base URL
    try:
        resolved = urllib.parse.urljoin(app_base_url, redirect_param)
    except Exception as exc:
        raise ValueError(f"Failed to resolve redirect param: {redirect_param}") from exc

    parsed = urllib.parse.urlparse(resolved)

    # Ensure the resolved URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Redirect URL must be absolute: {resolved}")

    # Check if the domain matches the base domain (subdomain allowed)
    def _is_subdomain(base: str, target: str) -> bool:
        return target == base or target.endswith("." + base)

    base_domain = base_parsed.netloc.lower()
    target_domain = parsed.netloc.lower()

    if _is_subdomain(base_domain, target_domain):
        # It's a relative or same‑site redirect – safe
        return resolved

    # Otherwise, it must be in the list of allowed external domains
    if target_domain not in [d.lower() for d in ALLOWED_DOMAINS]:
        raise ValueError(
            f"Redirect to domain '{target_domain}' is not allowed. "
            f"Allowed domains: {', '.join(ALLOWED_DOMAINS)}"
        )

    # Final safe redirect
    return resolved