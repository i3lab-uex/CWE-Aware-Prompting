import urllib.parse

# Domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more allowed domains as needed.
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g. "https://myapp.com").
    callback_path : str
        The relative path for the OAuth callback (e.g. "/auth/callback").
    state : str
        A unique opaque value that should be sent back by the OAuth provider.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed domain.
    """
    # Ensure base_url ends with a slash so that urljoin behaves correctly
    if not base_url.endswith("/"):
        base_url += "/"

    # Join the base URL with the callback path
    joined = urllib.parse.urljoin(base_url, callback_path)

    # Parse the URL components
    parsed = urllib.parse.urlparse(joined)

    # Verify that the domain is allowed
    netloc = parsed.netloc.lower()
    # Strip port if present for comparison
    domain = netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{domain}' is not allowed")

    # Preserve existing query parameters and add the state
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # parse_qs returns lists for each key; we want single values
    query_params = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}
    query_params["state"] = state

    # Build the new query string
    new_query = urllib.parse.urlencode(query_params, doseq=False)

    # Reconstruct the full URL
    new_parsed = parsed._replace(query=new_query)
    return urllib.parse.urlunparse(new_parsed)


# Example usage (for testing only, remove or guard with __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        url = create_oauth_callback_url(
            base_url="https://myapp.com",
            callback_path="/oauth/callback",
            state="xyz123"
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid callback URL: {exc}")