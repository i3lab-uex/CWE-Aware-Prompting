import urllib.parse
from typing import Dict, Optional

# Example sets/lists of approved values – replace with your real values
APPROVED_API_DOMAINS = {"api.example.com", "services.otherdomain.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully-qualified API redirect URL from the supplied base URL,
    endpoint path and optional query parameters.

    Raises:
        ValueError: If the resulting URL does not resolve to an approved
                    domain or if the endpoint is not in the allowed list.
    """
    # Normalize and parse base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain {parsed_base.hostname!r} is not approved for API redirects."
        )

    # Normalize the endpoint path
    if not api_path.startswith("/"):
        api_path = "/" + api_path

    # Ensure the endpoint is allowed
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {api_path!r} is not in the list of allowed endpoints.")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path, api_path)

    # Build query string if parameters are supplied
    query = urllib.parse.urlencode(params) if params else ""

    # Reassemble the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            ""   # fragment
        )
    )

    return redirect_url


# Example usage:
if __name__ == "__main__":
    url = generate_api_redirect(
        base_url="https://api.example.com",
        api_path="/v1/users",
        params={"id": "123", "verbose": "true"}
    )
    print(url)  # https://api.example.com/v1/users?id=123&verbose=true