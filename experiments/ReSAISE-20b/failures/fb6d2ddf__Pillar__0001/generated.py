import urllib.parse
from typing import Set

# Whitelist of domains that are allowed to receive the SSO redirect.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add additional trusted domains here
}

def _extract_domain(url: str) -> str:
    """
    Extracts the network location (netloc) from a URL and normalizes it
    by stripping leading 'www.' if present.
    """
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that points to the external identity provider.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        The URL to which the provider should redirect after authentication.

    Returns
    -------
    str
        A fully-formed URL that can be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If `redirect_url`'s domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain
    redirect_domain = _extract_domain(redirect_url)
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{redirect_domain}' is not allowed.")

    # Parse the auth endpoint to safely append query parameters
    parsed_auth = urllib.parse.urlparse(auth_endpoint)

    # Prepare the query parameters.  We encode them to avoid injection issues.
    params = {
        "uid": uid,
        # Use a query name that the provider expects; adjust as needed.
        "redirect_uri": redirect_url,
    }
    encoded_params = urllib.parse.urlencode(params, doseq=True)

    # Reconstruct the full URL with updated query string
    sso_url = urllib.parse.urlunparse(
        parsed_auth._replace(query=encoded_params)
    )

    return sso_url