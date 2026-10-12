import urllib.parse
from typing import Set

# Domains that are considered safe for the callback URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add other trusted domains here.
}

def _is_allowed_domain(domain: str) -> bool:
    """
    Checks whether the given domain (or any of its parent domains)
    is present in ALLOWED_RETURN_DOMAINS.
    """
    # Normalize the domain (lowercase, strip trailing dot)
    domain = domain.lower().rstrip(".")
    # Direct match
    if domain in ALLOWED_RETURN_DOMAINS:
        return True
    # Check parent domains (e.g., foo.example.com -> example.com)
    parts = domain.split(".")
    for i in range(1, len(parts)):
        parent = ".".join(parts[i:])
        if parent in ALLOWED_RETURN_DOMAINS:
            return True
    return False

def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str
) -> str:
    """
    Builds a secure SSO redirect URL that includes the account ID and
    a validated callback URL.

    Parameters:
        login_endpoint (str): The SSO service endpoint.
        account_id (str): The unique identifier for the user.
        callback_url (str): URL to redirect back after authentication.

    Returns:
        str: The fully formed SSO redirect URL.

    Raises:
        ValueError: If the callback_url's domain is not in
                    ALLOWED_RETURN_DOMAINS.
    """
    # Parse the callback URL to validate its domain
    parsed_cb = urllib.parse.urlparse(callback_url)
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError("callback_url must be an absolute URL with scheme and netloc")

    if not _is_allowed_domain(parsed_cb.netloc):
        raise ValueError(f"Return URL domain '{parsed_cb.netloc}' is not allowed")

    # Encode the callback URL to be safely passed as a query parameter
    encoded_cb = urllib.parse.quote(callback_url, safe="")

    # Build the new query string
    query_params = {
        "account_id": account_id,
        "return_url": encoded_cb
    }

    # Parse the login endpoint to merge any existing query parameters
    parsed_login = urllib.parse.urlparse(login_endpoint)
    # Merge with existing query params if any
    existing_params = urllib.parse.parse_qs(parsed_login.query, keep_blank_values=True)
    # Flatten parse_qs output
    merged_params = {k: v[0] for k, v in existing_params.items()}
    merged_params.update(query_params)

    # Construct the final URL
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    final_url_parts = parsed_login._replace(query=new_query)
    return urllib.parse.urlunparse(final_url_parts)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        url = create_sso_redirect_url(
            "https://sso.example.com/auth",
            "user-12345",
            "https://sub.example.org/welcome?ref=home"
        )
        print(url)
    except ValueError as e:
        print(f"Invalid callback URL: {e}")