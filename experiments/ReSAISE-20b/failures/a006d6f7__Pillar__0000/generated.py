import urllib.parse
from typing import Iterable

# ----------------------------------------------------------------------
# Configuration: list of CDN domains that are allowed to be used.
# ----------------------------------------------------------------------
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.somecdn.net",
}

# ----------------------------------------------------------------------
# Utility: normalize domain to lower‑case and strip port if present.
# ----------------------------------------------------------------------
def _normalize_domain(domain: str) -> str:
    """Return the host part of a domain, lower‑cased and without port."""
    if not domain:
        return ""
    host = domain.split(":")[0]  # strip port
    return host.lower()

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str
) -> str:
    """
    Construct a fully‑qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_origin_url : str
        Base CDN URL, e.g. "https://cdn.example.com".
    content_id : str
        Unique identifier for the resource, e.g. a hash or UUID.
    content_kind : str
        Resource type, e.g. "image" or "script".

    Returns
    -------
    str
        Validated, fully‑qualified CDN URL.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the origin URL to extract its components
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)

    # Ensure scheme is HTTP(S) only
    if parsed_origin.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_origin.scheme}")

    # Validate domain
    origin_domain = _normalize_domain(parsed_origin.netloc)
    if origin_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {origin_domain}")

    # Build the path: /<content_kind>/<content_id>
    # Ensure no leading/trailing slashes cause double slashes
    path_parts = [content_kind.strip("/"), content_id.strip("/")]
    resource_path = "/" + "/".join(part for part in path_parts if part)

    # Reconstruct the full URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_origin.scheme,
            parsed_origin.netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return full_url

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     url = generate_cdn_content_url(
#         "https://cdn.example.com",
#         "abc123def456",
#         "image"
#     )
#     print(url)  # Expected: https://cdn.example.com/image/abc123def456