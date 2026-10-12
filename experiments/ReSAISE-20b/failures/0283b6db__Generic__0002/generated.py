import urllib.parse
from typing import Set

# Domains that are allowed to be used as return URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.org",
    # Add more domains as needed
}


def _is_allowed_return_url(return_url: str) -> bool:
    """
    Verify that the return URL's domain is in ALLOWED_RETURN_DOMAINS.
    """
    parsed = urllib.parse.urlparse(return_url)
    # Reject URLs without a scheme or network location
    if not parsed.scheme or not parsed.netloc:
        return False

    # Extract the domain (netloc may contain port)
    domain = parsed.hostname
    return domain in ALLOWED_RETURN_DOMAINS


def generate_sso_redirect(
    sso_endpoint: str,
    user_id: str,
    return_url: str
) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to redirect back after successful SSO.

    Returns
    -------
    str
        Fully constructed SSO redirect URL containing user_id and return_url.

    Raises
    ------
    ValueError
        If `return_url` is not from an allowed domain or is malformed.
    """
    if not _is_allowed_return_url(return_url):
        raise ValueError(f"Return URL domain not allowed: {return_url}")

    # Prepare query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    query = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=%")

    # Parse the SSO endpoint to preserve any existing query components
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    # Combine with new query parameters, preserving existing ones
    if parsed_endpoint.query:
        combined_query = f"{parsed_endpoint.query}&{query}"
    else:
        combined_query = query

    # Reconstruct the full URL
    sso_url_parts = parsed_endpoint._replace(query=combined_query)
    return urllib.parse.urlunparse(sso_url_parts)