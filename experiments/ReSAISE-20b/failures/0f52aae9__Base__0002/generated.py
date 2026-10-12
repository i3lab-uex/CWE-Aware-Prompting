import urllib.parse
from typing import Set

# Example set of allowed callback domains.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a safe OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The path to the OAuth callback handler (e.g., "/auth/callback").
    session_state : str
        A unique state value to protect against CSRF.

    Returns
    -------
    str
        The fully assembled OAuth callback URL, e.g.
        "https://app.example.com/auth/callback?state=xyz".

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS`` or does
        not match the domain of ``main_url``.
    """
    # Normalize and parse the base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main URL: {main_url!r}")

    # Build the callback path relative to the base URL
    callback_path = urllib.parse.urljoin(parsed_main.path + "/", redirect_endpoint.lstrip("/"))

    # Construct the full URL with query parameters
    query = urllib.parse.urlencode({"state": session_state})
    callback_url_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        callback_path,
        "",  # params
        query,
        ""   # fragment
    )
    callback_url = urllib.parse.urlunparse(callback_url_parts)

    # Validate the domain of the constructed URL
    parsed_callback = urllib.parse.urlparse(callback_url)
    callback_domain = parsed_callback.hostname

    if not callback_domain:
        raise ValueError("Callback URL does not contain a valid hostname.")

    # Allow same-domain callbacks or those explicitly listed
    if callback_domain != parsed_main.hostname and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {callback_domain!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return callback_url