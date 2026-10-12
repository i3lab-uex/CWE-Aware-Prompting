import urllib.parse
from typing import Set

# Example set of allowed domains; replace with your actual configuration.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "app.example.org"}

def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO service.
    user_identifier : str
        Unique identifier for the user.
    redirect_uri : str
        The URL to return to after authentication.

    Returns
    -------
    str
        A fully-formed redirect URL suitable for use in a 302 response.

    Raises
    ------
    ValueError
        If the domain of `redirect_uri` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URI to validate its domain.
    parsed = urllib.parse.urlparse(redirect_uri)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid redirect URI: missing scheme or netloc")

    # Normalize domain for comparison (lowercase, no port).
    host = parsed.hostname
    if host is None:
        raise ValueError("Redirect URI must contain a hostname")

    # Strip port if present for comparison
    host = host.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{host}' is not allowed")

    # Encode the redirect_uri as a query parameter value.
    encoded_redirect = urllib.parse.quote(redirect_uri, safe="")

    # Build query parameters safely.
    query_params = urllib.parse.urlencode(
        {
            "user": user_identifier,
            "redirect_uri": redirect_uri,  # urlencode will encode it again
        }
    )

    # Construct the final URL.
    base = urllib.parse.urljoin(auth_service_endpoint.rstrip("/") + "/", "")
    return f"{base}?{query_params}"