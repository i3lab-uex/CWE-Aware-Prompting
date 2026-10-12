import urllib.parse
from typing import Iterable

# A set of domains that are trusted to host CDN resources.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somesite.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully-qualified URL to access a CDN resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN, e.g. "https://cdn.example.com/".
    file_id : str
        A unique identifier for the resource. Should be URL-safe.
    file_type : str
        The type of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        The absolute URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme:
        parsed_base = parsed_base._replace(scheme="https")
        cdn_url_base = urllib.parse.urlunparse(parsed_base)

    # Build the relative path for the resource.
    # Use quote to safely encode any unsafe characters in file_id or file_type.
    safe_file_type = urllib.parse.quote(file_type.strip("/"))
    safe_file_id = urllib.parse.quote(file_id.strip("/"))
    relative_path = f"/{safe_file_type}/{safe_file_id}"

    # Join the base URL with the relative path.
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Validate the resolved domain.
    resolved_netloc = urllib.parse.urlparse(full_url).netloc.lower()
    if resolved_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {resolved_netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url