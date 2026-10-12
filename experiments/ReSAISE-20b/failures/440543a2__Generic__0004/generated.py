import urllib.parse
from typing import Dict, Optional

# Define the set of approved API domains and list of allowed endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/status",
]

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API URL by joining the base_url with a given endpoint path
    and optional query parameters.

    Parameters
    ----------
    base_url : str
        The root URL of the API, e.g. "https://api.example.com".
    path : str
        The endpoint path to be appended, e.g. "/users".
    params : dict or None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully-qualified URL ready for use in a redirect or request.

    Raises
    ------
    ValueError
        If the domain of the final URL is not in `APPROVED_API_DOMAINS` or
        if the endpoint path is not in `ALLOWED_ENDPOINTS`.
    """
    # Ensure base_url has a scheme
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (e.g., https://)")

    # Resolve domain
    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Normalize and validate path
    normalized_path = urllib.parse.urljoin("/", path)  # ensures leading slash
    if not any(normalized_path.startswith(ep) for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # Build the full URL
    url_without_query = urllib.parse.urljoin(parsed_base.geturl(), normalized_path)

    if params:
        # Ensure all values are strings and encode safely
        safe_params = {k: str(v) for k, v in params.items()}
        query_string = urllib.parse.urlencode(safe_params)
        final_url = f"{url_without_query}?{query_string}"
    else:
        final_url = url_without_query

    # Final safety check: parse again to ensure no unintended redirects
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.netloc.lower() != domain:
        raise ValueError("Redirect would lead to a different domain")

    return final_url