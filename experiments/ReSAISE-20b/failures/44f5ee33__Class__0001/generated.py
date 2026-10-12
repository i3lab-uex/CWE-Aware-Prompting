import urllib.parse
from typing import Set

# Domains that are allowed to be used as callback targets.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.myapp.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The path to be appended to the base URL (e.g. "/auth/callback").
    nonce : str
        A unique state parameter used to validate the OAuth transaction.

    Returns
    -------
    str
        The fully-qualified callback URL including scheme, host, path and query.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise the base URL and path
    if not main_url:
        raise ValueError("main_url must be a non-empty string")
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Construct the full URL
    base_parsed = urllib.parse.urlparse(main_url)
    if base_parsed.scheme not in {"http", "https"}:
        raise ValueError("main_url must use http or https scheme")

    # Join path and add nonce as query
    full_path = urllib.parse.urljoin(base_parsed.path + "/", redirect_path.lstrip("/"))
    query = urllib.parse.urlencode({"state": nonce})
    callback_url = urllib.parse.urlunparse((
        base_parsed.scheme,
        base_parsed.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    ))

    # Validate domain against allowed list
    parsed_callback = urllib.parse.urlparse(callback_url)
    if parsed_callback.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{parsed_callback.hostname}' is not allowed"
        )

    return callback_url