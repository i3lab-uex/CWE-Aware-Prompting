import urllib.parse
from typing import Set

# Domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "sub.example.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_back_url : str
        URL to return to after successful SSO.

    Returns
    -------
    str
        The fully-formed redirect URL with query parameters encoded.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`
        or if the scheme of the return URL is not HTTPS.
    """
    # Validate that redirect_back_url is a full URL and uses https
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    if parsed_return.scheme != "https":
        raise ValueError("Return URL must use HTTPS scheme.")
    if not parsed_return.netloc:
        raise ValueError("Return URL must contain a network location (domain).")

    # Extract the domain part for validation
    domain = parsed_return.hostname or ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed.")

    # Construct query parameters
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url
    }
    encoded_params = urllib.parse.urlencode(params, safe="/:")  # allow ':' and '/' in URLs

    # Parse the SSO service URL to safely combine paths
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("SSO service URL must be a valid absolute URL.")

    # Build the final redirect URL
    sso_base = urllib.parse.urlunparse(parsed_sso._replace(query=""))
    final_url = f"{sso_base}?{encoded_params}"

    return final_url