import urllib.parse

# Example whitelist – replace with your actual allowed domains.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net",
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint URL (may already contain query parameters).
    user_identifier : str
        Unique identifier for the user.
    redirect_link : str
        URL to which the SSO provider should return after authentication.

    Returns
    -------
    str
        Fully constructed SSO redirect URL with validated return link.

    Raises
    ------
    ValueError
        If the `redirect_link` is not a valid absolute URL or its domain
        is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect link and validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be a valid absolute URL")

    # Extract the hostname (without port) and compare against the whitelist
    domain = parsed_redirect.hostname or ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_link domain '{domain}' is not allowed")

    # Parse the base SSO URI to preserve existing components
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Merge existing query parameters with the new ones
    qs = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    qs["user"] = [user_identifier]
    qs["redirect"] = [redirect_link]

    # Reconstruct the full URL
    new_query = urllib.parse.urlencode(qs, doseq=True)
    constructed_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return constructed_url