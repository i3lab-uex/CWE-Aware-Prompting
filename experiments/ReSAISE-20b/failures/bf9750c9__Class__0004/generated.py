import urllib.parse
from typing import Set

# Whitelist of domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
}

def construct_sso_redirect(
    sso_uri: str,
    user_identifier: str,
    redirect_link: str
) -> str:
    """
    Build an SSO redirect URL that includes the user identifier and a return URL.
    
    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint (e.g. "https://sso.example.com/login").
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_link : str
        Absolute URL to which the user should be redirected after SSO.
    
    Returns
    -------
    str
        Fully-formed SSO redirect URL.
    
    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect_link domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be a fully-qualified URL")

    # Normalize the host (lowercase, strip port)
    host = parsed_redirect.hostname.lower() if parsed_redirect.hostname else ""
    # Check that the host ends with one of the allowed domains
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"redirect_link domain '{host}' is not allowed")

    # Parse the base SSO URI to manipulate its query parameters
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Build the new query dict
    query_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # Use list values as required by parse_qs
    query_params["user_id"] = [user_identifier]
    query_params["redirect_uri"] = [redirect_link]

    # Reconstruct the URL
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    new_sso_parts = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(new_sso_parts)