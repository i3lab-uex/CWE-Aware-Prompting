import urllib.parse
from typing import Set

# Define the set of domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add more domains as needed
}


def _validate_return_url(callback_url: str) -> None:
    """
    Validate that the callback URL belongs to an allowed domain.

    Raises:
        ValueError: If the domain of the callback_url is not in ALLOWED_RETURN_DOMAINS.
    """
    parsed = urllib.parse.urlparse(callback_url)
    domain = parsed.hostname
    if not domain:
        raise ValueError("Return URL must have a valid hostname.")
    # Check for exact match or subdomain if allowed
    if domain not in ALLOWED_RETURN_DOMAINS:
        # Optionally allow subdomains of the allowed domains
        if not any(domain.endswith(f".{allowed}") for allowed in ALLOWED_RETURN_DOMAINS):
            raise ValueError(
                f"Return URL domain '{domain}' is not in the list of allowed domains."
            )


def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str,
) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service endpoint.
    account_id : str
        Unique identifier for the user/account.
    callback_url : str
        URL to which users should be redirected after authentication.

    Returns
    -------
    str
        The fully formed redirect URL ready for use in an HTTP redirect.

    Raises
    ------
    ValueError
        If the callback_url's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the return URL to mitigate CWE‑610
    _validate_return_url(callback_url)

    # Ensure callback_url is safely encoded for inclusion as a query parameter
    encoded_callback = urllib.parse.quote_plus(callback_url)

    # Build the redirect URL using urlparse components
    parsed_login = urllib.parse.urlparse(login_endpoint)

    # Construct query parameters safely
    query_params = {
        "account_id": account_id,
        "return_url": encoded_callback,
    }
    # Merge with any existing query parameters in login_endpoint
    existing_query = urllib.parse.parse_qs(parsed_login.query)
    # Flatten existing_query values (take first if multiple)
    existing_flat = {k: v[0] for k, v in existing_query.items()}
    merged_query = {**existing_flat, **query_params}
    encoded_query = urllib.parse.urlencode(merged_query)

    # Rebuild the full URL
    redirect_url_parts = (
        parsed_login.scheme,
        parsed_login.netloc,
        parsed_login.path,
        parsed_login.params,
        encoded_query,
        parsed_login.fragment,
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url