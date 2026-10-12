import urllib.parse

# Example set of allowed callback domains. In a real application this would be
# populated from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add any additional trusted domains here
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a full OAuth callback URL by combining the application's base URL,
    the callback endpoint path, and a state parameter.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    callback_endpoint : str
        The path component for the OAuth callback (e.g., "/oauth/callback").
    verification_state : str
        A unique value used to verify the integrity of the OAuth request flow.

    Returns
    -------
    str
        The fully qualified callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the computed callback URL is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the base URL has a trailing slash for correct urljoin behaviour
    base = app_base_url.rstrip("/") + "/"
    # Join the callback endpoint to the base URL
    full_path = urllib.parse.urljoin(base, callback_endpoint.lstrip("/"))

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(full_path)

    # Validate that the domain is allowed
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{hostname}' is not in the list of allowed domains."
        )

    # Append the state query parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [verification_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url