import urllib.parse

# Domains that are permitted to receive the OAuth callback.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more trusted domains here.
}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Build a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_path : str
        The relative path to the OAuth callback handler (e.g., "/auth/callback").
    state : str
        A unique, cryptographically random string used to mitigate CSRF.

    Returns
    -------
    str
        The complete callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If any component is missing or if the resulting URL resolves to an untrusted domain.
    """
    # Basic validation
    if not base_url or not callback_path or not state:
        raise ValueError("base_url, callback_path, and state must be non‑empty")

    # Ensure the base URL has a scheme; default to https if missing.
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme:
        base_url = f"https://{base_url}"
        parsed_base = urllib.parse.urlparse(base_url)

    # Join the base URL with the callback path safely.
    joined = urllib.parse.urljoin(parsed_base.geturl(), callback_path)

    # Append the state parameter.
    url_parts = list(urllib.parse.urlparse(joined))
    query_params = urllib.parse.parse_qs(url_parts[4])
    query_params["state"] = [state]
    url_parts[4] = urllib.parse.urlencode(query_params, doseq=True)
    final_url = urllib.parse.urlunparse(url_parts)

    # Verify the resulting domain is allowed.
    final_parsed = urllib.parse.urlparse(final_url)
    netloc_clean = final_parsed.hostname
    if not netloc_clean or netloc_clean.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {netloc_clean}")

    return final_url