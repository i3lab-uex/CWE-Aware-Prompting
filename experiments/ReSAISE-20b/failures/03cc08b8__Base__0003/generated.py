import urllib.parse

# Example set of allowed domains – in real code this would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The endpoint path for the OAuth callback handler (e.g. "/auth/callback").
    token_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with a ``state`` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS`` or
        does not match the application host.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_app = urllib.parse.urlparse(application_url)
    if not parsed_app.scheme:
        raise ValueError("application_url must include a scheme (http:// or https://)")

    # Resolve the callback route against the base URL
    resolved = urllib.parse.urljoin(application_url, callback_route)

    # Parse the resulting URL to inspect its components
    parsed_callback = urllib.parse.urlparse(resolved)

    # Extract the hostname (domain) for validation
    callback_host = parsed_callback.hostname
    if not callback_host:
        raise ValueError("Callback URL must contain a valid hostname")

    # Validate that the callback host is either the same as the application
    # host or is explicitly allowed
    app_host = parsed_app.hostname
    if callback_host != app_host and callback_host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {callback_host!r}. "
            "Allowed domains are either the application host or entries in ALLOWED_CALLBACK_DOMAINS."
        )

    # Append the state parameter securely
    query_params = urllib.parse.parse_qs(parsed_callback.query)
    # Ensure we do not overwrite an existing state parameter
    if "state" in query_params:
        raise ValueError("Callback URL already contains a 'state' parameter")
    query_params["state"] = [token_state]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Rebuild the final URL
    final_url = urllib.parse.urlunparse((
        parsed_callback.scheme,
        parsed_callback.netloc,
        parsed_callback.path,
        parsed_callback.params,
        encoded_query,
        parsed_callback.fragment
    ))

    return final_url