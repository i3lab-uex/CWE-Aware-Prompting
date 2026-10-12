import urllib.parse
from typing import Set

# Whitelist of domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.internal",
    # Add more trusted domains here.
}


def construct_sso_redirect(
    sso_uri: str,
    user_identifier: str,
    redirect_link: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base SSO endpoint (may include existing query parameters).
    user_identifier : str
        Unique identifier for the user.
    redirect_link : str
        Absolute URL to which the IdP should return after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # 1. Validate the redirect_link domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be an absolute URL")

    # Extract the hostname (without port)
    hostname = parsed_redirect.hostname
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # 2. Prepare query parameters
    redirect_params = {
        "user_id": user_identifier,
        # Ensure the redirect URL is percent‑encoded
        "redirect_uri": redirect_link,
    }
    encoded_params = urllib.parse.urlencode(redirect_params, doseq=True)

    # 3. Merge with the base SSO URI
    parsed_sso = urllib.parse.urlparse(sso_uri)
    # Preserve existing query parameters if any
    existing_query = parsed_sso.query
    new_query = (
        f"{existing_query}&{encoded_params}" if existing_query else encoded_params
    )

    # Rebuild the full URL
    new_sso = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(new_sso)


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    sso_endpoint = "https://sso.example.com/auth"
    user_id = "user-12345"
    return_url = "https://example.com/welcome?foo=bar"

    try:
        url = construct_sso_redirect(sso_endpoint, user_id, return_url)
        print("SSO Redirect URL:", url)
    except ValueError as e:
        print("Error constructing SSO redirect:", e)