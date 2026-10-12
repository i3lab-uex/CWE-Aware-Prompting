import urllib.parse

# Whitelisted domains that the redirect URL is allowed to point to.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "mydomain.net",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL.
    uid : str
        Unique user identifier to be sent to the identity provider.
    redirect_url : str
        The URL that the user should be redirected back to after SSO.

    Returns
    -------
    str
        The fully constructed SSO redirect URL with query parameters.
    
    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URL to extract its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    # Normalise the hostname (lowercase) for comparison
    redirect_domain = parsed_redirect.hostname.lower() if parsed_redirect.hostname else ""
    
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{redirect_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )
    
    # Build the query parameters
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,  # Pass the full URL; it will be percent‑encoded
    }
    
    # Construct the final URL
    # Use urllib.parse.urljoin to correctly handle relative paths in sso_path.
    base_url = urllib.parse.urljoin(sso_path, "")
    full_query = urllib.parse.urlencode(query_params)
    final_url = f"{base_url}?{full_query}"
    
    return final_url