import urllib.parse
from pathlib import PosixPath

# Define a set of approved CDN domains. In practice, this would be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def generate_cdn_content_url(cdn_origin_url: str,
                              content_id: str,
                              content_kind: str) -> str:
    """
    Build a fully qualified URL to access a resource on an approved CDN.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com").
    content_id : str
        Unique identifier for the resource.
    content_kind : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        A validated, fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ALLOWED_CDN_DOMAINS.
    """
    # Parse the origin URL to extract components
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)

    # Ensure the URL has a scheme; default to https if missing
    scheme = parsed_origin.scheme or "https"

    # Normalise netloc to lower case for comparison
    origin_netloc = parsed_origin.netloc.lower()
    if not origin_netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Validate the domain
    if origin_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {origin_netloc!r}. "
            "Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Construct the path to the resource.
    # Use PosixPath to avoid double slashes and to normalize
    path = PosixPath(parsed_origin.path) / content_kind / content_id

    # Build the final URL
    url = urllib.parse.urlunparse(
        (
            scheme,
            origin_netloc,
            str(path),
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return url

# Example usage (for demonstration only; remove or comment out in production)
if __name__ == "__main__":
    print(
        generate_cdn_content_url(
            "https://cdn.example.com",
            "abc123.jpg",
            "image"
        )
    )