import urllib.parse
from typing import Iterable

# Example allowed domains; replace with your own whitelist.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}


def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_path : str
        The relative path to the OAuth callback endpoint (e.g. "/auth/callback").
    token_state : str
        A unique value to prevent CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the computed callback URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the redirect path starts with a slash and is safely encoded
    safe_path = urllib.parse.quote(redirect_path, safe="/")
    # Join the base URL and path
    callback_url = urllib.parse.urljoin(main_url, safe_path)

    # Append the state parameter
    parsed = urllib.parse.urlparse(callback_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = token_state
    new_query = urllib.parse.urlencode(query_params)
    callback_url = parsed._replace(query=new_query).geturl()

    # Validate the domain
    netloc = urllib.parse.urlparse(callback_url).netloc.lower()
    # Remove potential port number
    domain = netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {domain}. Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return callback_url