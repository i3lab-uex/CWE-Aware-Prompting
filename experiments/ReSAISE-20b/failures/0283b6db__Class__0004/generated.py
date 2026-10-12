import urllib.parse
from typing import Set

# Allowed domains for the return URL (example set; modify as needed)
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "trusted.org"}

def _is_allowed_return_url(return_url: str) -> bool:
    """
    Verify that the return URL belongs to an allowed domain.
    Raises ValueError if not allowed.
    """
    parsed = urllib.parse.urlparse(return_url)
    # Reject URLs without a network location (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("Return URL must be absolute with a network location")

    # Normalize domain to lower case for comparison
    domain = parsed.hostname.lower() if parsed.hostname else ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")
    return True

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        Base endpoint of the SSO service (e.g., "https://sso.example.com/auth").
    user_id : str
        Unique identifier for the user.
    return_url : str
        Absolute URL to redirect back after SSO.

    Returns
    -------
    str
        Full redirect URL including query parameters.

    Raises
    ------
    ValueError
        If the return_url is not from an allowed domain.
    """
    # Validate the return URL
    _is_allowed_return_url(return_url)

    # Build query parameters safely
    params = {
        "user_id": user_id,
        "return_url": return_url
    }
    query = urllib.parse.urlencode(params, safe=":/")  # keep scheme and slashes in return_url

    # Construct the final URL
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    if parsed_endpoint.scheme not in {"http", "https"}:
        raise ValueError("SSO endpoint must use http or https scheme")

    # Preserve existing query parameters on the endpoint if any
    existing_query = parsed_endpoint.query
    combined_query = "&".join(filter(None, [existing_query, query]))

    redirect_url = urllib.parse.urlunparse((
        parsed_endpoint.scheme,
        parsed_endpoint.netloc,
        parsed_endpoint.path,
        parsed_endpoint.params,
        combined_query,
        parsed_endpoint.fragment
    ))

    return redirect_url