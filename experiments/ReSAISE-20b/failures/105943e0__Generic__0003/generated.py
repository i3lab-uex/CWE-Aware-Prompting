import urllib.parse
from typing import Set

# Example set of allowed domains – replace with your actual list.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.org",
}

def _is_allowed_domain(url: str) -> bool:
    """
    Checks whether the domain of a URL is in ALLOWED_RETURN_DOMAINS.
    Subdomains are accepted if they end with an allowed domain.
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if not host:
        return False

    # Compare the full hostname against each allowed domain.
    for allowed in ALLOWED_RETURN_DOMAINS:
        if host == allowed or host.endswith("." + allowed):
            return True
    return False

def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Build a redirect URL for SSO authentication.

    Parameters
    ----------
    login_endpoint : str
        The base SSO service endpoint URL.
    account_id : str
        Unique identifier for the user (will be passed as a query param).
    callback_url : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully formed redirect URL.

    Raises
    ------
    ValueError
        If the callback_url domain is not in ALLOWED_RETURN_DOMAINS.
    """
    if not _is_allowed_domain(callback_url):
        raise ValueError(
            f"Return URL domain is not allowed: {urllib.parse.urlparse(callback_url).hostname}"
        )

    # Construct the query parameters.
    params = {
        "account": account_id,
        "return_url": callback_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?&")  # keep URLs intact in return_url

    # Ensure the login_endpoint already contains a path; otherwise, add one.
    base = urllib.parse.urljoin(login_endpoint.rstrip("/") + "/", "")

    # Combine base and query string.
    redirect_url = f"{base}?{query_string}"
    return redirect_url