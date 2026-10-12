import urllib.parse
from typing import Set

# Predefined set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def _extract_domain(url: str) -> str:
    """
    Extract the domain (netloc) from a URL, stripping any port.
    """
    parsed = urllib.parse.urlparse(url)
    host_port = parsed.netloc.lower()
    # Remove userinfo if present
    if "@" in host_port:
        host_port = host_port.split("@", 1)[-1]
    # Strip port
    return host_port.split(":", 1)[0]

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The callback endpoint, either a relative path (e.g., "/auth/callback")
        or an absolute URL.
    session_id : str
        A unique identifier used as a state parameter.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS and
        does not match the host application's domain.
    """
    if not host_url:
        raise ValueError("host_url must be a non-empty string")
    if not path_callback:
        raise ValueError("path_callback must be a non-empty string")
    if not session_id:
        raise ValueError("session_id must be a non-empty string")

    # Resolve the full callback URL
    if urllib.parse.urlparse(path_callback).scheme:
        # Absolute URL supplied – use as-is
        callback_url = path_callback
    else:
        # Relative path – join with host_url
        callback_url = urllib.parse.urljoin(host_url.rstrip("/") + "/", path_callback.lstrip("/"))

    # Validate domain
    host_domain = _extract_domain(host_url)
    callback_domain = _extract_domain(callback_url)

    if host_domain != callback_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Must be same as host or in ALLOWED_CALLBACK_DOMAINS."
        )

    # Append the state parameter
    parsed = urllib.parse.urlparse(callback_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    if "state" in query_params:
        raise ValueError("The callback URL already contains a 'state' parameter")
    query_params["state"] = session_id

    new_query = urllib.parse.urlencode(query_params)
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url