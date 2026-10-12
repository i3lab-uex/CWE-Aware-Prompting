import urllib.parse as urlparse
from typing import List

# Example list of domains that are permitted for external redirects.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    # Add other trusted domains here
]

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com").
    next_route : str
        The user supplied redirect target. May be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the base domain and is not on an
        allowed external domain.
    """
    # Parse the main base URL to extract its components
    base_parsed = urlparse.urlparse(main_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid main_base_url: {main_base_url!r}")

    # Parse the next_route
    next_parsed = urlparse.urlparse(next_route)

    # If next_route is a relative path, join it with the base URL
    if not next_parsed.scheme and not next_parsed.netloc:
        # Ensure the path starts with a slash
        relative_path = next_parsed.path or '/'
        if not relative_path.startswith('/'):
            relative_path = '/' + relative_path
        # Preserve any query or fragment from next_route
        resolved_url = urlparse.urlunparse((
            base_parsed.scheme,
            base_parsed.netloc,
            relative_path,
            next_parsed.params,
            next_parsed.query,
            next_parsed.fragment
        )))
    else:
        # next_route is an absolute URL – validate it
        if next_parsed.scheme not in ('http', 'https'):
            raise ValueError(f"Unsupported scheme in next_route: {next_parsed.scheme!r}")

        # If the host matches the base domain, it's safe
        if next_parsed.netloc == base_parsed.netloc:
            resolved_url = urlparse.urlunparse(next_parsed)
        else:
            # Check if the host is in ALLOWED_DOMAINS
            host = next_parsed.hostname or ''
            if host not in ALLOWED_DOMAINS:
                raise ValueError(
                    f"Redirect to external domain {host!r} is not permitted"
                )
            # If allowed, use the next_route as-is
            resolved_url = urlparse.urlunparse(next_parsed)

    return resolved_url

# Example usage
if __name__ == "__main__":
    base = "https://app.example.com"
    print(assemble_redirect_uri(base, "/dashboard"))            # relative
    print(assemble_redirect_uri(base, "https://app.example.com/profile"))  # same domain
    print(assemble_redirect_uri(base, "https://trusted.org/welcome"))      # allowed external
    try:
        print(assemble_redirect_uri(base, "https://malicious.com/steal"))
    except ValueError as e:
        print(f"Blocked: {e}")