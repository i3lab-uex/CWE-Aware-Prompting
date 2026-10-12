import urllib.parse

# Example allowed domains – replace with the real list for your application.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here.
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a full OAuth callback URL and validate that its domain is allowed.

    Parameters
    ----------
    app_base_url : str
        The application's main base URL (e.g., "https://app.example.com").
    callback_endpoint : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    verification_state : str
        A unique value used to protect against CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure base and endpoint are properly joined
    full_url = urllib.parse.urljoin(app_base_url.rstrip('/') + '/', callback_endpoint.lstrip('/'))

    # Append the state parameter securely
    parsed = urllib.parse.urlparse(full_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params['state'] = verification_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the URL with the updated query string
    final_url = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
    )

    # Validate the domain (netloc) against allowed domains
    hostname = parsed.hostname  # e.g., "app.example.com"
    if hostname is None:
        raise ValueError("Callback URL does not contain a valid hostname.")

    # Allow subdomains of the trusted domains
    def is_allowed(host):
        for allowed in ALLOWED_CALLBACK_DOMAINS:
            if host == allowed or host.endswith("." + allowed):
                return True
        return False

    if not is_allowed(hostname.lower()):
        raise ValueError(f"Disallowed callback domain: {hostname}")

    return final_url