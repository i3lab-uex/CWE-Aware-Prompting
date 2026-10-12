import urllib.parse
from typing import Set

# A set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.safecdn.org",
    # add other trusted domains here
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully-qualified URL pointing to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the Content Delivery Network (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier of the specific resource (e.g., "logo.png", "main.js").
    res_category : str
        Category/type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The complete URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not target a domain listed in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the CDN base URL to extract components
    parsed_base = urllib.parse.urlparse(cdn_url)

    # Ensure the base URL includes a scheme; default to https if missing
    scheme = parsed_base.scheme or "https"
    netloc = parsed_base.netloc

    # If the user supplied a URL without scheme, the entire string might be in path
    if not netloc:
        # Assume the first part of the URL is the domain
        parts = parsed_base.path.split("/", 1)
        netloc = parts[0]
        path_from_url = "/" + parts[1] if len(parts) > 1 else ""

    # Validate the CDN domain
    if netloc.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Disallowed CDN domain: {netloc}")

    # Construct the path for the resource
    # Ensure there is exactly one slash between category and key
    safe_category = res_category.strip("/")
    safe_key = urllib.parse.quote(resource_key, safe="")  # encode key to be URL-safe
    resource_path = f"/{safe_category}/{safe_key}"

    # Combine the base URL with the resource path
    full_url = urllib.parse.urlunparse((
        scheme,
        netloc,
        resource_path,      # path
        "",                 # params
        "",                 # query
        ""                  # fragment
    ))

    return full_url

# Example usage (uncomment to test)
# print(build_external_resource_link("https://cdn.example.com/assets", "logo.png", "image"))