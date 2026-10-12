import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "app.example.org",
    "auth.myservice.io"
}


def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    token_path : str
        The path that will handle the OAuth callback (e.g., "/auth/callback").
    session_state : str
        A CSRF‑protecting state value that must be included as a query parameter.

    Returns
    -------
    str
        The fully‑formed callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL is absolute
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Join the path to the base URL
    joined = urllib.parse.urljoin(app_base_url.rstrip("/") + "/", token_path.lstrip("/"))

    # Append the state query parameter
    url_parts = list(urllib.parse.urlparse(joined))
    # Preserve existing query parameters if any
    query = urllib.parse.parse_qs(url_parts[4], keep_blank_values=True)
    query["state"] = [session_state]
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate the domain against allowed list
    parsed_final = urllib.parse.urlparse(final_url)
    domain = parsed_final.hostname or ""
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not allowed for OAuth callbacks")

    return final_url