import urllib.parse
from typing import Set

# Whitelist of domains that are allowed as the return URL after SSO.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add additional domains as needed.
}

def _extract_domain(url: str) -> str:
    """
    Return the hostname part of a URL, lower‑cased and without port.
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    return host.lower()

def construct_sso_redirect(
    sso_uri: str,
    user_identifier: str,
    redirect_link: str
) -> str:
    """
    Build a full SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base URL of the SSO provider.
    user_identifier : str
        Unique identifier for the user (e.g., a UUID).
    redirect_link : str
        URL to return to after authentication.

    Returns
    -------
    str
        The complete SSO redirect URL with query parameters encoded.
    
    Raises
    ------
    ValueError
        If the redirect_link's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate return URL domain
    domain = _extract_domain(redirect_link)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{domain}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Parse the base SSO URI to manipulate its query string
    parsed_sso = urllib.parse.urlparse(sso_uri)
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))

    # Add or overwrite required parameters
    existing_params["user"] = user_identifier
    existing_params["return_url"] = redirect_link

    # Rebuild the URL with updated query string
    new_query = urllib.parse.urlencode(existing_params, doseq=True)
    new_sso_parts = parsed_sso._replace(query=new_query)

    return urllib.parse.urlunparse(new_sso_parts)