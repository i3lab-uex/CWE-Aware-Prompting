import urllib.parse
from typing import Set

# Example set of allowed callback domains; in real code this would be configured elsewhere
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "myapp.org"}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The endpoint for the OAuth callback handler (e.g., "/auth/callback").
    session_id : str
        A unique identifier used as the OAuth state parameter.

    Returns
    -------
    str
        The fully assembled callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the callback URL's domain is not allowed or does not match the host domain.
    """
    # Resolve the full callback URL
    base_parsed = urllib.parse.urlparse(host_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid host_url: {host_url}")

    # Ensure the path starts with a slash
    if not path_callback.startswith("/"):
        path_callback = "/" + path_callback

    # Join host URL with the callback path
    full_url = urllib.parse.urljoin(host_url.rstrip("/") + "/", path_callback.lstrip("/"))
    callback_parsed = urllib.parse.urlparse(full_url)

    # Validate domain
    host_domain = base_parsed.hostname.lower()
    callback_domain = callback_parsed.hostname.lower() if callback_parsed.hostname else ""

    # Domain must be same as host or in the allowed list
    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)} or same as host."
        )

    # Append the state parameter
    query = urllib.parse.parse_qs(callback_parsed.query)
    query["state"] = [session_id]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL
    final_parsed = callback_parsed._replace(query=new_query)
    return urllib.parse.urlunparse(final_parsed)


# Example usage (commented out):
# if __name__ == "__main__":
#     url = generate_oauth_url(
#         host_url="https://app.example.com",
#         path_callback="/oauth/callback",
#         session_id="abc123"
#     )
#     print(url)