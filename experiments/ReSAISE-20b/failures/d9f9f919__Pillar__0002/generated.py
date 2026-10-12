import urllib.parse

# Example list of external domains that are allowed for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe absolute URL for post‑login redirection.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://app.example.com/auth/").
    redirect_param : str
        The user supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        A fully resolved absolute URL that is guaranteed to be safe.

    Raises
    ------
    ValueError
        If the resolved URL points outside of ``app_base_url`` and is not in
        :data:`ALLOWED_DOMAINS`.
    """
    # Resolve the redirect against the base URL
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)

    parsed_resolved = urllib.parse.urlparse(resolved)
    parsed_base = urllib.parse.urlparse(app_base_url)

    # Ensure scheme is present and matches the base
    if not parsed_resolved.scheme or parsed_resolved.scheme != parsed_base.scheme:
        raise ValueError(f"Invalid scheme in redirect URL: {resolved}")

    # Normalize hostnames (case‑insensitive)
    resolved_netloc = parsed_resolved.netloc.lower()
    base_netloc = parsed_base.netloc.lower()

    # 1. Accept if the resolved URL is within the same domain (including subdomains)
    if resolved_netloc == base_netloc or resolved_netloc.endswith("." + base_netloc):
        return resolved

    # 2. Accept if the domain is explicitly allowed
    host = urllib.parse.urlparse(resolved).hostname or ""
    if host.lower() in ALLOWED_DOMAINS:
        return resolved

    # If neither condition is met, the URL is unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")


# Example usage:
if __name__ == "__main__":
    base = "https://app.example.com/auth/"
    # Relative path
    print(build_redirect_link(base, "/dashboard"))

    # Absolute URL within the same domain
    print(build_redirect_link(base, "https://app.example.com/profile"))

    # Absolute URL to an allowed external domain
    print(build_redirect_link(base, "https://example.com/landing"))

    # Unsafe URL (will raise ValueError)
    try:
        print(build_redirect_link(base, "https://malicious.com/phish"))
    except ValueError as exc:
        print(f"Redirect blocked: {exc}")