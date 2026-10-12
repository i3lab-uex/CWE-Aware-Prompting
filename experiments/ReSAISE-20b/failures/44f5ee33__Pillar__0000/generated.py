import urllib.parse
from typing import Set

# Example set of allowed callback domains – replace with real values in production.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_path : str
        The path to execute OAuth callbacks (e.g., "/auth/callback").
    nonce : str
        A unique state value used to verify the OAuth transaction.

    Returns
    -------
    str
        The fully qualified callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the redirect path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Join the base URL with the path
    full_url = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Parse the resulting URL to validate its domain
    parsed = urllib.parse.urlparse(full_url)

    # Reject URLs that lack a scheme or netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid callback URL constructed: {full_url}")

    # Extract the hostname for domain validation
    hostname = parsed.hostname or ""
    if hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {hostname}")

    # Append the state parameter
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [nonce]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Rebuild the full URL with the new query string
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url