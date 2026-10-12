import urllib.parse

# Domains that are considered safe for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "myapp.local",
    "auth.mycompany.org",
}

def generate_oauth_callback_link(app_base_url: str,
                                 callback_endpoint: str,
                                 verification_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_endpoint : str
        The specific path for the OAuth callback endpoint (e.g., "/auth/callback").
    verification_state : str
        A unique value used to verify the integrity of the OAuth request.

    Returns
    -------
    str
        The fully-qualified callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the callback endpoint starts with a slash so urljoin behaves predictably.
    if not callback_endpoint.startswith("/"):
        callback_endpoint = "/" + callback_endpoint

    # Build the absolute URL.
    raw_url = urllib.parse.urljoin(app_base_url.rstrip("/") + "/", callback_endpoint.lstrip("/"))

    # Parse the URL to inspect its components.
    parsed = urllib.parse.urlparse(raw_url)

    # Validate the domain against the whitelist.
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {hostname}")

    # Append the state query parameter.
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [verification_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL with the updated query string.
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return final_url