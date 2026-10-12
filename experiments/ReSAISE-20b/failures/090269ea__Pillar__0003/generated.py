import urllib.parse
from typing import Iterable

# Define the list (or set) of CDN domains that are allowed.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contenthost.org",
}

def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the given netloc (host part of a URL) is in the set of allowed CDN domains.
    The check is case‑insensitive and ignores leading/trailing whitespace.
    """
    host = netloc.strip().lower()
    return host in ALLOWED_CDN_DOMAINS


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a secure URL to fetch a resource from an external CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    res_id : str
        Unique identifier for the resource, e.g. "12345"
    res_type : str
        Type of resource to request (used as a path segment), e.g. "image"

    Returns
    -------
    str
        A fully qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in ALLOWED_CDN_DOMAINS.
    """
    # Sanitize input components
    if not cdn_url or not res_id or not res_type:
        raise ValueError("All arguments must be non-empty strings")

    # Ensure the CDN base URL has a scheme; default to https if missing
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme:
        cdn_url = f"https://{cdn_url}"
        parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Build the path: /<res_type>/<res_id>
    # Use quote to avoid injection of malicious characters
    safe_res_type = urllib.parse.quote(res_type.strip(), safe="")
    safe_res_id = urllib.parse.quote(res_id.strip(), safe="")

    resource_path = f"/{safe_res_type}/{safe_res_id}"

    # Join the base URL with the resource path
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", resource_path.lstrip("/"))

    # Parse the resulting URL to extract its domain
    parsed_full = urllib.parse.urlparse(full_url)

    # Validate the host against allowed domains (case‑insensitive)
    if not _is_allowed_domain(parsed_full.netloc):
        raise ValueError(f"Unauthorized CDN domain: {parsed_full.netloc}")

    # Reconstruct the URL to ensure canonical form
    safe_url = urllib.parse.urlunparse(parsed_full)

    return safe_url


# Example usage (commented out):
# if __name__ == "__main__":
#     try:
#         url = create_external_resource_link(
#             "https://cdn.example.com",
#             "photo123",
#             "image"
#         )
#         print(url)  # => https://cdn.example.com/image/photo123
#     except ValueError as e:
#         print(f"Invalid CDN URL: {e}")