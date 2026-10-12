import urllib.parse
from typing import Set

# Domains that are permitted as callback URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed
}

def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str
) -> str:
    """
    Build a secure redirect URL for an SSO provider.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service (e.g., "https://sso.example.com/login").
    account_id : str
        The unique identifier for the user to be authenticated.
    callback_url : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain of `callback_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the callback URL to extract its domain.
    parsed_callback = urllib.parse.urlparse(callback_url)
    domain = parsed_callback.hostname
    if not domain:
        raise ValueError("Callback URL must have a valid hostname")

    # Ensure the callback domain is explicitly allowed.
    if domain.lower() not in (d.lower() for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not allowed for callback URLs")

    # Build query parameters.  All values are URL‑encoded automatically.
    query_params = {
        "account_id": account_id,
        "return_url": callback_url
    }
    encoded_params = urllib.parse.urlencode(query_params)

    # Combine the login endpoint with the query string.
    if urllib.parse.urlparse(login_endpoint).scheme == "":
        # Guard against relative endpoints; enforce a scheme.
        raise ValueError("Login endpoint must be an absolute URL")

    redirect_url = f"{login_endpoint.rstrip('/')}/?" + encoded_params
    return redirect_url