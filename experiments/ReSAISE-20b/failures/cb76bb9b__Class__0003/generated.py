import urllib.parse
from typing import Set

# Example set of allowed CDN domains. Replace with the real ones.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully qualified URL for a CDN resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Unique identifier of the resource (e.g., "12345").
    res_type : str
        Type of the resource, used to construct the path (e.g., "image" or "script").

    Returns
    -------
    str
        The fully qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in ALLOWED_CDN_DOMAINS or if any component is malformed.
    """
    # 1. Sanitize inputs: strip whitespace and ensure they are strings
    if not all(isinstance(arg, str) for arg in (base_cdn_url, res_id, res_type)):
        raise ValueError("All arguments must be strings.")

    base_cdn_url = base_cdn_url.strip()
    res_id = res_id.strip().lstrip("/")  # avoid leading slash
    res_type = res_type.strip().rstrip("/") + "/"  # ensure trailing slash

    # 2. Construct a provisional URL using urljoin
    provisional_path = urllib.parse.urljoin(res_type, res_id)
    provisional_url = urllib.parse.urljoin(base_cdn_url.rstrip("/") + "/", provisional_path)

    # 3. Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(provisional_url)

    # 4. Validate the scheme (must be http or https)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 5. Validate the network location (netloc) against allowed domains
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {hostname}")

    # 6. Reconstruct the URL to ensure canonical form
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        hostname,          # use lowercase to avoid case issues
        urllib.parse.quote(parsed.path),  # encode path segments
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))

    return safe_url