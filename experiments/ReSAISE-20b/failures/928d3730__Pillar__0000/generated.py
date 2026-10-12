import urllib.parse

# Predefined set of domains allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more allowed domains here.
}


def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The relative endpoint for the OAuth callback handler (e.g., "/auth/callback").
    session_id : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled, validated OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback domain is not in ALLOWED_CALLBACK_DOMAINS and does not match
        the host's domain.
    """
    # Resolve the full callback URL by joining host and path components
    callback_url = urllib.parse.urljoin(host_url.rstrip("/") + "/", path_callback.lstrip("/"))

    # Parse the resulting URL to inspect components
    parsed = urllib.parse.urlparse(callback_url)

    # Reject URLs without a scheme or netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid callback URL: missing scheme or domain")

    # Extract the hostname for validation
    callback_host = parsed.hostname
    if not callback_host:
        raise ValueError("Invalid callback URL: hostname could not be determined")

    # Determine the host domain (without subdomains) for comparison
    def _root_domain(host: str) -> str:
        parts = host.split(".")
        return ".".join(parts[-2:]) if len(parts) >= 2 else host

    host_root = _root_domain(parsed.hostname)
    allowed = any(callback_host == domain or callback_host.endswith("." + domain) for domain in ALLOWED_CALLBACK_DOMAINS)

    # Ensure the callback URL is either on an allowed domain or matches the host domain
    if not (allowed or _root_domain(host_url) == host_root):
        raise ValueError(f"Callback domain '{callback_host}' is not allowed")

    # Append the state parameter securely
    query = dict(urllib.parse.parse_qsl(parsed.query))
    query["state"] = session_id
    new_query = urllib.parse.urlencode(query)

    # Reconstruct the final URL
    final_url = parsed._replace(query=new_query).geturl()
    return final_url