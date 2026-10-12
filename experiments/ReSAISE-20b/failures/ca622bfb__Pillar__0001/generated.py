import urllib.parse

# Example allowed domains; in real code this should be configured securely.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a full OAuth callback URL by joining the root URL with the provided path
    and appending a state parameter derived from ``session_token``.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_for_callback : str
        The relative path that handles OAuth callbacks (e.g., "/oauth/callback").
    session_token : str
        A token that will be passed as the ``state`` query parameter.

    Returns
    -------
    str
        The fully-qualified callback URL ready to be used in OAuth flows.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Construct the base callback URL.
    # ``urljoin`` handles leading/trailing slashes and normalizes the result.
    base_callback = urllib.parse.urljoin(root_url.rstrip('/') + '/', path_for_callback.lstrip('/'))

    # Parse the resulting URL to inspect its components.
    parsed = urllib.parse.urlparse(base_callback)

    # Verify the domain is allowed.
    if not parsed.netloc:
        raise ValueError("Callback URL does not contain a valid hostname.")
    if parsed.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not authorized for OAuth callbacks.")

    # Append the state parameter safely using urlencode.
    query_params = urllib.parse.parse_qs(parsed.query)
    # Preserve existing parameters if any; ``parse_qs`` returns list values.
    query_params["state"] = [session_token]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Rebuild the URL with the updated query string.
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        encoded_query,
        parsed.fragment
    ))

    return final_url