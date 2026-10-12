import urllib.parse
from typing import Set

# Example set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g. "https://myapp.com").
    path_callback : str
        The endpoint for the OAuth callback handler (e.g. "/auth/callback").
    session_id : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS or
        does not match the host_url domain.
    """
    # Normalise the host URL and ensure it has a scheme
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme:
        raise ValueError("host_url must include a scheme (http or https)")

    # Build the callback URL by safely joining the host and path
    # urljoin handles leading/trailing slashes correctly.
    callback_url = urllib.parse.urljoin(host_url.rstrip("/") + "/", path_callback.lstrip("/"))

    # Parse the callback URL to extract components
    parsed_cb = urllib.parse.urlparse(callback_url)

    # Validate the scheme: only http or https are allowed
    if parsed_cb.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_cb.scheme}' in callback URL")

    # Validate the domain
    host_domain = parsed_host.hostname.lower()
    cb_domain = parsed_cb.hostname.lower()

    # Allow the callback if it is either:
    # 1. Exactly the same domain as host_url, or
    # 2. In the predefined ALLOWED_CALLBACK_DOMAINS set.
    if cb_domain != host_domain and cb_domain not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Callback domain '{cb_domain}' is not allowed")

    # Append the state parameter securely
    query_params = urllib.parse.parse_qs(parsed_cb.query)
    # Preserve existing parameters; do not overwrite if 'state' already exists
    if "state" in query_params:
        raise ValueError("Callback URL must not contain an existing 'state' parameter")
    query_params["state"] = [session_id]

    # Reconstruct the URL with updated query
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    final_url_parts = (
        parsed_cb.scheme,
        parsed_cb.netloc,
        parsed_cb.path,
        parsed_cb.params,
        new_query,
        parsed_cb.fragment,
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url