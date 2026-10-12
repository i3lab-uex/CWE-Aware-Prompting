import urllib.parse

# Example set of allowed callback domains – replace with your own.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback_url(root_url: str,
                                path_for_callback: str,
                                session_token: str) -> str:
    """
    Build a fully‑qualified OAuth callback URL that includes the state
    parameter and guarantees that the resulting host is within the set of
    allowed callback domains.

    Parameters
    ----------
    root_url : str
        Base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        Path that will be appended to the base URL (e.g. "/auth/callback").
    session_token : str
        Token to embed as the `state` query parameter.

    Returns
    -------
    str
        The complete callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the root URL contains a scheme; otherwise urljoin behaves
    # unexpectedly.  Default to https if missing.
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        root_url = "https://" + root_url
        parsed_root = urllib.parse.urlparse(root_url)

    # Join the base URL with the callback path.
    full_path = urllib.parse.urljoin(root_url.rstrip('/') + '/', path_for_callback.lstrip('/'))

    # Append the state query parameter.
    url_parts = list(urllib.parse.urlparse(full_path))
    query = urllib.parse.parse_qs(url_parts[4])
    query['state'] = [session_token]
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate the host is allowed.
    domain = urllib.parse.urlparse(final_url).hostname
    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain!r}")

    return final_url