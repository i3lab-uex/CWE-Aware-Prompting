import urllib.parse
from typing import Set

# Domains allowed for OAuth callbacks (example values; adjust as needed)
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    "localhost",
}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The relative path where the OAuth provider should return (e.g. "/oauth/callback").
    nonce : str
        A unique string used as the state parameter to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL, including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL uses an unauthorized domain or scheme.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or parsed_main.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_main.scheme}'. Only http and https are allowed.")

    # Resolve the full path (handles leading/trailing slashes)
    resolved_path = urllib.parse.urljoin(parsed_main.path.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Construct the full URL without query
    base_callback = urllib.parse.urlunparse(
        (
            parsed_main.scheme,
            parsed_main.netloc,
            resolved_path,
            "",  # params
            "",  # query (empty for now)
            "",  # fragment
        )
    )

    # Verify the domain is authorized
    if parsed_main.netloc.split(":")[0] not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{parsed_main.netloc}' is not authorized for OAuth callbacks.")

    # Append the state parameter
    query = urllib.parse.urlencode({"state": nonce})
    final_url = f"{base_callback}?{query}"

    return final_url