import urllib.parse
from typing import Set

# Example set of allowed CDN domains. In a real application this should be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.s3.amazonaws.com"
}


def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a full URL for a CDN resource.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Unique identifier for the resource.
    res_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed CDN domain.
    """
    # Parse the base URL and validate its scheme
    parsed_base = urllib.parse.urlparse(base_cdn_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Ensure the base domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not an allowed CDN host")

    # Normalise the path: strip leading/trailing slashes to avoid double slashes
    base_path = parsed_base.path.rstrip("/")
    # Construct the relative path for the resource
    rel_path = f"{res_type.strip('/')}/{res_id.strip('/')}"

    # Join base path with relative path
    full_path = urllib.parse.urljoin(base_path + "/", rel_path)

    # Rebuild the URL
    full_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final check: ensure the domain of the final URL is still allowed
    parsed_final = urllib.parse.urlparse(full_url)
    if parsed_final.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL host '{parsed_final.hostname}' is not allowed")

    return full_url