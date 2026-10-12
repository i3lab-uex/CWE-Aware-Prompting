import urllib.parse
from typing import Set

# Example allowed domains; in real code this would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str
) -> str:
    """
    Build a fully qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g., "https://myapp.com").
    callback_route : str
        The relative route that handles the OAuth callback (e.g., "/auth/callback").
    token_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL with the `state` query parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``
        and does not match the domain of ``application_url``.
    """
    # Resolve callback URL relative to application root
    base_parsed = urllib.parse.urlparse(application_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid application_url: {application_url!r}")

    # Build absolute callback URL
    full_callback = urllib.parse.urljoin(application_url, callback_route)
    parsed_cb = urllib.parse.urlparse(full_callback)

    # Validate domain
    cb_domain = parsed_cb.hostname
    if not cb_domain:
        raise ValueError(f"Callback URL does not contain a hostname: {full_callback!r}")

    app_domain = base_parsed.hostname
    if cb_domain not in ALLOWED_CALLBACK_DOMAINS and cb_domain != app_domain:
        raise ValueError(
            f"Callback domain '{cb_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}; "
            f"application domain: {app_domain}"
        )

    # Append the state parameter
    query = urllib.parse.parse_qs(parsed_cb.query)
    query["state"] = [token_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    assembled_url = urllib.parse.urlunparse(
        parsed_cb._replace(query=new_query)
    )
    return assembled_url