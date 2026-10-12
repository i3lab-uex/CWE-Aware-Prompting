import urllib.parse
from typing import Set

# Pre‑defined set of allowed CDN domains.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str
) -> str:
    """
    Construct a fully‑qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g., "https://cdn.example.com").
    resource_identifier : str
        Unique identifier for the requested resource.
    resource_kind : str
        Type of resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully resolved CDN URL.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed CDN domain,
        or if the base URL is malformed.
    """
    # Validate and parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url}")

    # Ensure the scheme is HTTP(S) only
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_base.scheme}' in CDN URL")

    # Normalize the path to ensure it ends with a slash
    base_path = parsed_base.path.rstrip("/") + "/"

    # Encode the resource identifier to avoid injection or path traversal
    safe_identifier = urllib.parse.quote(resource_identifier, safe="")

    # Build the relative path: e.g., "image/<id>"
    rel_path = f"{resource_kind.rstrip('/')}/{safe_identifier}"

    # Join the base and relative path
    full_url = urllib.parse.urljoin(parsed_base._replace(path=base_path).geturl(), rel_path)

    # Re‑parse to extract the netloc for domain validation
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL domain '{parsed_full.netloc}' is not an allowed CDN"
        )

    return full_url