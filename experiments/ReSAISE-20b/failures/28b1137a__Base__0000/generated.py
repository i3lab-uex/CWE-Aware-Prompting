import urllib.parse

# Whitelist of domains that are allowed to receive the redirect after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.local",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        Base URL of the SSO endpoint (e.g. "https://sso.example.com/auth").
    uid : str
        Unique user identifier to be passed to the SSO provider.
    redirect_url : str
        URL that the user should return to after authentication.

    Returns
    -------
    str
        A fully formed SSO redirect URL that includes the UID and a
        percent‑encoded `redirect` query parameter.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the return URL to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect URL")

    # Normalize the domain (lowercase) and strip port if present
    netloc = parsed_redirect.netloc.split(':')[0].lower()
    if netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{netloc}' is not allowed")

    # Build query parameters for the SSO endpoint
    sso_query = {
        "uid": uid,
        # Pass the original redirect URL as a query param
        "redirect": redirect_url,
    }

    # Combine the base SSO path with the query string
    sso_parsed = urllib.parse.urlparse(sso_path)
    # Preserve any existing query parameters in the base SSO path
    existing_params = urllib.parse.parse_qs(sso_parsed.query)
    # Merge with new parameters (new params override existing ones if keys clash)
    merged_params = {**{k: v[0] for k, v in existing_params.items()}, **sso_query}
    query_string = urllib.parse.urlencode(merged_params)

    # Reconstruct the full URL
    sso_url = urllib.parse.urlunparse((
        sso_parsed.scheme,
        sso_parsed.netloc,
        sso_parsed.path,
        sso_parsed.params,
        query_string,
        sso_parsed.fragment,
    ))

    return sso_url