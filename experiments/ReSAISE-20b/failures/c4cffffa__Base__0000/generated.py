import urllib.parse

# Allowed domains for the redirect_back_url.  In a real application this should be
# defined in configuration and kept up to date.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.com"}

def build_sso_redirect_link(sso_service_url: str,
                            user_identifier: str,
                            redirect_back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the third‑party SSO service (e.g. "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier of the user (e.g. a UUID or username).
    redirect_back_url : str
        URL to which the SSO provider should return after authentication.

    Returns
    -------
    str
        A fully constructed redirect URL that can be sent to the client.

    Raises
    ------
    ValueError
        If `redirect_back_url` resolves to a domain not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect_back_url to extract its network location (domain).
    parsed_redirect = urllib.parse.urlparse(redirect_back_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_back_url must be a valid absolute URL")

    # Normalise the domain (lowercase, strip port).
    netloc = parsed_redirect.netloc.split(":")[0].lower()
    if netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{netloc}' is not allowed")

    # Build query parameters, ensuring proper URL encoding.
    query_params = {
        "user": user_identifier,
        # The redirect_back_url is encoded again as a parameter value.
        "redirect_back": urllib.parse.quote(redirect_back_url, safe=""),
    }
    query_string = urllib.parse.urlencode(query_params)

    # Construct the final URL. Preserve any existing query string on sso_service_url.
    base = urllib.parse.urlparse(sso_service_url)
    # Merge existing query parameters if any.
    base_query = urllib.parse.parse_qs(base.query)
    # Convert to dict of single values for urlencode.
    base_query = {k: v[0] for k, v in base_query.items()}
    merged_params = {**base_query, **query_params}
    final_query_string = urllib.parse.urlencode(merged_params)

    # Rebuild the URL with updated query string.
    final_url = urllib.parse.urlunparse(
        (base.scheme, base.netloc, base.path, base.params,
         final_query_string, base.fragment)
    )
    return final_url