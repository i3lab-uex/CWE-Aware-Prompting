import urllib.parse

# Domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "myapp.local",
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://myapp.com").
    callback_uri : str
        The relative or absolute path for the OAuth callback endpoint.
    session_state : str
        A unique value that will be added as a query parameter to prevent CSRF.

    Returns
    -------
    str
        The fully qualified callback URL including the state parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure root_url ends with a slash so urljoin behaves correctly
    if not root_url.endswith("/"):
        root_url += "/"

    # Join the base URL with the callback path
    joined = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(joined)

    # Validate that the hostname is in the allowed set
    hostname = parsed.hostname or ""
    if hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{hostname}' is not allowed")

    # Add the state parameter to the query string
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [session_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Rebuild the URL with the new query string
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