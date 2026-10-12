import urllib.parse
from typing import Iterable

# Example set of allowed domains; in real code this would be imported or configured elsewhere
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(
    main_url: str,
    redirect_path: str,
    token_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The path for the OAuth callback (e.g., "/auth/callback").
    token_state : str
        A unique state value to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully qualified OAuth callback URL with a state query parameter.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure the redirect path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Join base URL and path safely
    base_parsed = urllib.parse.urlparse(main_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("main_url must be a valid absolute URL")

    # Build the full path with query parameters
    callback_path = urllib.parse.urljoin(base_parsed.path or "/", redirect_path)
    query = urllib.parse.urlencode({"state": token_state})
    full_url_parts = (
        base_parsed.scheme,
        base_parsed.netloc,
        callback_path,
        "",  # params
        query,
        ""   # fragment
    )
    callback_url = urllib.parse.urlunparse(full_url_parts)

    # Verify the domain is allowed
    callback_domain = urllib.parse.urlparse(callback_url).hostname or ""
    if callback_domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Disallowed callback domain: {callback_domain}")

    return callback_url