import urllib.parse

# Domains that are allowed to be redirected to even if they differ from the app's host.
APPROVED_DOMAINS = [
    "https://trusted.example.com",
    "https://secure.partner.org"
]


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    app_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    redirect_param : str
        User-provided path or full URL to redirect to.

    Returns
    -------
    str
        The final, fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the app's domain or an approved domain.
    """
    # Normalize base application URL
    base_parsed = urllib.parse.urlparse(app_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_url must be a valid absolute URL")

    # Resolve the redirect target against the base URL
    joined = urllib.parse.urljoin(app_url, redirect_param)
    target_parsed = urllib.parse.urlparse(joined)

    # Ensure the scheme is HTTP or HTTPS
    if target_parsed.scheme not in ("http", "https"):
        raise ValueError("Redirect scheme must be http or https")

    # If the redirect is relative, keep it within the app domain
    if not target_parsed.netloc:
        # Relative path: build absolute URL using the base
        final_url = urllib.parse.urlunparse(
            (base_parsed.scheme, base_parsed.netloc, target_parsed.path,
             target_parsed.params, target_parsed.query, target_parsed.fragment)
        )
    else:
        # Absolute URL: must be within app domain or an approved domain
        if target_parsed.netloc == base_parsed.netloc:
            final_url = joined  # safe internal redirect
        else:
            # Check against approved domains list (exact match or subdomain)
            allowed = False
            for domain in APPROVED_DOMAINS:
                approved_parsed = urllib.parse.urlparse(domain)
                if target_parsed.netloc == approved_parsed.netloc:
                    allowed = True
                    break
            if not allowed:
                raise ValueError("Redirect target is not within an approved domain")
            final_url = joined

    return final_url