import urllib.parse
from typing import Iterable

# Define a set of allowed CDN domains.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.othersite.net",
}


def generate_cdn_content_url(
    cdn_origin_url: str, content_id: str, content_kind: str
) -> str:
    """
    Construct a fully qualified URL for a resource on an external CDN.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    content_id : str
        The unique identifier of the resource.
    content_kind : str
        The type of resource, used as a sub‑path component (e.g. "image" or "script").

    Returns
    -------
    str
        The fully resolved and validated URL pointing to the requested content.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure the base URL has a scheme; default to https if missing.
    parsed_base = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_base.scheme:
        cdn_origin_url = f"https://{cdn_origin_url}"
        parsed_base = urllib.parse.urlparse(cdn_origin_url)

    # Normalise the path: join kind and id ensuring no leading/trailing slashes.
    path = urllib.parse.urljoin(f"/{content_kind}/", content_id)

    # Build the final URL.
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # Validate the domain.
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {parsed_base.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url