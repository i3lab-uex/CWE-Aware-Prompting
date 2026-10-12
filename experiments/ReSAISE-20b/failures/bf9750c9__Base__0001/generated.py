import urllib.parse
from typing import Set

# Example whitelist – replace with your actual domains.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    "trustedsite.net"
}


def construct_sso_redirect(sso_uri: str, user_identifier: str,
                           redirect_link: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base URI of the SSO provider.
    user_identifier : str
        Unique identifier for the authenticated user.  It is appended to
        ``sso_uri`` as a query parameter named ``user_id``.
    redirect_link : str
        Absolute URL that the user should be sent to after SSO completes.
        The hostname must appear in :data:`ALLOWED_RETURN_DOMAINS`.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the hostname of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`
        or if either input is malformed.
    """
    # Validate the SSO base URI
    sso_parsed = urllib.parse.urlparse(sso_uri)
    if not sso_parsed.scheme or not sso_parsed.netloc:
        raise ValueError(f"Invalid SSO URI: {sso_uri!r}")

    # Validate the redirect link
    redirect_parsed = urllib.parse.urlparse(redirect_link)
    if not redirect_parsed.scheme or not redirect_parsed.netloc:
        raise ValueError(f"Invalid redirect link: {redirect_link!r}")

    # Ensure the domain is whitelisted
    hostname = redirect_parsed.hostname
    if not hostname or hostname.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Redirect domain {hostname!r} is not allowed")

    # Build the query parameters
    query = urllib.parse.parse_qs(sso_parsed.query, keep_blank_values=True)
    # ``parse_qs`` returns list values; we convert to single strings
    query = {k: v[0] if len(v) == 1 else v for k, v in query.items()}

    # Add/override the user_id and redirect parameters
    query["user_id"] = user_identifier
    # Encode the full redirect link as a single string value
    query["redirect"] = redirect_link

    # Reconstruct the full SSO URL
    new_query = urllib.parse.urlencode(query, doseq=True)
    sso_url_parts = list(sso_parsed)
    sso_url_parts[4] = new_query  # index 4 is the query component
    return urllib.parse.urlunparse(sso_url_parts)