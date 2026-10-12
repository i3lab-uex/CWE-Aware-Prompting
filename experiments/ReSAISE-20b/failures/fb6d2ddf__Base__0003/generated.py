import urllib.parse

# Example whitelist – in a real application this would be defined elsewhere.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build an SSO redirect URL that includes the user ID and a safe return URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint (e.g. "https://sso.example.com/auth").
    uid : str
        The unique identifier of the user.
    redirect_url : str
        Destination URL to which the user should be sent after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URL and extract its hostname
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    host = parsed_redirect.hostname or ""

    # Normalise the hostname for comparison (lowercase, strip leading/trailing dots)
    host = host.lower().strip(".")

    # Reject if the hostname is not in the whitelist
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Build the SSO query parameters
    sso_params = {
        "uid": uid,
        # Use a reserved parameter name (e.g., `return_to`) that the SSO provider expects
        "return_to": redirect_url,
    }

    # Parse the auth endpoint to preserve any existing query parameters
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Merge existing query params with new ones
    existing_params = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)
    # Convert list values to single strings (assuming one value per key)
    existing_params = {k: v[0] for k, v in existing_params.items()}
    merged_params = {**existing_params, **sso_params}

    # Reconstruct the URL
    new_query = urllib.parse.urlencode(merged_params, doseq=False)
    final_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        new_query,
        parsed_auth.fragment,
    )
    return urllib.parse.urlunparse(final_url_parts)