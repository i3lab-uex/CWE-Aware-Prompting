import urllib.parse
from typing import Set

# Example allowed domains; replace with your actual set.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    "myapp.local",
}

def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str,
) -> str:
    """
    Build a redirect URL for SSO authentication.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service.
    account_id : str
        Unique identifier for the user.
    callback_url : str
        URL to redirect the user after successful authentication.

    Returns
    -------
    str
        The full SSO redirect URL including query parameters.

    Raises
    ------
    ValueError
        If the callback_url's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the callback URL to inspect its domain
    parsed_cb = urllib.parse.urlparse(callback_url)
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError(f"Invalid callback URL: {callback_url}")

    # Extract domain (host) and normalize it
    host = parsed_cb.hostname or ""
    if host.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Callback domain '{host}' is not allowed")

    # Encode the callback URL so it can be safely passed as a query param
    encoded_cb = urllib.parse.quote(callback_url, safe="")

    # Build the full redirect URL
    query_params = {
        "account_id": account_id,
        "return_url": encoded_cb,
    }
    # Parse the login endpoint to merge any existing query params
    parsed_login = urllib.parse.urlparse(login_endpoint)
    # Preserve existing query parameters from the login endpoint
    existing_params = urllib.parse.parse_qs(parsed_login.query)
    # Flatten existing_params values (parse_qs returns list values)
    flattened_existing = {k: v[0] for k, v in existing_params.items()}

    # Merge with new params (new params override existing ones if duplicate)
    merged_params = {**flattened_existing, **query_params}
    new_query = urllib.parse.urlencode(merged_params)

    # Reconstruct the full URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_login.scheme,
            parsed_login.netloc,
            parsed_login.path,
            parsed_login.params,
            new_query,
            parsed_login.fragment,
        )
    )

    return redirect_url