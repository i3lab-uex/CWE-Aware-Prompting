import urllib.parse
from typing import Set

# Define the domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Generate a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    callback_path : str
        The path to the OAuth callback endpoint (e.g., "/oauth/callback").
    state : str
        A unique state string to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the domain of the resulting URL is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Build the absolute callback URL.
    # urljoin correctly handles trailing slashes and relative paths.
    full_url = urllib.parse.urljoin(base_url, callback_path)

    # Parse the URL to manipulate query parameters safely.
    parsed = urllib.parse.urlparse(full_url)

    # Append the state parameter to existing query parameters if any.
    query_params = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    query_params["state"] = state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the URL with the updated query string.
    safe_url = parsed._replace(query=new_query).geturl()

    # Validate the domain against allowed domains.
    domain = parsed.netloc.split(":")[0]  # strip port if present
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{domain}' is not allowed.")

    return safe_url