import re
from urllib.parse import urlparse, urljoin

# Example list of allowed external domains; adjust as needed
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL by combining the application's base URL with
    a user‑supplied next route.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com/").
    next_route : str
        The user‑supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside the base domain and not in ALLOWED_DOMAINS).
    """
    # Normalise the base URL (ensure it ends with a slash for proper joining)
    if not main_base_url.endswith("/"):
        base = f"{main_base_url}/"
    else:
        base = main_base_url

    # Parse the user supplied next_route
    parsed_next = urlparse(next_route)

    # If the user supplied a full URL (has scheme and netloc)
    if parsed_next.scheme and parsed_next.netloc:
        # Validate the scheme
        if parsed_next.scheme not in {"http", "https"}:
            raise ValueError("Unsupported URL scheme")

        # Check if the domain is allowed
        netloc = parsed_next.netloc.lower()
        # Strip potential port number for domain comparison
        domain = netloc.split(":")[0]

        if domain not in ALLOWED_DOMAINS:
            # Ensure the domain matches the base domain
            base_parsed = urlparse(base)
            base_domain = base_parsed.netloc.lower()
            if domain != base_domain:
                raise ValueError("Redirect URL points to an untrusted domain")

        # Reconstruct the full URL ensuring no path traversal tricks
        safe_url = parsed_next.geturl()
    else:
        # Treat as a relative path; join with base
        safe_url = urljoin(base, next_route)

    # Final safety check: ensure the resulting URL resolves to the same domain
    final_parsed = urlparse(safe_url)
    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError("Resulting URL is malformed")

    # Ensure the final domain is either the base domain or in ALLOWED_DOMAINS
    final_domain = final_parsed.netloc.split(":")[0].lower()
    base_domain = urlparse(base).netloc.lower()

    if final_domain != base_domain and final_domain not in ALLOWED_DOMAINS:
        raise ValueError("Resulting URL points to an untrusted domain")

    return safe_url