import urllib.parse
from typing import Set

# Domains that are allowed to receive the OAuth callback.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://app.example.org").
    callback_path : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    state : str
        A unique, unguessable string used to mitigate CSRF attacks.

    Returns
    -------
    str
        A fully qualified callback URL that includes the state parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain not in
        ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure the callback path is properly quoted to avoid injection
    safe_path = urllib.parse.quote(callback_path, safe="/")
    # Combine base URL and path safely
    full_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", safe_path.lstrip("/"))
    # Append the state query parameter
    parsed = urllib.parse.urlparse(full_url)
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query_params["state"] = [state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    final_url = parsed._replace(query=new_query).geturl()

    # Validate that the domain is allowed
    netloc = urllib.parse.urlparse(final_url).netloc.lower()
    # Strip port if present
    domain = netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain}")

    return final_url