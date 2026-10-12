import urllib.parse
from typing import Iterable

# Example list of allowed domains – replace with your actual list.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.myapp.com"}


def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a full OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The path where the OAuth provider should redirect to (e.g. "/auth/callback").
    token_state : str
        A unique state string to mitigate CSRF attacks.

    Returns
    -------
    str
        The complete callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure redirect_path starts with a slash for correct urljoin behaviour
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Build the base URL for the callback
    callback_url = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Append the state query parameter
    parsed = urllib.parse.urlparse(callback_url)
    qs = dict(urllib.parse.parse_qsl(parsed.query))
    qs["state"] = token_state
    new_query = urllib.parse.urlencode(qs)

    final_url = parsed._replace(query=new_query).geturl()

    # Validate domain
    domain = urllib.parse.urlparse(final_url).netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{domain}' is not allowed")

    return final_url