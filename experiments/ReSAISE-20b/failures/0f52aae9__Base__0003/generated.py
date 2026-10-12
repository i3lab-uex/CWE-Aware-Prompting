import urllib.parse
from typing import Set

# Allowed domains for OAuth callback URLs.  These should be the only
# domains that can receive the redirect, e.g. the application's own
# domain(s) and any trusted third‑party providers.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str,
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The endpoint path that handles the OAuth callback (e.g. "/oauth/callback").
    session_state : str
        A unique identifier that is passed back to the client to maintain state.

    Returns
    -------
    str
        A fully assembled, validated OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS or does
        not match the main_url's host.
    """
    # Normalise and join the base URL with the callback path
    joined_url = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_endpoint.lstrip("/"))

    # Append the state parameter safely
    parsed = urllib.parse.urlparse(joined_url)
    query = dict(urllib.parse.parse_qsl(parsed.query))
    query["state"] = session_state
    new_query = urllib.parse.urlencode(query)

    final_url_parts = parsed._replace(query=new_query)
    callback_url = urllib.parse.urlunparse(final_url_parts)

    # Validate the domain to mitigate CWE‑601
    callback_host = urllib.parse.urlparse(callback_url).hostname
    if not callback_host:
        raise ValueError("Constructed URL has no hostname")

    # Ensure the host is either the same as main_url's host or in the allowed set
    main_host = urllib.parse.urlparse(main_url).hostname
    if callback_host != main_host and callback_host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback host '{callback_host}' is not allowed")

    return callback_url