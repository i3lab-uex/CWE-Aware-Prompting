import urllib.parse

# Whitelist of domains allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.local"
}


def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL for a given user and return destination.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider (e.g. "https://sso.example.com/login").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        Absolute URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        The fully assembled SSO redirect URL with all required query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    host = parsed_redirect.hostname

    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{host}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Ensure the auth_endpoint is a valid absolute URL.
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if not (parsed_auth.scheme and parsed_auth.netloc):
        raise ValueError(f"Invalid auth_endpoint URL: {auth_endpoint}")

    # Build the query parameters.
    params = {
        "uid": uid,
        "redirect_uri": redirect_url
    }

    # Encode parameters safely.
    encoded_params = urllib.parse.urlencode(params, safe=":/")

    # Construct the final SSO URL.
    sso_url = urllib.parse.urlunparse(
        (
            parsed_auth.scheme,
            parsed_auth.netloc,
            parsed_auth.path,
            parsed_auth.params,
            encoded_params,
            ""  # fragment
        )
    )

    return sso_url