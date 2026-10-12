import urllib.parse
from typing import Iterable

# A set of CDN domains that are allowed to be used.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.somedomain.org",
    "static.mysite.net",
}

def build_cdn_resource_url(
    cdn_url_base: str,
    file_id: str,
    file_type: str
) -> str:
    """
    Build a fully-qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN.  Should include protocol and domain,
        e.g. "https://cdn.example.com/".
    file_id : str
        Unique identifier of the resource.  This will be appended to the path.
    file_type : str
        Type of resource, e.g. "image", "script".  Used to construct a path
        segment or query string if needed.

    Returns
    -------
    str
        A fully-qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS`.  This protects against accidental or
        malicious redirects to an untrusted CDN.
    """
    # Ensure the base URL ends with a slash so that urljoin behaves predictably
    if not cdn_url_base.endswith("/"):
        base = f"{cdn_url_base}/"
    else:
        base = cdn_url_base

    # Construct the relative path.  We use a simple format: <file_type>/<file_id>
    # This keeps the URL clean and avoids query-string injection.
    relative_path = urllib.parse.urljoin(
        "", f"{file_type.rstrip('/')}/{urllib.parse.quote(file_id)}"
    )

    # Build the absolute URL
    full_url = urllib.parse.urljoin(base, relative_path)

    # Parse the resulting URL to validate its domain
    parsed = urllib.parse.urlparse(full_url)

    # Normalise the netloc to lowercase for comparison
    domain = parsed.netloc.lower()

    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{domain}'. "
            "Allowed domains are: "
            + ", ".join(sorted(ALLOWED_CDN_DOMAINS))
        )

    return full_url