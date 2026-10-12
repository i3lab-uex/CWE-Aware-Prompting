import urllib.parse

# Predefined set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed
}


def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Generate a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g., "https://myapp.com").
    path_callback : str
        The relative endpoint for the OAuth callback handler (e.g., "/auth/callback").
    session_id : str
        A unique identifier for the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL domain is not allowed or does not match the host domain.
    """
    # Validate that path_callback is a relative path
    if not path_callback.startswith("/"):
        raise ValueError("path_callback must be a relative path starting with '/'")

    # Parse the host URL to extract its components
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError("host_url must be a valid absolute URL")

    # Build the full callback URL
    full_callback = urllib.parse.urljoin(host_url, path_callback)

    # Parse the resulting callback URL
    parsed_callback = urllib.parse.urlparse(full_callback)
    callback_netloc = parsed_callback.netloc.lower()

    # Determine the host domain (strip subdomains if necessary)
    host_domain = parsed_host.netloc.lower()

    # If the callback domain is different, ensure it is in ALLOWED_CALLBACK_DOMAINS
    if callback_netloc != host_domain:
        # Extract the effective top-level domain (eTLD+1) for comparison
        # Simple split on last two parts; for production, use tldextract
        def get_etld_plus_one(domain: str) -> str:
            parts = domain.split(".")
            return ".".join(parts[-2:]) if len(parts) >= 2 else domain

        callback_etld = get_etld_plus_one(callback_netloc)
        host_etld = get_etld_plus_one(host_domain)

        if callback_etld not in ALLOWED_CALLBACK_DOMAINS and host_etld not in ALLOWED_CALLBACK_DOMAINS:
            raise ValueError(
                f"Callback domain '{callback_netloc}' is not allowed "
                f"(host domain: '{host_domain}')"
            )

    # Append the state parameter
    query_params = urllib.parse.parse_qs(parsed_callback.query)
    query_params["state"] = [session_id]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_callback.scheme,
            parsed_callback.netloc,
            parsed_callback.path,
            parsed_callback.params,
            new_query,
            parsed_callback.fragment,
        )
    )

    return final_url