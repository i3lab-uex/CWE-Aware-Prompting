import urllib.parse
from typing import Set

# A predefined set of allowed CDN domains.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.somedomain.net",
}

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str,
) -> str:
    """
    Construct a fully‑qualified CDN URL for a resource and validate that
    the resulting host belongs to an allowed CDN domain.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier of the resource (e.g. "logo.png" or "app.min.js").
    resource_kind : str
        Kind of resource, e.g. 'image' or 'script'. This is used only for
        path normalization and can be extended to enforce stricter rules.

    Returns
    -------
    str
        The fully qualified URL pointing at the resource on the CDN.

    Raises
    ------
    ValueError
        If the resolved URL does not point to a host listed in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Normalise the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url!r}")

    # Ensure the resource identifier does not start with a leading slash
    # to avoid accidentally overriding the base path.
    resource_identifier = resource_identifier.lstrip("/")

    # Build the relative path. For example, for an image we might
    # prefix with "images/" or for a script "scripts/". This is optional.
    kind_prefix = {
        "image": "images/",
        "script": "scripts/",
    }.get(resource_kind.lower(), "")

    relative_path = urllib.parse.urljoin(kind_prefix, resource_identifier)

    # Construct the full URL
    full_url = urllib.parse.urljoin(parsed_base.geturl() + "/", relative_path)

    # Validate the host
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {parsed_full.netloc!r} not in "
            f"{sorted(ALLOWED_CDN_DOMAINS)}"
        )

    return full_url