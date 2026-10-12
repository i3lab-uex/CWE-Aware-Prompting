import urllib.parse

# Domains that are permitted to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here.
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_path : str
        The path to the OAuth callback endpoint (e.g., "/auth/oauth/callback").
    state : str
        A unique opaque value used to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully-qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resolved callback URL does not belong to an allowed domain.
    """
    # Parse and normalise the base URL.
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url must be a valid absolute URL")

    # Ensure the callback path is relative and does not contain a scheme or netloc.
    if urllib.parse.urlparse(callback_path).scheme:
        raise ValueError("callback_path must be a relative path, not an absolute URL")

    # Join the base and callback paths safely.
    joined_path = urllib.parse.urljoin(parsed_base.path or "/", callback_path)

    # Reconstruct the full URL without a query component yet.
    base_without_query = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            joined_path,
            "",  # params
            "",  # query (to be added)
            "",  # fragment
        )
    )

    # Append the state parameter.
    callback_url = f"{base_without_query}?state={urllib.parse.quote(state, safe='')}"

    # Verify the domain is allowed.
    parsed_callback = urllib.parse.urlparse(callback_url)
    if not parsed_callback.netloc.lower() in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{parsed_callback.netloc}' is not allowed")

    return callback_url