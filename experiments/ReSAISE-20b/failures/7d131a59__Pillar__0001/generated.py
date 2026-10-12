import urllib.parse

# Example set of allowed callback domains.
# In a real application this should be configured securely.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.com"}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a full OAuth callback URL from the base application URL, a callback path,
    and an opaque state value. The resulting URL must resolve to a domain in
    ALLOWED_CALLBACK_DOMAINS; otherwise, ValueError is raised.

    Args:
        base_url: The application's base URL (e.g., "https://myapp.com").
        callback_path: Path to append for the OAuth callback (e.g., "/auth/callback").
        state: A unique opaque string to prevent CSRF attacks.

    Returns:
        The fully qualified OAuth callback URL.

    Raises:
        ValueError: If the resolved domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Normalize and combine base URL with callback path
    full_url = urllib.parse.urljoin(base_url.rstrip('/') + '/', callback_path.lstrip('/'))

    # Parse the resulting URL to extract components
    parsed = urllib.parse.urlparse(full_url)

    # Ensure a scheme is present; if missing, default to https
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc

    # If the URL was originally missing a scheme, prepend https
    if not parsed.scheme:
        full_url = f"{scheme}://{netloc}{parsed.path}"
        if parsed.query:
            full_url += f"?{parsed.query}"

    # Extract the domain part (exclude port)
    domain = netloc.split(':')[0]

    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain}")

    # Append the state parameter securely
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [state]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    final_url = urllib.parse.urlunparse((
        scheme,
        netloc,
        parsed.path,
        parsed.params,
        encoded_query,
        parsed.fragment
    ))

    return final_url