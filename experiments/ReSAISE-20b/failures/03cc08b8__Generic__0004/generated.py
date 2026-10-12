import urllib.parse

# Example set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here.
}


def assemble_oauth_callback(application_url: str, callback_route: str, token_state: str) -> str:
    """
    Assemble a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g., "https://app.example.com").
    callback_route : str
        The endpoint path for the OAuth callback handler (e.g., "/oauth/callback").
    token_state : str
        A unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL, including the `state` query parameter.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS and does not match
        the domain of `application_url`.
    """
    # Parse the base application URL.
    app_parsed = urllib.parse.urlparse(application_url)

    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError(f"Invalid application URL: {application_url!r}")

    # Ensure callback_route is relative and does not contain a scheme.
    if urllib.parse.urlparse(callback_route).scheme:
        raise ValueError(f"Callback route must be a relative path, got: {callback_route!r}")

    # Build the full callback URL.
    # Use urljoin to correctly handle slashes between base and route.
    full_url = urllib.parse.urljoin(application_url, callback_route)

    # Append the state query parameter.
    parsed = urllib.parse.urlparse(full_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = token_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the final URL.
    final_url_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment,
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    # Validate the domain of the callback URL.
    callback_domain = parsed.netloc.split(":")[0]  # strip port if present

    allowed_domains = ALLOWED_CALLBACK_DOMAINS
    app_domain = app_parsed.netloc.split(":")[0]

    if callback_domain not in allowed_domains and callback_domain != app_domain:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(allowed_domains)}; application domain: {app_domain}"
        )

    return final_url