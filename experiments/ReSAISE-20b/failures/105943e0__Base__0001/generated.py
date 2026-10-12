import urllib.parse

# Domains that are allowed as callback URLs.  Add more domains as needed.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service endpoint.
    account_id : str
        The unique identifier for the user.
    callback_url : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the callback URL to extract its domain.
    parsed_callback = urllib.parse.urlparse(callback_url)
    if not parsed_callback.scheme or not parsed_callback.netloc:
        raise ValueError("callback_url must be a fully-qualified URL")

    # Normalize the domain (lowercase, remove port if present).
    netloc = parsed_callback.netloc.split(":")[0].lower()
    if netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not allowed as a return URL")

    # Build the query parameters for the SSO endpoint.
    query_params = {
        "accountId": account_id,
        # Use the entire callback URL as a query value; percent‑encode it.
        "returnUrl": callback_url,
    }

    # Parse the login endpoint to ensure we can safely add query parameters.
    parsed_login = urllib.parse.urlparse(login_endpoint)
    # Merge any existing query parameters with the new ones.
    existing_query = urllib.parse.parse_qs(parsed_login.query, keep_blank_values=True)
    # parse_qs returns lists; flatten for simplicity.
    merged_query = {k: v[0] if isinstance(v, list) else v for k, v in existing_query.items()}
    merged_query.update(query_params)

    # Construct the final URL.
    new_url = urllib.parse.urlunparse(
        (
            parsed_login.scheme,
            parsed_login.netloc,
            parsed_login.path,
            parsed_login.params,
            urllib.parse.urlencode(merged_query, doseq=True),
            parsed_login.fragment,
        )
    )

    return new_url