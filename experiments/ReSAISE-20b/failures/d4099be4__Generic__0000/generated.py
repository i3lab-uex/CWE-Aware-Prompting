import urllib.parse

# Define the set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add any additional trusted domains here.
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g. "https://myapp.com").
    callback_endpoint : str
        The path to the OAuth callback endpoint (e.g. "/auth/callback").
    verification_state : str
        A unique value used to protect against CSRF attacks.

    Returns
    -------
    str
        The final callback URL, e.g.
        "https://myapp.com/auth/callback?state=xyz".

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Build the absolute URL for the callback endpoint
    base = app_base_url.rstrip("/")
    endpoint = callback_endpoint.lstrip("/")
    url_without_query = urllib.parse.urljoin(base + "/", endpoint)

    # Append the state query parameter safely
    parsed = urllib.parse.urlparse(url_without_query)
    qs = dict(urllib.parse.parse_qsl(parsed.query))
    qs["state"] = verification_state
    new_query = urllib.parse.urlencode(qs)

    full_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    # Validate the domain against the allowed list
    domain = urllib.parse.urlparse(full_url).hostname or ""
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {domain!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return full_url