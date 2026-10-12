import urllib.parse
from typing import Set

# Example set of allowed CDN domains. In a real system this would be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content-provider.org"
}

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str
) -> str:
    """
    Build a fully qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier of the resource (e.g., "logo.png" or "main.js").
    resource_kind : str
        The type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not belong to an allowed CDN domain,
        or if the scheme is not HTTP(S).
    """
    # Normalise and parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or parsed_base.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed_base.scheme}'. Only http and https are allowed.")

    # Validate the domain against the whitelist
    hostname = parsed_base.hostname or ""
    if hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an allowed CDN.")

    # Construct the path safely: ensure no leading slashes in resource_identifier
    clean_resource = resource_identifier.lstrip("/")
    # Combine the base path with the resource identifier and kind
    # e.g., /images/logo.png or /scripts/main.js
    resource_path = urllib.parse.urljoin(f"{parsed_base.path.rstrip('/')}/", f"{resource_kind}/{clean_resource}")

    # Rebuild the URL with the new path
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            cdn_url="https://cdn.example.com/assets/",
            resource_identifier="/logo.png",
            resource_kind="images"
        )
        print(url)  # https://cdn.example.com/assets/images/logo.png
    except ValueError as e:
        print(f"URL construction failed: {e}")