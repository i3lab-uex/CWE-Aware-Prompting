import urllib.parse
from typing import Set

# Example set of allowed CDN domains; replace with your actual list.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Identifier of the resource (e.g., a file name or hash).
    res_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Parse the base URL to extract its components.
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base!r}")

    # Ensure the scheme is HTTP(S) to avoid other protocols.
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_base.scheme}' in CDN base URL")

    # Verify that the domain is allowed.
    netloc = parsed_base.netloc.lower()
    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not in the list of allowed CDN domains")

    # Build a safe path by quoting each component.
    # The final path will look like: /{res_type}/{res_id}
    safe_res_type = urllib.parse.quote(res_type.strip(), safe="")
    safe_res_id   = urllib.parse.quote(res_id.strip(),  safe="")

    # Construct the relative path.
    relative_path = f"/{safe_res_type}/{safe_res_id}"

    # Join the base URL with the relative path.
    full_url = urllib.parse.urljoin(parsed_base.geturl(), relative_path)

    # Final validation: ensure the resulting URL's domain is still allowed.
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL points to disallowed domain: {final_parsed.netloc!r}")

    return full_url