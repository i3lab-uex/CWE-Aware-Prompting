import re
from urllib.parse import urlparse, urljoin

# Example allowed external domains; modify as needed for your application.
ALLOWED_DOMAINS = [
    "example.com",
    "auth.example.org",
    # add more trusted domains here
]


def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        The base URL of the application (e.g., "https://myapp.com").
    forward_param : str
        The URL path or address the user wants to navigate to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application's domain or one of the allowed external domains.
    """
    # Normalise base URL
    app_parsed = urlparse(app_home_url)
    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError(f"Invalid base application URL: {app_home_url!r}")

    # Determine if forward_param is an absolute URL
    forward_parsed = urlparse(forward_param)
    if forward_parsed.scheme and forward_parsed.netloc:
        # Absolute URL: must be in ALLOWED_DOMAINS
        if forward_parsed.netloc not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to external domain '{forward_parsed.netloc}' is not allowed.")
        # Preserve the provided absolute URL
        final_url = forward_param
    else:
        # Relative path or scheme‑less reference; combine with base URL
        final_url = urljoin(app_home_url, forward_param)

    # After combination, verify the domain
    final_parsed = urlparse(final_url)
    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError(f"Resulting URL is invalid: {final_url!r}")

    # If the final domain matches the app's domain, it's safe
    if final_parsed.netloc == app_parsed.netloc:
        return final_url

    # Otherwise, it must be an allowed external domain
    if final_parsed.netloc in ALLOWED_DOMAINS:
        return final_url

    raise ValueError(f"Redirect to domain '{final_parsed.netloc}' is not allowed.")


# ------------------------------------------------------------------
# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     base = "https://myapp.com"
#     for param in ["/dashboard", "https://example.com/welcome",
#                   "//malicious.com/phish", "http://auth.example.org/login"]:
#         try:
#             print(create_forward_link(base, param))
#         except ValueError as e:
#             print(f"Rejected: {e}")