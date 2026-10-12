import urllib.parse
from typing import Iterable

# Example list of allowed callback domains – replace with your own safe list.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://myapp.com").
    redirect_path : str
        The path component for the OAuth callback (e.g., "/oauth/callback").
    token_state : str
        A unique value to be appended as the `state` query parameter.

    Returns
    -------
    str
        A fully formed, validated OAuth redirect URL.

    Raises
    ------
    ValueError
        If the computed callback domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalize the base URL
    parsed_main = urllib.parse.urlparse(main_url.rstrip("/"))
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url}")

    # Combine the path safely
    combined_path = urllib.parse.urljoin(parsed_main.path + "/", redirect_path.lstrip("/"))

    # Build query parameters, ensuring `state` is present
    query = urllib.parse.urlencode({"state": token_state})

    # Assemble the full URL components
    callback_url = urllib.parse.urlunparse((
        parsed_main.scheme,
        parsed_main.netloc,
        combined_path,
        "",          # params
        query,       # query
        ""           # fragment
    ))

    # Validate the domain to mitigate open redirect (CWE-601)
    callback_netloc = urllib.parse.urlparse(callback_url).netloc
    if callback_netloc.split(":")[0] not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{callback_netloc}' is not allowed")

    return callback_url