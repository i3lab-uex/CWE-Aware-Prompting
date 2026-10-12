import urllib.parse
from pathlib import Path

# Example set of allowed CDN domains (subdomains are acceptable)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.cdnprovider.net",
    "static.myapp.org"
}


def construct_external_resource_url(cdn_base_url: str,
                                    resource_id: str,
                                    resource_type: str) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_id : str
        The unique identifier of the requested resource.
    resource_type : str
        Type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain,
        or if user input attempts to override the scheme/netloc.
    """
    # Normalize and validate base URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("cdn_base_url must include scheme and netloc")

    # Prevent user input from changing the base domain
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError("cdn_base_url must use http or https scheme")

    # Build the path safely
    safe_path = Path(resource_type).joinpath(resource_id)
    # Ensure no leading slashes that could override the base path
    safe_path_str = str(safe_path).lstrip("/")

    # Construct the full URL
    full_url = urllib.parse.urljoin(parsed_base.geturl() + "/", safe_path_str)

    # Parse the resulting URL to validate domain
    parsed_full = urllib.parse.urlparse(full_url)
    host = parsed_full.hostname

    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"URL points to disallowed domain: {host}")

    return full_url