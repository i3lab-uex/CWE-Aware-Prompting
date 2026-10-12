import urllib.parse
from typing import Set

# Example set of allowed callback domains; in a real application this would be configured elsewhere
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The callback endpoint path (e.g., "/auth/callback").
    session_id : str
        A unique identifier used as the OAuth state parameter.

    Returns
    -------
    str
        The fully assembled OAuth callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in ALLOWED_CALLBACK_DOMAINS and does not
        match the host domain.
    """
    # Ensure path_callback starts with a slash
    if not path_callback.startswith("/"):
        path_callback = "/" + path_callback

    # Parse the host URL to extract its components
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError("Invalid host_url: missing scheme or network location")

    # Resolve the full callback URL by joining host and path
    callback_url = urllib.parse.urljoin(host_url, path_callback)

    # Parse the resulting URL to inspect its domain
    parsed_callback = urllib.parse.urlparse(callback_url)
    callback_domain = parsed_callback.hostname

    if not callback_domain:
        raise ValueError("Callback URL does not contain a valid hostname")

    # Validate domain: must be either the same as host or in ALLOWED_CALLBACK_DOMAINS
    if callback_domain != parsed_host.hostname and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter securely
    query = urllib.parse.urlencode({"state": session_id})
    full_url = urllib.parse.urlunparse(
        (
            parsed_callback.scheme,
            parsed_callback.netloc,
            parsed_callback.path,
            parsed_callback.params,
            query,
            parsed_callback.fragment,
        )
    )

    return full_url