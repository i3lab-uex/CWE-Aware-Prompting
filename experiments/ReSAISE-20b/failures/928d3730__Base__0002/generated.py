import urllib.parse

# Set of domains that are allowed to be used as OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}


def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The relative or absolute callback endpoint (e.g., "/auth/callback").
    session_id : str
        A unique identifier to preserve state across the OAuth flow.

    Returns
    -------
    str
        The fully-qualified, signed callback URL including the state parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL points to an untrusted domain.
    """
    # Resolve the final callback URL
    resolved_url = urllib.parse.urljoin(host_url, path_callback)

    # Parse the resolved URL to inspect its components
    parsed = urllib.parse.urlparse(resolved_url)

    # Reject URLs without a scheme or host
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Callback URL must include a scheme and host")

    # Ensure the callback domain is either:
    #   1) The same as the host_url's domain, or
    #   2) Listed in ALLOWED_CALLBACK_DOMAINS.
    host_domain = urllib.parse.urlparse(host_url).hostname
    callback_domain = parsed.hostname

    if (
        host_domain is None
        or callback_domain is None
        or (callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS)
    ):
        raise ValueError(f"Disallowed callback domain: {callback_domain}")

    # Build the query string with a state parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_id]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the URL with the new query string
    final_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment,
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url