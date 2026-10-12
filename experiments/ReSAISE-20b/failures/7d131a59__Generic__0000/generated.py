import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a full OAuth callback URL and validate that it belongs to an allowed domain.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_path : str
        The path to be appended for the OAuth callback (e.g., "/auth/callback").
    state : str
        A unique, cryptographically random string to protect against CSRF.

    Returns
    -------
    str
        The fully-qualified callback URL, including the `state` query parameter.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise the base URL to avoid double slashes or missing scheme
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Ensure callback_path starts with a slash
    if not callback_path.startswith("/"):
        callback_path = "/" + callback_path

    # Combine base URL and callback path
    combined_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", callback_path.lstrip("/"))

    # Append the state query parameter
    url_parts = list(urllib.parse.urlparse(combined_url))
    query = urllib.parse.parse_qs(url_parts[4], keep_blank_values=True)
    query["state"] = [state]
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate domain
    netloc = urllib.parse.urlparse(final_url).netloc.split(":")[0].lower()
    if netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {netloc}")

    return final_url