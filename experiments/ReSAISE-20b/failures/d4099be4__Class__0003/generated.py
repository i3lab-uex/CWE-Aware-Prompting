import urllib.parse

# A set of domains that are considered safe for OAuth callback URLs.
# In a real application, this should be defined in configuration and
# never modified by user input.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str,
) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's main base URL, e.g. "https://myapp.example.com".
    callback_endpoint : str
        The path to the OAuth callback endpoint, e.g. "/auth/callback".
    verification_state : str
        A unique value to be included as the `state` query parameter.

    Returns
    -------
    str
        A fully-qualified URL that points to the callback endpoint and
        includes the state parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL has a scheme; otherwise urljoin will treat it as relative.
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme:
        raise ValueError("app_base_url must include a scheme (http:// or https://)")

    # Join the base URL with the callback endpoint.
    joined_url = urllib.parse.urljoin(app_base_url, callback_endpoint)

    # Append the state query parameter.
    url_parts = list(urllib.parse.urlparse(joined_url))
    # Parse existing query parameters and add the state.
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query["state"] = verification_state
    url_parts[4] = urllib.parse.urlencode(query)
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate that the domain is allowed.
    final_parsed = urllib.parse.urlparse(final_url)
    host = final_parsed.hostname
    if not host or host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {host}")

    return final_url