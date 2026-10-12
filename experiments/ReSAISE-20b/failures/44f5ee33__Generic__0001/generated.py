import urllib.parse
from typing import Set

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add more allowed domains as needed.
}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The path component that will handle the OAuth callback (e.g. "/auth/callback").
    nonce : str
        A state value used to prevent CSRF attacks.

    Returns
    -------
    str
        The fully‑qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Parse the base URL and make sure it contains a scheme.
    parsed_base = urllib.parse.urlparse(main_url)
    if not parsed_base.scheme:
        raise ValueError(f"Base URL must include a scheme: {main_url!r}")

    # Build the full path by joining the base URL with the redirect path.
    joined = urllib.parse.urljoin(parsed_base.geturl(), redirect_path)

    # Parse the joined URL to inspect its components.
    parsed = urllib.parse.urlparse(joined)

    # Validate that the host is allowed.
    host = parsed.hostname
    if not host or host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain {host!r} is not allowed")

    # Append the state parameter as a query string.
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [nonce]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL with the new query string.
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )
    return final_url