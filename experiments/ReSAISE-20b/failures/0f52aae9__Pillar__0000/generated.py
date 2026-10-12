import urllib.parse

# A set of domains that are explicitly allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",          # for local testing
}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The relative or absolute endpoint that handles the OAuth callback
        (e.g., "/auth/callback").
    session_state : str
        A unique identifier that ties the request to a user session.

    Returns
    -------
    str
        The fully qualified callback URL with the state parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS` or does not match the domain of
        ``main_url``.
    """
    # Normalise and resolve the redirect endpoint against the main URL
    resolved = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Parse the resulting URL to extract components
    parsed = urllib.parse.urlparse(resolved)

    # Ensure we have a scheme and network location
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid callback URL derived from main_url='{main_url}' "
                         f"and redirect_endpoint='{redirect_endpoint}': {resolved}")

    # Check that the domain is allowed
    hostname = parsed.hostname.lower()
    if not (hostname in ALLOWED_CALLBACK_DOMAINS or hostname == urllib.parse.urlparse(main_url).hostname.lower()):
        raise ValueError(f"Callback domain '{hostname}' is not allowed for OAuth redirects.")

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
    )

    return final_url