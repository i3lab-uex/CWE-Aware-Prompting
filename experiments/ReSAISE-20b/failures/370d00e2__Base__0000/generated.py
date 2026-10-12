import urllib.parse
from typing import Set

# Allowed domains for OAuth callback URLs. Update this set with legitimate domains.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    token_path : str
        The path where the OAuth provider should redirect (e.g., "/oauth/callback").
    session_state : str
        A state token used to validate the OAuth transaction.

    Returns
    -------
    str
        The fully constructed, validated callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to an untrusted domain or if the base URL is malformed.
    """
    # Parse the base URL to ensure it contains a scheme and netloc
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Join the path to the base URL
    joined = urllib.parse.urljoin(app_base_url, token_path)

    # Parse the resulting URL to inspect its domain
    parsed = urllib.parse.urlparse(joined)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Resulting URL is malformed: {joined!r}")

    # Ensure the domain is in the whitelist
    hostname = parsed.hostname
    if hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain {hostname!r} is not allowed for OAuth callbacks")

    # Build query string with the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    callback_url = parsed._replace(query=query).geturl()

    return callback_url