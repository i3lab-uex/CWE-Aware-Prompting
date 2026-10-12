import urllib.parse
from typing import Set

# Example set of allowed domains; in real usage this would be configured elsewhere
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a safe OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application, e.g. "https://app.example.com".
    redirect_path : str
        The path to be appended, e.g. "/oauth/callback".
    nonce : str
        A state parameter used to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unauthorized domain or has an unsupported scheme.
    """
    # Ensure we have a proper base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("`main_url` must be a fully-qualified URL with scheme and host")

    # Join the base URL with the callback path
    joined = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Parse the joined URL to extract components
    parsed = urllib.parse.urlparse(joined)

    # Validate scheme (only http/https allowed)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host domain against allowed list
    hostname = parsed.hostname or ""
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not allowed for OAuth callbacks")

    # Append the nonce as a query parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [nonce]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        encoded_query,
        parsed.fragment
    ))

    return safe_url