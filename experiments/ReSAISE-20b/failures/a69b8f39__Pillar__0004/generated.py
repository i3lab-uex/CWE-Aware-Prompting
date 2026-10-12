import urllib.parse
from typing import Set

# Domains that are allowed for the return URL.  Update this set as needed.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "trusted.example.org",
}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct a Single Sign-On redirect URL that forwards the user to
    `sso_service` with their identifier and a return URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO provider.  May already contain query parameters.
    user_ref : str
        Unique identifier of the user to be sent to the SSO provider.
    back_url : str
        URL to redirect the user back to after authentication.  Must belong
        to one of :data:`ALLOWED_RETURN_DOMAINS`.

    Returns
    -------
    str
        A fully‑qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain of `back_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL's domain
    parsed_back = urllib.parse.urlparse(back_url)
    back_domain = parsed_back.hostname
    if not back_domain or back_domain.lower() not in (d.lower() for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Return URL domain '{back_domain}' is not allowed.")

    # Prepare query parameters.  The back_url itself must be URL‑encoded.
    params = {
        "user_ref": user_ref,
        "back_url": back_url,  # urlencode will handle encoding
    }
    encoded_params = urllib.parse.urlencode(params)

    # Parse the SSO service URL to handle existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_service)
    # Merge existing query params with new ones
    existing_query = parsed_sso.query
    if existing_query:
        # Preserve order: new params appended after existing ones.
        full_query = f"{existing_query}&{encoded_params}"
    else:
        full_query = encoded_params

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        full_query,
        parsed_sso.fragment
    ))
    return final_url