import urllib.parse
from pathlib import Path

# Example set of allowed CDN domains. In production this should be defined in configuration.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Build a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_key : str
        Identifier of the specific resource (e.g. "logo.png").
    res_category : str
        Category/type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully constructed URL pointing to the resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in ALLOWED_CDN_DOMAINS or if the URL scheme
        is not HTTP/HTTPS.
    """
    # Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Validate scheme
    if parsed_cdn.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed_cdn.scheme}'. Only http/https are allowed.")

    # Validate domain
    netloc = parsed_cdn.hostname
    if not netloc or netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not an allowed CDN domain.")

    # Construct the path safely
    # Use pathlib.Path to normalize slashes and avoid double slashes
    resource_path = Path(res_category).joinpath(resource_key)

    # Ensure the path starts with a slash
    resource_path_str = str(resource_path).lstrip("/")
    full_path = f"/{resource_path_str}"

    # Rebuild the URL with the new path
    rebuilt = parsed_cdn._replace(path=full_path)
    full_url = urllib.parse.urlunparse(rebuilt)

    # Final safety check: re-validate the domain after reconstruction
    final_netloc = urllib.parse.urlparse(full_url).hostname
    if final_netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Resulting URL points to an untrusted domain.")

    return full_url