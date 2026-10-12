import urllib.parse

# Domains that are allowed to receive the OAuth callback.
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
        The application's base URL (e.g., "https://app.example.com").
    callback_path : str
        The relative path that handles the OAuth callback (e.g., "/auth/callback").
    state : str
        A unique, unguessable string used to maintain state between request and callback.

    Returns
    -------
    str
        The fully qualified OAuth callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL is parsed correctly.
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Join the callback path to the base URL.
    joined = urllib.parse.urljoin(parsed_base.geturl(), callback_path)

    # Append the state query parameter safely.
    query = urllib.parse.urlencode({"state": state})
    callback_url = f"{joined}?{query}"

    # Validate that the domain is allowed.
    parsed_callback = urllib.parse.urlparse(callback_url)
    callback_domain = parsed_callback.hostname
    if not callback_domain or callback_domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {callback_domain!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return callback_url