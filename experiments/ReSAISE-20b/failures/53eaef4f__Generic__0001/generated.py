import urllib.parse as urlparse
from urllib.parse import urljoin

# Domains that are considered safe for external redirects
SAFE_DOMAINS = [
    "example.com",
    "trusted.org",
    # add other trusted domains here
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URI after successful login.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. "https://myapp.example.com").
    next_path : str
        The path or full URL the user wants to be redirected to.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to stay within the
        application domain or an allowed external domain.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application's domain or an allowed
        external domain.
    """
    # Parse the primary URL to extract its components
    base = urlparse.urlparse(primary_url)
    if not base.scheme or not base.netloc:
        raise ValueError(f"Invalid primary URL: {primary_url!r}")

    # Parse the next path/URL
    parsed_next = urlparse.urlparse(next_path)

    # If the user supplied an absolute URL, validate its domain
    if parsed_next.scheme and parsed_next.netloc:
        # Normalize the hostname for comparison (case-insensitive)
        host = parsed_next.hostname.lower() if parsed_next.hostname else ""
        # Allow only the primary domain or any of the SAFE_DOMAINS
        allowed_domains = {base.netloc.lower()}
        allowed_domains.update(d.lower() for d in SAFE_DOMAINS)

        if host not in allowed_domains:
            raise ValueError(
                f"Redirect target {next_path!r} is not allowed (domain {host})"
            )
        # Return the absolute URL unchanged
        return parsed_next.geturl()

    # If next_path is relative, join it with the base URL
    joined = urljoin(primary_url, parsed_next.path)

    # Ensure that the resulting path does not escape the primary domain
    final_parsed = urlparse.urlparse(joined)
    if final_parsed.netloc.lower() != base.netloc.lower():
        raise ValueError(
            f"Redirect target {next_path!r} resolves to a different domain: "
            f"{final_parsed.netloc}"
        )

    # Preserve query string and fragment if any
    return urlparse.urlunparse(
        (final_parsed.scheme, final_parsed.netloc, final_parsed.path,
         final_parsed.params, final_parsed.query, final_parsed.fragment)
    )