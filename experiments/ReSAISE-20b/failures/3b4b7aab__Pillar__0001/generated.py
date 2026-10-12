import urllib.parse

# Example set of domains that are permitted for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost:8000",  # allow local dev
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g. "https://app.example.com").
    callback_uri : str
        The relative path to the OAuth callback endpoint (e.g. "/oauth/callback").
    session_state : str
        A unique value to be appended as a query parameter for CSRF protection.

    Returns
    -------
    str
        The complete callback URL, e.g.
        "https://app.example.com/oauth/callback?state=abc123".

    Raises
    ------
    ValueError
        If the domain of the resulting URL is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Join the base URL and callback path safely.
    full_url = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL into components.
    parsed = urllib.parse.urlparse(full_url)

    # Ensure the domain (netloc) is allowed.
    if parsed.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {parsed.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    # Parse existing query parameters (if any) and add the state param.
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # parse_qs returns values as lists; convert to simple list for urlencode.
    query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
    query_params["state"] = session_state

    # Rebuild the URL with updated query string.
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    rebuilt = parsed._replace(query=new_query)

    return urllib.parse.urlunparse(rebuilt)


# Example usage (would normally be in a separate test or application code):
if __name__ == "__main__":
    try:
        callback = construct_oauth_callback_uri(
            root_url="https://app.example.com",
            callback_uri="/oauth/callback",
            session_state="xyz123abc"
        )
        print("Constructed callback URL:", callback)
    except ValueError as e:
        print("Error constructing callback URL:", e)