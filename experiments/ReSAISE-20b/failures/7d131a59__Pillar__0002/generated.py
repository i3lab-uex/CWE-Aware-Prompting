import urllib.parse

# Domains that are permitted for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add additional trusted domains here.
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_path : str
        The relative path to the OAuth callback endpoint (e.g., "/oauth/callback").
    state : str
        A unique opaque value used to mitigate CSRF attacks.

    Returns
    -------
    str
        The complete callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If the final URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # 1. Resolve the absolute callback URL
    #   - urljoin handles missing slashes and relative paths.
    resolved_url = urllib.parse.urljoin(base_url, callback_path)

    # 2. Append the state query parameter safely
    parsed = urllib.parse.urlparse(resolved_url)
    # Preserve existing query parameters if any.
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query_params["state"] = [state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # 3. Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # 4. Validate the domain
    final_domain = urllib.parse.urlparse(final_url).hostname
    if not final_domain or final_domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {final_domain}")

    return final_url