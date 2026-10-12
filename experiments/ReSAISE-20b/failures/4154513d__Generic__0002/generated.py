import urllib.parse
from typing import Set

# Example allowed domains; replace with your own list.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "myapp.org"}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO service endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URL and verify its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Redirect URL must be a valid absolute URL")

    # Normalize the domain for comparison
    redirect_domain = parsed_redirect.netloc.lower()
    if not any(redirect_domain == d or redirect_domain.endswith(f".{d}") for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError("Redirect URL domain is not allowed")

    # Build query parameters
    params = {
        "uid": uid,
        "redirect": redirect_url,  # will be encoded by urlencode
    }

    # Construct the final URL
    auth_parsed = urllib.parse.urlparse(auth_endpoint)
    query = urllib.parse.urlencode(params, safe=':/')
    # Preserve existing query params in auth_endpoint if any
    if auth_parsed.query:
        query = f"{auth_parsed.query}&{query}"

    new_url_parts = auth_parsed._replace(query=query)
    return urllib.parse.urlunparse(new_url_parts)


# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.example.com/auth"
    user_id = "12345"
    return_to = "https://myapp.org/dashboard?ref=login"

    try:
        redirect = build_sso_redirect(endpoint, user_id, return_to)
        print("Redirect URL:", redirect)
    except ValueError as e:
        print(f"Error: {e}")