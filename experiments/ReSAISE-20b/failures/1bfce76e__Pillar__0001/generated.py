import urllib.parse
from pathlib import Path

# Predefined set of safe CDN domains
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com/assets/"
    res_id : str
        Identifier of the resource, e.g. "logo.svg"
    res_type : str
        Type of resource (e.g., 'image', 'script'). Used only for validation.

    Returns
    -------
    str
        The absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the final URL does not resolve to a domain in ``ALLOWED_CDN_DOMAINS``.
    """

    # Ensure we are dealing with an absolute URL
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base}")

    # Validate the domain against allowed list
    if parsed_base.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not an allowed CDN domain")

    # Build a safe path by normalizing the resource identifier
    # This removes any leading slashes or relative components that could escape the base path.
    safe_res_id = str(Path(res_id).parts[-1])  # only keep the last component

    # Construct a new path relative to the base
    new_path = urllib.parse.urljoin(parsed_base.path + "/", safe_res_id)

    # Rebuild the full URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final domain check (in case the base had a different domain after join)
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Generated URL resolves to an unapproved domain: {final_parsed.netloc}")

    return final_url