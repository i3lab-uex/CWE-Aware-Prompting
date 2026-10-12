import urllib.parse
from typing import Iterable

# Allowed CDN domains – populate with the actual trusted domains.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    # add more domains as required
}


def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Assemble a secure URL to fetch a resource from an approved CDN.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    content_id : str
        Unique identifier for the requested resource.
    content_kind : str
        Type of resource, e.g. "image", "script".

    Returns
    -------
    str
        Fully-qualified, validated URL pointing to the requested content.

    Raises
    ------
    ValueError
        If the resolved URL points to an unauthorized domain or if the input is malformed.
    """
    # Parse and normalise the origin URL
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url}")

    # Ensure the domain is in the whitelist
    domain = parsed_origin.netloc.lower()
    if domain not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Domain '{domain}' is not an allowed CDN host")

    # Normalise the content kind and ID to avoid path traversal or injection
    safe_kind = urllib.parse.quote_plus(content_kind.strip().lower())
    safe_id = urllib.parse.quote_plus(content_id.strip())

    # Construct the relative path. We avoid leading slashes to keep urljoin behaviour
    relative_path = f"{safe_kind}/{safe_id}"

    # Build the final URL, preserving scheme and netloc
    full_url = urllib.parse.urljoin(
        f"{parsed_origin.scheme}://{parsed_origin.netloc}/",
        relative_path
    )

    # Final sanity check: parse again and confirm host matches the original domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() != domain:
        raise ValueError("URL resolution changed the host to an unauthorized domain")

    return full_url