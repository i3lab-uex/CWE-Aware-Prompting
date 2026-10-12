import urllib.parse
import posixpath

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.safesite.org"
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    resource_key : str
        Identifier of the specific resource (file name or path fragment).
    res_category : str
        Category of the resource, e.g. "image", "script".

    Returns
    -------
    str
        A fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not point to an allowed CDN domain.
    """
    # Normalize inputs
    cdn_url = cdn_url.rstrip('/') + '/'
    res_category = res_category.strip('/')
    resource_key = resource_key.lstrip('/')

    # Prevent path traversal by normalizing the constructed path
    safe_path = posixpath.normpath(f"/{res_category}/{resource_key}")
    if safe_path.startswith(".."):
        raise ValueError("Resource key attempts to traverse outside the base path")

    # Build the full URL
    url = urllib.parse.urljoin(cdn_url, safe_path.lstrip('/'))

    # Parse the URL to verify its domain
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed.netloc}' is not in the list of allowed CDN domains")

    return url