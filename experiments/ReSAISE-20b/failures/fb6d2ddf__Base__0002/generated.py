import urllib.parse

# Whitelisted domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.com",
    "trusted.org",
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base SSO endpoint (e.g. "https://sso.example.com/auth").
    uid : str
        Unique user identifier.
    redirect_url : str
        Destination URL to return to after authentication.

    Returns
    -------
    str
        Fully constructed SSO redirect URL with query parameters.
    
    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL and extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL")

    # Normalize the domain: lower‑case and strip port if present.
    netloc = parsed_redirect.netloc.split(":")[0].lower()

    if netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Unapproved return domain: {netloc}")

    # Build the query string safely.
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,  # will be percent‑encoded by urlencode
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Assemble the final URL.
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Preserve any existing query params in auth_endpoint.
    if parsed_auth.query:
        final_query = f"{parsed_auth.query}&{encoded_query}"
    else:
        final_query = encoded_query

    final_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        final_query,
        parsed_auth.fragment,
    )
    return urllib.parse.urlunparse(final_url_parts)