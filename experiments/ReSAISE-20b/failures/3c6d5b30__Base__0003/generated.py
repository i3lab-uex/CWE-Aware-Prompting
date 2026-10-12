import urllib.parse

# Example list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "cdn.example.net",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL from the base application URL and a user-provided
    'next' parameter. The resulting URL must either belong to the same domain as
    `domain_base_url` or be in the ALLOWED_DOMAINS list. Otherwise a ValueError
    is raised.

    Args:
        domain_base_url (str): The base URL of the application.
        next_redirect_param (str): The user-provided redirect target.

    Returns:
        str: A fully qualified URL safe for redirection.

    Raises:
        ValueError: If the resulting URL is not within the base domain or
                    one of the allowed external domains.
    """
    # Parse the base URL to extract scheme and netloc
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid base URL")

    # Determine the final redirect URL
    next_parsed = urllib.parse.urlparse(next_redirect_param)

    if next_parsed.scheme and next_parsed.netloc:
        # Absolute URL provided by the user
        redirect_url = next_redirect_param
    else:
        # Relative path – safely join with the base URL
        redirect_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Validate the resulting URL
    final_parsed = urllib.parse.urlparse(redirect_url)

    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError("Redirect URL is missing scheme or netloc")

    # Check if the redirect target is within the same domain as the base
    if final_parsed.netloc == base_parsed.netloc:
        return redirect_url

    # If not the same domain, ensure it's an allowed external domain
    if final_parsed.netloc in ALLOWED_DOMAINS:
        return redirect_url

    # If none of the checks pass, reject the URL
    raise ValueError("Redirect target not allowed: potential open redirect vulnerability")