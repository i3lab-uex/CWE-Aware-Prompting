import urllib.parse
from typing import Set

# Example set of allowed return domains; replace with your actual list.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "myapp.org"}

def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base endpoint of the SSO service.
    user_identifier : str
        Unique identifier for the user (e.g., a UID or email).
    redirect_uri : str
        The URL to return to after authentication.

    Returns
    -------
    str
        Full redirect URL containing the SSO endpoint, user ID,
        and encoded return URI.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the return URL's domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    redirect_domain = parsed_redirect.hostname
    if not redirect_domain or redirect_domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{redirect_domain}' is not allowed.")

    # Parse the auth service endpoint
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)

    # Extract existing query parameters, if any
    query_params = urllib.parse.parse_qs(parsed_endpoint.query, keep_blank_values=True)

    # Add/overwrite the required parameters
    query_params["user"] = [str(user_identifier)]
    query_params["redirect_uri"] = [redirect_uri]

    # Build the new query string
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Construct the final URL
    new_endpoint = parsed_endpoint._replace(query=encoded_query)
    return urllib.parse.urlunparse(new_endpoint)

# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.example.com/auth"
    user_id = "alice123"
    return_url = "https://myapp.org/dashboard"

    try:
        redirect = construct_sso_redirect(endpoint, user_id, return_url)
        print("Redirect URL:", redirect)
    except ValueError as e:
        print("Error:", e)