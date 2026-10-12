import urllib.parse
from typing import Set

# Whitelist of domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "trusted.org"}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Build an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base URL of the SSO endpoint.
    uid : str
        Unique user identifier to include in the query string.
    redirect_url : str
        Destination URL after SSO authentication.

    Returns
    -------
    str
        A fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    domain = parsed_redirect.netloc.split(":")[0].lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for redirect_url")

    # Build query parameters
    query_params = {
        "uid": uid,
        "redirect_uri": redirect_url,
    }

    # Parse the base SSO path to preserve any existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_path)
    # Merge existing and new query parameters
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # Flatten existing_params values (parse_qs returns lists)
    merged_params = {k: v[0] if isinstance(v, list) else v for k, v in existing_params.items()}
    merged_params.update(query_params)

    # Reconstruct the full URL
    new_query = urllib.parse.urlencode(merged_params)
    sso_url_parts = parsed_sso._replace(query=new_query, fragment="")
    full_sso_url = urllib.parse.urlunparse(sso_url_parts)

    return full_sso_url