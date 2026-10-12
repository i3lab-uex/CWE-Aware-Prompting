import urllib.parse
from typing import Set

# Example allowed callback domains (should be defined elsewhere in the application)
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base application URL (e.g., "https://myapp.com").
    path_callback : str
        The relative path to the OAuth callback endpoint (e.g., "/oauth/callback").
    session_id : str
        A unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled, validated OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in ALLOWED_CALLBACK_DOMAINS and does not match
        the host_url's domain, preventing open‑redirect vulnerabilities.
    """
    if not path_callback.startswith("/"):
        raise ValueError("path_callback must be a relative path starting with '/'")

    # Parse the host URL to extract its components
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError("host_url must be a valid absolute URL")

    # Build the base callback URL
    base_callback = urllib.parse.urljoin(host_url, path_callback)

    # Ensure the resulting URL is still under the same host
    parsed_base = urllib.parse.urlparse(base_callback)
    if parsed_base.scheme != parsed_host.scheme:
        raise ValueError("Callback URL scheme mismatch")

    # Check domain: must be same as host or in ALLOWED_CALLBACK_DOMAINS
    callback_domain = parsed_base.hostname.lower() if parsed_base.hostname else ""
    host_domain = parsed_host.hostname.lower() if parsed_host.hostname else ""

    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{callback_domain}' is not allowed for OAuth callbacks")

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed_base.query)
    # Ensure no existing 'state' param is overwritten
    if "state" in query_params:
        raise ValueError("Callback URL already contains a 'state' parameter")
    query_params["state"] = [session_id]

    # Reconstruct the URL with updated query
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    safe_callback_url = parsed_base._replace(query=new_query).geturl()

    return safe_callback_url