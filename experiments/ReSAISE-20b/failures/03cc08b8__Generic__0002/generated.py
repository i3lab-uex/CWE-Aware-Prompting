import urllib.parse

# Example set of allowed callback domains.  In a real application this would be
# populated from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The path or endpoint that handles the OAuth callback (e.g.
        "/auth/callback").
    token_state : str
        A unique identifier used to maintain state between the request and
        callback.

    Returns
    -------
    str
        A fully assembled OAuth callback URL that includes the `state`
        query parameter.

    Raises
    ------
    ValueError
        If the domain of the resulting URL is not the same as the
        application_url's domain and is not present in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Parse the base application URL and ensure it has a scheme
    parsed_app = urllib.parse.urlparse(application_url)
    if not parsed_app.scheme:
        raise ValueError("Application URL must include a scheme (http or https)")

    # Resolve the callback route relative to the application URL
    full_path = urllib.parse.urljoin(application_url, callback_route)

    # Append the state query parameter
    parsed_callback = urllib.parse.urlparse(full_path)
    query_params = dict(urllib.parse.parse_qsl(parsed_callback.query))
    query_params["state"] = token_state
    new_query = urllib.parse.urlencode(query_params)

    # Rebuild the full URL with the updated query string
    assembled_url = urllib.parse.urlunparse(
        (
            parsed_callback.scheme,
            parsed_callback.netloc,
            parsed_callback.path,
            parsed_callback.params,
            new_query,
            parsed_callback.fragment,
        )
    )

    # Validate the domain
    callback_domain = urllib.parse.urlparse(assembled_url).hostname
    if not callback_domain:
        raise ValueError("Failed to extract hostname from the assembled URL")

    # Allow same domain or domains explicitly whitelisted
    app_domain = parsed_app.hostname
    if callback_domain != app_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            "Allowed domains: same as application or those in ALLOWED_CALLBACK_DOMAINS."
        )

    return assembled_url