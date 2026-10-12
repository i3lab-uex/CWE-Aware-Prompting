import urllib.parse
from typing import Iterable

# Example allowed domains; replace with real values in production.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The path segment for the OAuth callback (e.g., "/oauth/callback").
    token_state : str
        A unique state value to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully-qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the redirect path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Join the base URL with the redirect path
    callback_url = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Append the state parameter safely
    parsed = urllib.parse.urlparse(callback_url)
    query = dict(urllib.parse.parse_qsl(parsed.query))
    query["state"] = token_state
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL with the new query string
    safe_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Validate domain against allowed list
    domain = urllib.parse.urlparse(safe_url).hostname or ""
    if not any(domain == allowed or domain.endswith("." + allowed) for allowed in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Callback domain '{domain}' is not allowed.")

    return safe_url