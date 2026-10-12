import urllib.parse

# Example set of allowed domains; replace with real values in production.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (must include scheme, e.g., "https://app.example.com").
    callback_path : str
        The path component for the OAuth callback (must start with '/').
    state : str
        A unique state string used for CSRF protection.

    Returns
    -------
    str
        The fully-qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Basic validation of inputs
    if not base_url:
        raise ValueError("base_url must be a non-empty string")
    if not callback_path.startswith("/"):
        raise ValueError("callback_path must start with '/'")

    # Join base URL and path safely
    joined = urllib.parse.urljoin(base_url.rstrip("/") + "/", callback_path.lstrip("/"))

    # Append state query parameter
    parsed = urllib.parse.urlparse(joined)
    qs = dict(urllib.parse.parse_qsl(parsed.query))
    qs["state"] = state
    new_query = urllib.parse.urlencode(qs)
    rebuilt = parsed._replace(query=new_query)

    # Validate domain
    domain = rebuilt.netloc.split(":")[0]  # ignore port if present
    if domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Callback domain '{domain}' is not allowed")

    return urllib.parse.urlunparse(rebuilt)