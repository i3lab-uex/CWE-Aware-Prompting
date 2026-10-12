import urllib.parse
from pathlib import Path

# Example set of allowed CDN domains. In a real application this would come from
# configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.provider.io",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a validated URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Unique identifier of the resource (e.g. a hash or filename).
    res_type : str
        Type of resource, used as a path component (e.g. "image" or "script").

    Returns
    -------
    str
        Fully resolved and validated URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain that is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url.rstrip("/"))
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url}")

    # Ensure the resource path is safe and does not contain traversal
    safe_res_type = Path(res_type).parts[-1]
    safe_res_id = Path(res_id).parts[-1]

    # Build the relative path: /<res_type>/<res_id>
    rel_path = f"/{safe_res_type}/{safe_res_id}"
    full_url = urllib.parse.urljoin(parsed_cdn.geturl(), rel_path)

    # Validate the domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(
            f"Disallowed CDN domain: {final_parsed.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url