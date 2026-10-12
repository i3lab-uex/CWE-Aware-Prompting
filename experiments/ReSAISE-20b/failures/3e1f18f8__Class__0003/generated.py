import urllib.parse
from typing import Set

# Example set of allowed domains for return URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add more domains as required.
}

def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        Base URL of the SSO service endpoint.
    user_identifier : str
        Unique identifier for the user.
    redirect_uri : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully formed redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_uri` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect_uri to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect_uri: must be a full URL with scheme and netloc")

    # Extract hostname (case‑insensitive comparison)
    host = parsed_redirect.hostname.lower()
    if host not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Redirect domain '{host}' is not allowed")

    # Encode query parameters
    encoded_user = urllib.parse.quote_plus(user_identifier, encoding="utf-8")
    encoded_redirect = urllib.parse.quote_plus(redirect_uri, encoding="utf-8")

    # Build the new query string
    new_query = f"user={encoded_user}&redirect_uri={encoded_redirect}"

    # Parse the auth service endpoint to merge any existing query components
    parsed_auth = urllib.parse.urlparse(auth_service_endpoint)
    # Merge with any existing query parameters
    if parsed_auth.query:
        merged_query = f"{parsed_auth.query}&{new_query}"
    else:
        merged_query = new_query

    # Reconstruct the final URL
    final_url_parts = parsed_auth._replace(query=merged_query)
    return urllib.parse.urlunparse(final_url_parts)

# Example usage:
if __name__ == "__main__":
    try:
        url = construct_sso_redirect(
            auth_service_endpoint="https://sso.example.com/auth",
            user_identifier="user123",
            redirect_uri="https://app.example.org/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")