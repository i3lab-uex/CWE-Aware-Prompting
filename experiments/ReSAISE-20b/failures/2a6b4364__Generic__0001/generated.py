import urllib.parse

# Domains that are considered safe for redirection.
ALLOWED_DOMAINS = ["example.com", "trustedpartner.org"]


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL by combining the application base URL with
    a user-provided 'next' parameter.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g. "https://myapp.com/").
    next_param : str
        The user-provided path or URL to redirect to.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the same domain as `base_url`
        or does not belong to an allowed external domain.
    """
    # Ensure base_url is absolute
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url must be a valid absolute URL")

    # Parse the user supplied parameter
    parsed_next = urllib.parse.urlparse(next_param)

    # If the next_param contains a scheme, we treat it as an absolute URL
    if parsed_next.scheme:
        # Only allow redirects to the same domain or allowed external domains
        target_netloc = parsed_next.netloc.lower()
        base_domain = parsed_base.netloc.lower()

        if target_netloc == base_domain:
            # Same domain – allowed
            final_url = parsed_next.geturl()
        elif target_netloc in [d.lower() for d in ALLOWED_DOMAINS]:
            # Allowed external domain
            final_url = parsed_next.geturl()
        else:
            raise ValueError("Redirect URL points to a disallowed domain")
    else:
        # Treat as a relative path – join with base_url
        final_url = urllib.parse.urljoin(base_url, next_param)

    # Final sanity check: ensure the resulting URL starts with base_url
    parsed_final = urllib.parse.urlparse(final_url)
    if not parsed_final.scheme or not parsed_final.netloc:
        raise ValueError("Redirect URL is malformed")

    # Optionally, ensure the final URL does not escape the base domain
    if parsed_final.netloc.lower() != parsed_base.netloc.lower():
        # Only allowed external domains are already checked above
        raise ValueError("Redirect URL points outside the allowed domain")

    return final_url


# Example usage
if __name__ == "__main__":
    base = "https://myapp.com/"
    for param in [
        "/dashboard",
        "https://myapp.com/profile?user=alice",
        "https://trustedpartner.org/welcome",
        "https://malicious.com/steal",
    ]:
        try:
            print(create_redirect_url(base, param))
        except ValueError as e:
            print(f"Rejected {param!r}: {e}")