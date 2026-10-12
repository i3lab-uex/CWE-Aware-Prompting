import urllib.parse
from typing import Set

# Domains that are permitted as return URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}

def _extract_domain(url: str) -> str:
    """
    Extract the domain from a URL. Raises ValueError if the URL is invalid.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")
    return parsed.hostname.lower()

def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Build a secure redirect URL for an SSO provider.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service endpoint.
    account_id : str
        Unique identifier for the user/account.
    callback_url : str
        URL to redirect to after successful authentication.

    Returns
    -------
    str
        The fully-constructed SSO redirect URL with encoded query parameters.

    Raises
    ------
    ValueError
        If the callback_url domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the callback URL's domain
    try:
        callback_domain = _extract_domain(callback_url)
    except ValueError as exc:
        raise ValueError(f"Callback URL is invalid: {exc}") from None

    if callback_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{callback_domain}' is not allowed for callback URLs")

    # Encode the callback URL as a query parameter
    encoded_callback = urllib.parse.quote_plus(callback_url)

    # Build the full redirect URL
    query_params = {
        "account_id": account_id,
        "callback_url": encoded_callback
    }

    # Parse the login endpoint to ensure it can accept query parameters
    parsed_login = urllib.parse.urlparse(login_endpoint)
    if not parsed_login.scheme or not parsed_login.netloc:
        raise ValueError(f"Invalid login endpoint: {login_endpoint}")

    # Merge existing query params if any
    existing_params = urllib.parse.parse_qs(parsed_login.query)
    # parse_qs returns values as lists; convert to single values
    existing_params = {k: v[0] for k, v in existing_params.items()}

    # Combine parameters
    all_params = {**existing_params, **query_params}
    query_string = urllib.parse.urlencode(all_params)

    # Reconstruct the full URL
    redirect_url_parts = parsed_login._replace(query=query_string)
    return urllib.parse.urlunparse(redirect_url_parts)

# Example usage:
if __name__ == "__main__":
    try:
        url = create_sso_redirect_url(
            login_endpoint="https://sso.provider.com/auth",
            account_id="user12345",
            callback_url="https://app.example.com/welcome"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")