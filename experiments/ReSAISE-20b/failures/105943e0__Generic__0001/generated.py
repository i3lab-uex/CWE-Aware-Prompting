import urllib.parse
from typing import Set

# Example set of allowed domains. In real usage this should be configured securely.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    "trustedpartner.net"
}


def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str
) -> str:
    """
    Build a redirect URL for SSO authentication.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service endpoint.
    account_id : str
        Unique identifier for the user/account.
    callback_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully constructed redirect URL containing query parameters.

    Raises
    ------
    ValueError
        If the domain of ``callback_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate callback domain
    parsed_callback = urllib.parse.urlparse(callback_url)
    domain = parsed_callback.netloc.lower()

    # Allow subdomains only if the root domain is permitted
    allowed = any(
        domain == allowed or domain.endswith("." + allowed)
        for allowed in ALLOWED_RETURN_DOMAINS
    )
    if not allowed:
        raise ValueError(
            f"Callback domain '{domain}' is not in the list of allowed domains."
        )

    # Build query parameters
    params = {
        "account_id": account_id,
        "redirect_uri": callback_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/")  # Preserve :// in URLs

    # Construct final URL
    if urllib.parse.urlparse(login_endpoint).scheme:
        base = login_endpoint.rstrip("?")
    else:
        raise ValueError("login_endpoint must be a valid absolute URL")

    redirect_url = f"{base}?{query_string}"
    return redirect_url