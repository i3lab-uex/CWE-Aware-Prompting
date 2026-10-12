import re
from urllib.parse import urlparse, urljoin

# A set of CDN domains that are allowed to host resources.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

# Regular expression to validate the resource ID.
# Only alphanumeric characters, hyphens and underscores are allowed.
RES_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a fully qualified URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g. "https://cdn.example.com/").
    res_id : str
        Unique identifier for the resource.
    res_type : str
        Resource type (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ALLOWED_CDN_DOMAINS,
        or if ``res_id`` contains disallowed characters.
    """
    # 1. Validate the resource ID.
    if not RES_ID_PATTERN.match(res_id):
        raise ValueError("Invalid res_id: only alphanumerics, hyphens and underscores are allowed")

    # 2. Normalize the base CDN URL.
    parsed_cdn = urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError("cdn_url must be a valid absolute URL")

    # 3. Ensure the CDN domain is allowed.
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_cdn.hostname}")

    # 4. Construct the relative path for the resource.
    # Use slash normalization to avoid double slashes or missing separators.
    relative_path = f"{res_type.strip('/')}/{res_id}"
    # Ensure the base ends with a slash to preserve relative path semantics.
    base_url = cdn_url.rstrip("/") + "/"

    # 5. Join the base URL with the relative path.
    full_url = urljoin(base_url, relative_path)

    # 6. Final sanity check: the resulting URL must still resolve to an allowed domain.
    final_parsed = urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Resulting URL points to an unauthorized domain")

    return full_url