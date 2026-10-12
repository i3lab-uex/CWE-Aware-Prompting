import urllib.parse

# Domains that are allowed for the return URL.  Add your own domains here.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO service endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully-formed redirect URL.

    Raises
    ------
    ValueError
        If the return URL's domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the return URL domain
    parsed_return = urllib.parse.urlparse(redirect_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Normalize the host (strip port)
    host = parsed_return.hostname.lower()
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Build query parameters for the SSO request
    query_params = {
        "uid": uid,
        "redirect_uri": redirect_url,  # encode the full URL
    }

    # Parse the auth endpoint to preserve existing query params
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Merge any existing query parameters from the auth endpoint
    existing_params = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)
    # Flatten parse_qs output
    merged_params = {k: v[0] for k, v in existing_params.items()}
    merged_params.update(query_params)

    # Construct the final URL
    new_query = urllib.parse.urlencode(merged_params)
    final_url = urllib.parse.urlunparse(
        (
            parsed_auth.scheme,
            parsed_auth.netloc,
            parsed_auth.path,
            parsed_auth.params,
            new_query,
            parsed_auth.fragment,
        )
    )

    return final_url