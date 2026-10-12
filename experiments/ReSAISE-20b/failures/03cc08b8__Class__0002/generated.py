import urllib.parse
from typing import Set

# Predefined set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}

def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://myapp.com").
    callback_route : str
        The endpoint path for the OAuth callback handler (e.g. "/oauth/callback").
    token_state : str
        A unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with a state query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS
        and does not match the application's host.
    """
    # Ensure callback_route starts with a slash
    if not callback_route.startswith("/"):
        callback_route = "/" + callback_route

    # Resolve the full URL
    base_parsed = urllib.parse.urlparse(application_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid application_url: {application_url}")

    # Build the path by joining base URL with callback_route
    full_path = urllib.parse.urljoin(application_url.rstrip("/") + "/", callback_route.lstrip("/"))

    # Append the state parameter, ensuring it is URL‑encoded
    query_params = {"state": token_state}
    encoded_query = urllib.parse.urlencode(query_params)
    callback_url = f"{full_path}?{encoded_query}"

    # Validate the domain of the resulting URL
    callback_parsed = urllib.parse.urlparse(callback_url)
    host = callback_parsed.hostname or ""

    # If the host is not in the allowed list, enforce it matches the application domain
    if host.lower() not in ALLOWED_CALLBACK_DOMAINS and host.lower() != base_parsed.hostname.lower():
        raise ValueError(
            f"Disallowed callback domain '{host}'. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}. "
            f"Application domain: {base_parsed.hostname}"
        )

    return callback_url