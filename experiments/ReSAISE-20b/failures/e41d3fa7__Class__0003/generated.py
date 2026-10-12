import urllib.parse

# Trusted API domains and allowed endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "https://secure.api.net",  # fully qualified URLs are allowed
}

# Allowed endpoint paths (relative to the base URL)
ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/inventory",
    "/search",
}


def generate_redirect_link(base_url: str, endpoint_path: str,
                           query_info: dict | None = None) -> str:
    """
    Build a full redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL, e.g. "https://api.example.com".
    endpoint_path : str
        The desired API endpoint, e.g. "/users".
    query_info : dict | None, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # 1. Parse the base URL and ensure it is well‑formed
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # 2. Validate domain
    base_domain = parsed_base.netloc.lower()
    if not any(base_domain == dom.lower() or
               (dom.startswith("https://") and base_domain == urllib.parse.urlparse(dom).netloc.lower())
               for dom in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{base_domain}' is not approved")

    # 3. Normalize endpoint path
    if not endpoint_path.startswith("/"):
        raise ValueError(f"Endpoint path must start with '/': {endpoint_path}")
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # 4. Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint_path.lstrip("/"))

    # 5. Construct the query string
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        query_string = urllib.parse.urlencode(query_info, doseq=True)
    else:
        query_string = ""

    # 6. Assemble the final URL
    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    ))

    return redirect_url