import urllib.parse
from typing import Iterable

# List of CDN domains that are allowed to serve resources.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a secure URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com".
    res_id : str
        Unique identifier for the resource (e.g. a hash or UUID).
    res_type : str
        Resource type, e.g. "image", "script".

    Returns
    -------
    str
        The fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS`` or if
        the URL construction fails due to malformed inputs.
    """
    # Parse the base CDN URL and validate scheme
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if parsed_cdn.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_cdn.scheme}'. Only http/https are allowed.")

    # Normalise the netloc (domain) and compare against allowed list
    domain = parsed_cdn.hostname or ""
    if not any(domain == allowed or domain.endswith("." + allowed) for allowed in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not an authorized CDN domain.")

    # Sanitize the resource identifier and type
    safe_res_id = urllib.parse.quote(res_id, safe="")
    safe_res_type = urllib.parse.quote_plus(res_type)

    # Build the path: /{res_type}/{res_id}
    new_path = urllib.parse.urljoin(parsed_cdn.path + "/", f"{safe_res_type}/{safe_res_id}")

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url