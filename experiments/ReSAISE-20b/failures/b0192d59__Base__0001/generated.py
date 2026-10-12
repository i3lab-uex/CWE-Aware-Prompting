import urllib.parse

# ------------------------------------------------------------
# Configuration – only allow known, trusted domains and endpoints.
# ------------------------------------------------------------

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/status",
]


def generate_api_redirect_uri(base_uri: str, api_endpoint: str, query: dict | None = None) -> str:
    """
    Assemble a secure API redirect URL.

    Parameters
    ----------
    base_uri : str
        The base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The path to the desired endpoint (e.g. "/v1/users").
    query : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully assembled URL.

    Raises
    ------
    ValueError
        If the base domain or endpoint is not approved.
    """
    # ------------------------------------------------------------------
    # 1. Validate the base URI – ensure it has a scheme and an approved domain.
    # ------------------------------------------------------------------
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri!r}")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved base domain: {domain!r}")

    # ------------------------------------------------------------------
    # 2. Validate the endpoint – it must be in the whitelist.
    # ------------------------------------------------------------------
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {api_endpoint!r}")

    # ------------------------------------------------------------------
    # 3. Construct the new path by joining the base path and endpoint.
    # ------------------------------------------------------------------
    base_path = parsed_base.path.rstrip("/")
    new_path = api_endpoint if api_endpoint.startswith("/") else "/" + api_endpoint
    # urljoin requires a trailing slash on the base to treat it as a directory.
    full_path = urllib.parse.urljoin(base_path + "/", new_path.lstrip("/"))

    # ------------------------------------------------------------------
    # 4. Encode query parameters (if any) – urllib handles escaping.
    # ------------------------------------------------------------------
    encoded_query = ""
    if query:
        try:
            # Ensure all keys/values are strings; raise if not.
            encoded_query = urllib.parse.urlencode(
                {str(k): str(v) for k, v in query.items()}
            )
        except Exception as exc:
            raise ValueError(f"Invalid query parameters: {exc}") from exc

    # ------------------------------------------------------------------
    # 5. Reconstruct the final URL.
    # ------------------------------------------------------------------
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params
            encoded_query,
            "",          # fragment
        )
    )

    return final_url