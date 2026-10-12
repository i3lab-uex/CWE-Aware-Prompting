import urllib.parse
from typing import Set

# Example set of allowed domains. In a real application this would be configured elsewhere.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "trusted.org"}

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
        Base URL of the SSO service (e.g., "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g., a UUID or username).
    redirect_uri : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        A fully-formed redirect URL safe for use in an HTTP redirect.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URI domain to prevent open redirects
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a full, absolute URL")

    # Extract the domain part (netloc) and normalize it
    redirect_domain = parsed_redirect.netloc.lower()
    # Strip port if present
    redirect_domain = redirect_domain.split(":")[0]

    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{redirect_domain}' is not allowed")

    # Build query parameters, ensuring proper percent‑encoding
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_uri
    }
    encoded_query = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    # Combine the base endpoint with the query string
    # Use urljoin to correctly handle trailing slashes in the endpoint
    base = urllib.parse.urlparse(auth_service_endpoint)
    if not base.scheme or not base.netloc:
        raise ValueError("auth_service_endpoint must be a full, absolute URL")

    # Ensure the endpoint ends with a slash or has no path
    if not base.path.endswith("/"):
        endpoint = auth_service_endpoint.rstrip("/") + "/"
    else:
        endpoint = auth_service_endpoint

    final_url = f"{endpoint}?{encoded_query}"
    return final_url