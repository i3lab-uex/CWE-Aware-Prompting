import urllib.parse
from typing import Set

# Pre‑defined set of domains that are allowed for OAuth callbacks.
# In a real application this would be defined elsewhere and imported.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def assemble_oauth_callback(application_url: str, callback_route: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://myapp.com").
    callback_route : str
        The path to the OAuth callback handler (e.g. "/auth/callback").
    token_state : str
        A unique identifier used as a state parameter.

    Returns
    -------
    str
        The fully assembled callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the resulting URL is not in ``ALLOWED_CALLBACK_DOMAINS``
        and does not match the domain of ``application_url``.
    """
    # Parse the base application URL
    app_parsed = urllib.parse.urlparse(application_url)
    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError("Invalid application_url: must include scheme and host")

    # Build the full callback URL by combining path components
    # Ensure that there is exactly one slash between host and route
    callback_path = urllib.parse.urljoin(app_parsed.path + "/", callback_route.lstrip("/"))
    full_url = urllib.parse.ParseResult(
        scheme=app_parsed.scheme,
        netloc=app_parsed.netloc,
        path=callback_path,
        params="",
        query=f"state={urllib.parse.quote_plus(token_state)}",
        fragment=""
    ).geturl()

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    callback_domain = parsed_full.hostname.lower() if parsed_full.hostname else ""
    app_domain = app_parsed.hostname.lower() if app_parsed.hostname else ""

    # The callback domain must be either the same as the application domain
    # or explicitly listed in ALLOWED_CALLBACK_DOMAINS.
    if callback_domain != app_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {callback_domain}. "
            f"Allowed domains are {ALLOWED_CALLBACK_DOMAINS} or the same as application domain."
        )

    return full_url