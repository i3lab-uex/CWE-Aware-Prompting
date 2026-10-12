import urllib.parse
from typing import Set

# Allowed domains for OAuth callbacks (example set)
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"myapp.com", "auth.myapp.com"}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_path : str
        The path to handle OAuth callbacks (e.g., "/oauth/callback").
    nonce : str
        A unique state parameter used to prevent CSRF.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL with the nonce as a query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ALLOWED_CALLBACK_DOMAINS or if
        the base URL is malformed.
    """
    # Parse and validate the main URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main URL: {main_url!r}")

    # Ensure the redirect path is relative and starts with a slash
    if not redirect_path.startswith("/"):
        raise ValueError(f"Redirect path must be relative and start with '/': {redirect_path!r}")

    # Construct the full URL (scheme + netloc + path)
    base = f"{parsed_main.scheme}://{parsed_main.netloc}"
    full_path = urllib.parse.urljoin(base, redirect_path)

    # Parse the resulting URL to extract its domain
    parsed_full = urllib.parse.urlparse(full_path)
    callback_domain = parsed_full.netloc

    # Domain whitelist check
    if callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized redirect domain: {callback_domain!r}")

    # Append the nonce as a query parameter
    query = urllib.parse.urlencode({"state": nonce})
    final_url = urllib.parse.urlunparse(
        (
            parsed_full.scheme,
            parsed_full.netloc,
            parsed_full.path,
            parsed_full.params,
            query,
            parsed_full.fragment,
        )
    )

    return final_url