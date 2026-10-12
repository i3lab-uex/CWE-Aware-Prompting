import urllib.parse

# Example set of allowed domains – in real code this should be configurable.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net"
}


def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base SSO service endpoint (may already contain query parameters).
    uid : str
        Unique user identifier to be passed to the SSO service.
    redirect_url : str
        URL to return to after authentication. Must belong to an allowed domain.

    Returns
    -------
    str
        Fully constructed redirect URL with all required query parameters encoded.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    domain = parsed_redirect.hostname.lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect URL domain '{domain}' is not allowed")

    # Prepare query parameters
    # Preserve existing query params on the auth_endpoint
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    existing_params = dict(urllib.parse.parse_qsl(parsed_auth.query, keep_blank_values=True))

    # Add or override uid and redirect_uri
    existing_params.update({
        "uid": uid,
        # Use urlencode to properly escape the redirect URL
        "redirect_uri": redirect_url
    })

    # Reconstruct the auth_endpoint with updated query string
    new_query = urllib.parse.urlencode(existing_params, doseq=True)
    auth_url_parts = parsed_auth._replace(query=new_query)

    return urllib.parse.urlunparse(auth_url_parts)