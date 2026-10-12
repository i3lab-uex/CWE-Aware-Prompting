import urllib.parse

# List of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add any additional domains here
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a fully-qualified OAuth redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The relative path to the OAuth callback endpoint (e.g. "/oauth/callback").
    token_state : str
        A unique state value to prevent CSRF attacks.

    Returns
    -------
    str
        The fully-qualified redirect URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the main URL has a scheme and netloc
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main URL: {main_url!r}")

    # Construct the base callback URL
    base_callback = urllib.parse.urljoin(main_url, redirect_path)

    # Append the state query parameter
    query = urllib.parse.urlencode({"state": token_state})
    full_url = f"{base_callback}?{query}"

    # Validate the domain of the resulting URL
    parsed_full = urllib.parse.urlparse(full_url)
    netloc = parsed_full.netloc.lower()

    # Remove port if present for comparison
    host = netloc.split(":")[0]

    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Callback URL host {host!r} is not in the list of allowed domains.")

    return full_url