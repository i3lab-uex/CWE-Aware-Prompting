import urllib.parse

# List of domains allowed for OAuth callbacks (example values)
ALLOWED_CALLBACK_DOMAINS = {
    "auth.example.com",
    "oauth.example.org",
    # Add other trusted domains here
}

def generate_oauth_callback_link(app_base_url: str,
                                 callback_endpoint: str,
                                 verification_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    callback_endpoint : str
        The relative or absolute path for the OAuth callback (e.g., "/oauth/callback").
    verification_state : str
        A unique string used to verify the OAuth request.

    Returns
    -------
    str
        The fully constructed callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in `ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the full callback URL
    full_url = urllib.parse.urljoin(app_base_url, callback_endpoint)

    # Parse the URL components
    parsed = urllib.parse.urlparse(full_url)

    # Extract domain (netloc without port) for validation
    domain = parsed.hostname or ""
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{domain}' is not allowed.")

    # Append the state parameter to existing query string
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # Flatten existing values and add state
    query_params["state"] = [verification_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    finalized = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return finalized