import urllib.parse

# Define the set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "api.example.org",
    "auth.myapp.io",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The relative path to the OAuth callback endpoint (e.g., "/auth/callback").
    token_state : str
        A unique state value to protect against CSRF attacks.

    Returns
    -------
    str
        The complete OAuth callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure the base URL ends with a slash for correct urljoin behaviour
    if not main_url.endswith("/"):
        base = f"{main_url}/"
    else:
        base = main_url

    # Reject absolute URLs or URLs containing a scheme in redirect_path
    if urllib.parse.urlparse(redirect_path).scheme:
        raise ValueError("Redirect path must be a relative URL without scheme.")

    # Join base and redirect path safely
    callback_url = urllib.parse.urljoin(base, redirect_path)

    # Append the state parameter, ensuring it is URL‑encoded
    query = urllib.parse.urlencode({"state": token_state})
    callback_url_with_query = f"{callback_url}?{query}"

    # Validate that the domain of the resulting URL is allowed
    parsed = urllib.parse.urlparse(callback_url_with_query)
    domain = parsed.hostname

    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{domain}' is not allowed.")

    return callback_url_with_query