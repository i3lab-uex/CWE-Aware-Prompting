import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str,
                                session_token: str) -> str:
    """
    Build a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        The relative path that should handle the callback (e.g. "/oauth/callback").
    session_token : str
        A state token that will be added as a query parameter to prevent CSRF.

    Returns
    -------
    str
        The complete callback URL, e.g.
        "https://app.example.com/oauth/callback?state=XYZ".

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Join the root URL and callback path safely
    full_url = urllib.parse.urljoin(root_url.rstrip('/') + '/', path_for_callback.lstrip('/'))

    # Parse the resulting URL to extract its domain
    parsed = urllib.parse.urlparse(full_url)
    hostname = parsed.hostname

    if not hostname:
        raise ValueError("Callback URL does not contain a valid hostname")

    # Normalize the domain for comparison (lowercase, strip 'www.')
    normalized = hostname.lower()
    if normalized.startswith("www."):
        normalized = normalized[4:]

    # Ensure the domain is explicitly allowed
    if normalized not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{normalized}' is not authorized for OAuth callbacks")

    # Append the state token as a query parameter
    # Preserve any existing query parameters
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_token]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the URL with the updated query string
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return safe_url