import urllib.parse
from typing import Iterable

# Define the set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.secure.net",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        A unique identifier for the resource (e.g., a file name or hash).
    res_type : str
        The type of resource, used to prefix the path (e.g., "image", "script").

    Returns
    -------
    str
        A validated, absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ALLOWED_CDN_DOMAINS.
    """
    # Ensure the base CDN URL ends with a slash so that urljoin behaves as expected.
    if not cdn_url.endswith("/"):
        base = f"{cdn_url}/"
    else:
        base = cdn_url

    # Construct the relative path: <res_type>/<res_id>
    rel_path = urllib.parse.quote(f"{res_type}/{res_id}")

    # Build the absolute URL
    full_url = urllib.parse.urljoin(base, rel_path)

    # Parse out the domain (netloc) from the resulting URL
    parsed = urllib.parse.urlparse(full_url)
    domain = parsed.netloc.lower()

    # If the URL contains a port, strip it for comparison
    if ":" in domain:
        domain = domain.split(":")[0]

    # Verify that the domain is within the allowed list
    if domain not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Unauthorized CDN domain: {domain}")

    return full_url