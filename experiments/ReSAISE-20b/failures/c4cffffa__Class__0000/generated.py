import urllib.parse
from typing import Set

# Allowed domains for the redirect_back_url. Add your trusted domains here.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "trustedpartner.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (must be absolute).
    user_identifier : str
        Unique identifier for the user.
    redirect_back_url : str
        URL to return to after SSO completes.

    Returns
    -------
    str
        Full redirect URL containing the user identifier and return URL as query parameters.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """

    # Validate the redirect_back_url is an absolute URL
    parsed_redirect = urllib.parse.urlparse(redirect_back_url)
    if not (parsed_redirect.scheme and parsed_redirect.netloc):
        raise ValueError("redirect_back_url must be an absolute URL")

    # Extract the domain and check against allowed list
    domain = parsed_redirect.hostname or ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Prepare query parameters
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url
    }

    # Encode parameters and build the final URL
    query_string = urllib.parse.urlencode(params, safe=":/")
    # Preserve existing query parameters in sso_service_url
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    existing_query = parsed_sso.query
    if existing_query:
        full_query = f"{existing_query}&{query_string}"
    else:
        full_query = query_string

    # Reconstruct the URL with updated query
    new_sso_url = urllib.parse.urlunparse(
        parsed_sso._replace(query=full_query)
    )
    return new_sso_url