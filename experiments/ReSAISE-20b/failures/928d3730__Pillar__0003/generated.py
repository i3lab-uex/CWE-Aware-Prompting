import urllib.parse
from typing import Set

# Example allowed domains; in a real application this should be configured securely.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.myapp.org"}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g. "https://myapp.com").
    path_callback : str
        The callback endpoint (e.g. "/auth/callback").
    session_id : str
        A unique identifier to be sent as the OAuth `state` parameter.

    Returns
    -------
    str
        A fully assembled callback URL containing the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is neither in ALLOWED_CALLBACK_DOMAINS
        nor identical to the host_url's domain.
    """
    # Ensure we have a proper base URL and path
    base = host_url.rstrip("/")
    callback_path = urllib.parse.urljoin(base + "/", path_callback.lstrip("/"))

    # Parse the constructed URL to extract components
    parsed = urllib.parse.urlparse(callback_path)

    # Determine the domain of the callback URL
    callback_domain = parsed.hostname

    if not callback_domain:
        raise ValueError("Callback URL does not contain a valid hostname.")

    # Extract the host domain from the original host_url for same‑domain comparison
    host_parsed = urllib.parse.urlparse(host_url)
    host_domain = host_parsed.hostname

    # Verify domain is allowed
    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {ALLOWED_CALLBACK_DOMAINS}"
        )

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_id]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the URL with updated query
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return safe_url