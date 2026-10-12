import urllib.parse
from typing import Set

# Example allowed domains; replace with real values in production.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "app.example.org"}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        The URL to which users should be returned after authentication.

    Returns
    -------
    str
        A fully formed redirect URL that can be sent to the client.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to validate its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect URL: {redirect_url}")

    # Extract the hostname for domain comparison.
    host = parsed_redirect.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Build query parameters safely.
    params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }
    encoded_params = urllib.parse.urlencode(params, safe="/")

    # Ensure auth_endpoint has no existing query string.
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if parsed_auth.query:
        raise ValueError("auth_endpoint should not contain a query string")

    # Construct the final URL.
    redirect_parts = parsed_auth._replace(query=encoded_params)
    return urllib.parse.urlunparse(redirect_parts)

# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.example.com/auth"
    user_id = "user123"
    return_url = "https://app.example.org/dashboard"

    try:
        full_redirect = build_sso_redirect(endpoint, user_id, return_url)
        print(full_redirect)
    except ValueError as e:
        print(f"Error: {e}")