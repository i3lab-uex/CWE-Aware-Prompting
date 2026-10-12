import urllib.parse

# Whitelist of allowed return URL domains.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted.site.net",
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that forwards the user to an external identity provider.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint URL.
    uid : str
        The unique user identifier to be passed to the identity provider.
    redirect_url : str
        URL that the user should be returned to after successful authentication.

    Returns
    -------
    str
        The fully formed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if parsed_redirect.netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect URL domain '{parsed_redirect.netloc}' is not allowed."
        )

    # Prepare query parameters
    params = {
        "uid": uid,
        "redirect_url": redirect_url,  # keep the full URL as a parameter
    }

    # Parse the auth endpoint and merge existing query parameters (if any)
    parsed_auth = urllib.parse.urlparse(auth_endpoint)

    # Convert existing query parameters to a mutable dict
    existing_qs = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)

    # Update/insert our parameters (parse_qs returns lists)
    for key, value in params.items():
        existing_qs[key] = [value]

    # Reconstruct the query string
    new_query = urllib.parse.urlencode(existing_qs, doseq=True)

    # Build the final URL
    new_parsed = parsed_auth._replace(query=new_query)
    return urllib.parse.urlunparse(new_parsed)