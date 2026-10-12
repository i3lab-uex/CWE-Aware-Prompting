import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # add more trusted domains here
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a full OAuth callback URL and verify that it points to an allowed domain.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_path : str
        The path component for the OAuth callback (must start with '/').
    state : str
        A unique string used to maintain state between the request and callback.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL with the `state` query parameter appended.

    Raises
    ------
    ValueError
        If `callback_path` is not a relative path or if the resulting URL's domain is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`. This protects against CWE‑610 by preventing redirects
        to untrusted domains.
    """
    # Ensure the callback path is relative and begins with a slash
    if not isinstance(callback_path, str) or not callback_path.startswith("/"):
        raise ValueError("callback_path must be a relative path starting with '/'")

    # Combine base URL and callback path
    combined = urllib.parse.urljoin(base_url, callback_path)

    # Parse the URL components
    parsed = urllib.parse.urlparse(combined)

    # Verify that the host is allowed
    if parsed.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{parsed.hostname}' is not allowed")

    # Append the state query parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [state]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=encoded_query)
    )

    return final_url