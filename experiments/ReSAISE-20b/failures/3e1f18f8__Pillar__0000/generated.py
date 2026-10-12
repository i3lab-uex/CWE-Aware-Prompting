import urllib.parse
from typing import Set

# Allowed return domains (example values – replace with real ones)
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "trusted.example.org",
}

def _extract_domain(netloc: str) -> str:
    """
    Extract the domain part from a netloc, stripping any port.
    """
    return netloc.split(":")[0].lower()

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
        The base endpoint of the SSO service (e.g. "https://sso.example.com/auth").
    user_identifier : str
        The unique identifier of the user to be authenticated.
    redirect_uri : str
        The URL that the SSO provider should redirect back to after authentication.

    Returns
    -------
    str
        The fully constructed redirect URL, safe against open‑redirect attacks.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect_uri
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a fully qualified URL")

    domain = _extract_domain(parsed_redirect.netloc)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Parse the auth service endpoint
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)
    if not parsed_endpoint.scheme or not parsed_endpoint.netloc:
        raise ValueError("auth_service_endpoint must be a valid URL")

    # Build query parameters
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_uri
    }
    encoded_query = urllib.parse.urlencode(query_params)

    # Assemble the final URL
    new_url_parts = (
        parsed_endpoint.scheme,
        parsed_endpoint.netloc,
        parsed_endpoint.path or "",
        parsed_endpoint.params,
        encoded_query,
        parsed_endpoint.fragment
    )
    return urllib.parse.urlunparse(new_url_parts)