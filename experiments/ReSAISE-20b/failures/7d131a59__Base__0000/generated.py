import urllib.parse

# Example set of domains that are allowed for OAuth callbacks.
# In a real application this should be populated with the actual
# domains that are considered safe for redirects.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "sub.example.org"}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL that includes the provided
    `state` parameter and validates that the resulting domain is in
    ALLOWED_CALLBACK_DOMAINS.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_path : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    state : str
        A unique, opaque string used to maintain state between the request
        and callback.

    Returns
    -------
    str
        The fully constructed OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain not in
        ALLOWED_CALLBACK_DOMAINS.
    """
    # Normalise the base URL (ensure it ends with a slash so urljoin works)
    if not base_url.endswith("/"):
        base_url = f"{base_url}/"

    # Build the path with the state query parameter
    # Use urllib.parse to avoid manual string concatenation errors.
    path_with_state = urllib.parse.urljoin(callback_path, "")
    query = urllib.parse.urlencode({"state": state})
    full_path = f"{path_with_state}?{query}"

    # Join base URL and path to get the absolute callback URL
    callback_url = urllib.parse.urljoin(base_url, full_path)

    # Parse the resulting URL to extract the domain
    parsed = urllib.parse.urlparse(callback_url)
    netloc = parsed.netloc

    # Handle URLs that include port numbers (e.g., example.com:8080)
    domain = netloc.split(":")[0]

    if domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{domain}' is not allowed")

    return callback_url