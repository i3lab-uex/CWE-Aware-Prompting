import urllib.parse
from typing import Iterable

# List of CDN domains that are considered safe for use.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a fully-qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN. May include scheme, host and optional path.
    res_id : str
        Unique identifier of the resource. Must be URL-safe.
    res_type : str
        Resource type (e.g., 'image', 'script'). Used as part of the path.

    Returns
    -------
    str
        Fully-qualified URL to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    if not cdn_url:
        raise ValueError("cdn_url must be a non-empty string")

    if not res_id:
        raise ValueError("res_id must be a non-empty string")

    if not res_type:
        raise ValueError("res_type must be a non-empty string")

    # Ensure the CDN URL has a scheme; default to https if missing.
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    scheme = parsed_cdn.scheme or "https"
    netloc = parsed_cdn.netloc
    path = parsed_cdn.path.rstrip("/")
    base_url = f"{scheme}://{netloc}{path}"

    # Build the relative path for the resource
    # Use quote to ensure special characters are encoded.
    safe_res_id = urllib.parse.quote(res_id, safe="")
    relative_path = f"/{res_type}/{safe_res_id}"

    # Join the base URL with the relative path
    full_url = urllib.parse.urljoin(base_url + "/", relative_path)

    # Validate the domain of the constructed URL
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {final_parsed.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url