import urllib.parse
from typing import Set

# Domains that are allowed to be used as a return URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.example.org",
    # Add additional trusted domains here
}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a single sign‑on (SSO) redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO provider (e.g. "https://sso.example.com/login").
    user_identifier : str
        Unique identifier for the user that will be passed to the SSO provider.
    redirect_back_url : str
        URL where the user should be sent after successful authentication.

    Returns
    -------
    str
        Fully constructed SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect_back_url to extract its domain
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    return_domain = parsed_return.netloc.lower()

    # Strip port if present for domain comparison
    if ":" in return_domain:
        return_domain = return_domain.split(":")[0]

    if return_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{return_domain}' is not permitted."
        )

    # Build query parameters safely
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_back_url
    }
    encoded_params = urllib.parse.urlencode(query_params, safe=":/")

    # Construct the final URL
    sso_parsed = urllib.parse.urlparse(sso_service_url)
    # Preserve any existing query parameters in the SSO URL
    if sso_parsed.query:
        new_query = f"{sso_parsed.query}&{encoded_params}"
    else:
        new_query = encoded_params

    final_url_parts = sso_parsed._replace(query=new_query)
    return urllib.parse.urlunparse(final_url_parts)

# Example usage:
if __name__ == "__main__":
    try:
        url = build_sso_redirect_link(
            sso_service_url="https://sso.example.com/login",
            user_identifier="user-12345",
            redirect_back_url="https://myapp.example.org/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")