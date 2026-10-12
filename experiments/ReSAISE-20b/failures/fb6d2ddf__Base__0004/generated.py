import urllib.parse
from typing import Set

# Whitelisted domains that are allowed as redirect destinations.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add more domains as needed
}


def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        Destination URL to return after authentication.

    Returns
    -------
    str
        The fully formed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect URL's domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Strip port from the netloc for comparison
    domain = parsed_redirect.hostname or ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{domain}' is not allowed")

    # Build query parameters
    params = {
        "uid": uid,
        "return_url": redirect_url,  # The SSO provider will redirect here after auth
    }
    encoded_params = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=%")

    # Combine the base auth endpoint with query string
    if urllib.parse.urlparse(auth_endpoint).scheme:
        # auth_endpoint is already a full URL
        base = auth_endpoint.rstrip("?")
    else:
        # If a relative endpoint is provided, resolve it against a base
        raise ValueError("auth_endpoint must be an absolute URL")

    if "?" in base:
        full_url = f"{base}&{encoded_params}"
    else:
        full_url = f"{base}?{encoded_params}"

    return full_url