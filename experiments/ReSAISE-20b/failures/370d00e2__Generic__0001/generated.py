import urllib.parse

# Domains that are permitted to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (must include scheme).
    token_path : str
        Path component that will be appended to the base URL.
    session_state : str
        State string used for CSRF protection.

    Returns
    -------
    str
        Fully qualified OAuth callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If `app_base_url` is missing a scheme, or the resulting domain
        is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Parse the base URL and ensure it contains a scheme.
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Verify that the domain is allowed.
    if parsed_base.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Domain {parsed_base.hostname!r} is not allowed for OAuth callbacks"
        )

    # Join the base URL with the token path, normalizing slashes.
    callback_path = urllib.parse.urljoin(parsed_base.path + "/", token_path.lstrip("/"))

    # Construct the full URL with query parameters.
    query = urllib.parse.urlencode({"state": session_state})
    full_url_parts = parsed_base._replace(path=callback_path, query=query)
    return urllib.parse.urlunparse(full_url_parts)

# Example usage (uncomment to test):
# print(generate_oauth_token_url(
#     "https://example.com", "/oauth/callback", "abc123"
# ))