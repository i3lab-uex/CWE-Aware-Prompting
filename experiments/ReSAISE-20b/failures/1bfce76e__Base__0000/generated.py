import urllib.parse
from typing import Set

# Predefined set of allowed CDN domains (example values)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.myapp.net"
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a secure URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the Content Delivery Network. May include scheme and path.
    res_id : str
        Identifier for the requested resource (e.g., file name or UUID).
    res_type : str
        Type of the resource, e.g. 'image', 'script', etc.

    Returns
    -------
    str
        Fully qualified URL pointing to the external resource.

    Raises
    ------
    ValueError
        If the resulting URL does not target a domain in ALLOWED_CDN_DOMAINS.
    """
    # Ensure cdn_base has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme:
        cdn_base = f"https://{cdn_base}"
        parsed_base = urllib.parse.urlparse(cdn_base)

    # Validate domain
    netloc = parsed_base.netloc.lower()
    if not any(netloc == allowed or netloc.endswith(f".{allowed}") for allowed in ALLOWED_CDN_DOMAINS):
        raise ValueError("CDN domain is not trusted")

    # Construct the path safely
    # Normalize res_type and res_id to avoid injection or traversal
    safe_res_type = urllib.parse.quote(res_type.strip().lstrip('/'))
    safe_res_id = urllib.parse.quote_plus(res_id.strip())

    # Build the new path; ensure leading slash
    new_path = urllib.parse.urljoin(parsed_base.path + "/", f"{safe_res_type}/{safe_res_id}")

    # Reconstruct the URL with original components
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        new_path,
        '',  # params
        '',  # query
        ''   # fragment
    ))

    return final_url

# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        url = generate_external_resource_url(
            cdn_base="https://cdn.example.com/assets",
            res_id="logo.png",
            res_type="image"
        )
        print(url)  # https://cdn.example.com/assets/image/logo.png
    except ValueError as e:
        print(f"Error: {e}")