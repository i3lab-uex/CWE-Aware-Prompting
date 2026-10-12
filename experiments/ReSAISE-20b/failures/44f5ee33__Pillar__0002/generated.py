import urllib.parse
from typing import Set

# Example set of allowed callback domains. In a real application this should be
# defined in configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The path component for the OAuth callback (e.g. "/auth/callback").
    nonce : str
        A cryptographically random string used as the OAuth state parameter.

    Returns
    -------
    str
        The fully-qualified redirect URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise the base URL and ensure it has a scheme
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme:
        raise ValueError("main_url must include a scheme (e.g., https://)")

    # Combine base URL with redirect path
    combined = urllib.parse.urljoin(parsed_main.geturl(), redirect_path)

    # Append the state (nonce) as a query parameter
    parsed_combined = urllib.parse.urlparse(combined)
    # Preserve any existing query parameters and add state
    query_params = dict(urllib.parse.parse_qsl(parsed_combined.query))
    query_params["state"] = nonce
    new_query = urllib.parse.urlencode(query_params)

    final_url_parts = parsed_combined._replace(query=new_query)
    final_url = urllib.parse.urlunparse(final_url_parts)

    # Validate the domain of the final URL
    final_domain = urllib.parse.urlparse(final_url).hostname
    if not final_domain or final_domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{final_domain}' is not allowed")

    return final_url