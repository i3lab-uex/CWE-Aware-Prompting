import urllib.parse
from typing import Set

# Define the set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.mycompany.net",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_id : str
        Identifier of the resource to fetch (e.g. "logo.png").
    resource_type : str
        Type of the resource, used to build a sub‑path. Accepted values are
        ``image``, ``script`` and ``style``.

    Returns
    -------
    str
        The absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not resolve to a domain in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Normalise the base URL to ensure it ends with a slash
    normalized_base = cdn_base_url.rstrip("/") + "/"

    # Map resource types to sub‑paths; default to 'assets'
    type_path_map = {
        "image": "images",
        "script": "js",
        "style":  "css",
    }
    sub_path = type_path_map.get(resource_type.lower(), "assets")

    # Build the relative path to the resource
    relative_path = urllib.parse.urljoin(f"{sub_path}/", resource_id)

    # Resolve the final absolute URL
    full_url = urllib.parse.urljoin(normalized_base, relative_path)

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)
    domain = parsed.hostname

    # Validate the domain against the whitelist
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{domain}'. "
            f"Allowed domains: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    return full_url