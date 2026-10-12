import urllib.parse

# Example list of allowed callback domains.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more trusted domains here.
}


def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL, e.g. "https://app.example.com".
    callback_uri : str
        The path for the OAuth callback endpoint. It must be a relative path
        starting with '/' or an absolute URL whose domain is whitelisted.
    session_state : str
        A unique value to include as the `state` query parameter.

    Returns
    -------
    str
        The fully-qualified callback URL with the `state` query parameter appended.

    Raises
    ------
    ValueError
        If the computed callback URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    if not isinstance(root_url, str) or not isinstance(callback_uri, str):
        raise TypeError("root_url and callback_uri must be strings")

    # If the callback URI is relative, join it with the root URL.
    if urllib.parse.urlparse(callback_uri).scheme == "":
        # Ensure it starts with a slash to avoid accidental path concatenation.
        if not callback_uri.startswith("/"):
            raise ValueError("callback_uri must be a relative path starting with '/'")
        full_url = urllib.parse.urljoin(root_url.rstrip("/") + "/", callback_uri.lstrip("/"))
    else:
        # Absolute URL – verify its domain is allowed.
        full_url = callback_uri

    parsed = urllib.parse.urlparse(full_url)

    # Extract the hostname (ignore port if present).
    host = parsed.hostname
    if host is None:
        raise ValueError("Invalid callback URL: missing hostname")

    # Domain check – allow exact match or subdomains of allowed domains.
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Callback domain '{host}' is not in the list of allowed domains")

    # Append or update the 'state' query parameter.
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query_params["state"] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL with the updated query string.
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return safe_url