import urllib.parse
from typing import Iterable

# Example list of permitted CDN domains.  In real deployments this would come from
# a secure configuration source (e.g., environment variable, config file,
# or secrets manager).  The list must be kept up‑to‑date to avoid leaking
# resources to untrusted hosts.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.example.org",
    "static.myapp.net",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully qualified URL pointing to a resource hosted on an approved CDN.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    file_id : str
        Unique identifier of the resource (e.g. "12345abcd").
    file_type : str
        Resource type, typically a directory name (e.g. "images", "scripts").

    Returns
    -------
    str
        A fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not present in
        ``ALLOWED_CDN_DOMAINS`` or if the URL is malformed.
    """
    # Normalise base: ensure it ends with a slash so that urljoin behaves
    # predictably.  ``urlparse`` will handle missing scheme by treating it as
    # relative, so we explicitly add "https://" if absent.
    base = cdn_url_base.strip()
    if not base:
        raise ValueError("cdn_url_base must be a non-empty string")

    parsed_base = urllib.parse.urlparse(base)
    if not parsed_base.scheme:
        # Default to https for security
        base = f"https://{base}"
        parsed_base = urllib.parse.urlparse(base)

    # Build the relative path: <file_type>/<file_id>
    rel_path = urllib.parse.quote(f"{file_type.strip('/')}/{file_id.lstrip('/')}")
    # ``urljoin`` handles merging base with the relative path.
    full_url = urllib.parse.urljoin(base, rel_path)

    # Validate that the resulting URL resolves to an approved CDN domain.
    parsed_full = urllib.parse.urlparse(full_url)
    if not parsed_full.scheme or not parsed_full.netloc:
        raise ValueError(f"Malformed URL constructed: {full_url!r}")

    # Ensure the hostname is in the allowed list.  We ignore ports and userinfo
    # because they could be used to bypass checks (e.g., ``cdn.example.com:8080``).
    hostname = parsed_full.hostname
    if hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {hostname!r}")

    # Return the sanitized, fully resolved URL.
    return full_url