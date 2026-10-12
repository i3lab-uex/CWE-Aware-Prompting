import urllib.parse

# ----------------------------------------------------------------------
# Configuration – replace these with your actual values.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {"api.example.com", "api.secure.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v1/products",
]

# ----------------------------------------------------------------------
def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: dict | None = None
) -> str:
    """
    Construct a fully-qualified API redirect URL.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        Specific API endpoint path (e.g. "/v1/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully-qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the final URL points to an unapproved domain or disallowed endpoint.
    """
    # Normalise and validate the base URL
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {api_base_url!r}")

    # Ensure the domain is approved
    domain = parsed_base.hostname.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not approved")

    # Normalise and validate the endpoint
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    # Strip any query string or fragment from the supplied endpoint
    endpoint_path = urllib.parse.urlparse(endpoint).path

    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {endpoint_path!r} is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path, endpoint_path)

    # Merge query parameters
    base_query = urllib.parse.parse_qs(parsed_base.query)
    if query_params:
        # `urllib.parse.urlencode` expects a sequence of two-element tuples.
        # Flatten values that are lists into multiple key/value pairs.
        flat_params = []
        for k, v in query_params.items():
            if isinstance(v, (list, tuple)):
                flat_params.extend([(k, str(item)) for item in v])
            else:
                flat_params.append((k, str(v)))
        merged_query = urllib.parse.urlencode(
            {**{k: v[0] for k, v in base_query.items()}, **dict(flat_params)},
            doseq=True,
        )
    else:
        merged_query = urllib.parse.urlencode(base_query, doseq=True)

    # Reconstruct the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            merged_query,
            "",  # fragment
        )
    )

    return redirect_url

# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    url = build_api_redirect_url(
        api_base_url="https://api.example.com",
        endpoint="/v1/users",
        query_params={"page": 2, "sort": ["name", "date"]},
    )
    print(url)