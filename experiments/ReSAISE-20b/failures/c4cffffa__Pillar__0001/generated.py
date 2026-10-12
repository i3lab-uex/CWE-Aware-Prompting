import urllib.parse
from typing import Set

# Allowed domains for the return URL (example values, adjust as needed)
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "trustedpartner.org"}


def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g., "https://sso.provider.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g., a UUID or email).
    redirect_back_url : str
        The URL to return to after authentication.

    Returns
    -------
    str
        A fully formed redirect URL with encoded query parameters.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect_back_url to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_back_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect_back_url: missing scheme or netloc")

    # Extract the hostname and check against allowed domains
    hostname = parsed_redirect.hostname
    if not hostname or hostname.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(
            f"Return URL domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(ALLOWED_RETURN_DOMAINS)}"
        )

    # Build query parameters
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_back_url
    }

    # Encode parameters safely
    encoded_query = urllib.parse.urlencode(query_params, safe=":/")

    # Construct the final URL
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    # Preserve any existing query parameters in the SSO URL
    existing_query = parsed_sso.query
    combined_query = "&".join(filter(None, [existing_query, encoded_query]))

    sso_redirect = urllib.parse.urlunparse(
        parsed_sso._replace(query=combined_query)
    )

    return sso_redirect