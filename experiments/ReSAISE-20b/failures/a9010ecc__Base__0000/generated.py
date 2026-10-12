import urllib.parse

# Example list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = ["example.com", "trustedsite.org"]


def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL based on the application base URL and a user-provided
    redirect parameter. The function ensures that the final URL is either:

        * a relative path within the same origin as `app_base_url`, or
        * an absolute URL whose domain is in ALLOWED_DOMAINS.

    Parameters:
        app_base_url (str): The base URL of the application (e.g., "https://app.example.com").
        redirect_param (str): The user-provided path or absolute URL to redirect to.

    Returns:
        str: A fully-qualified URL that can be safely used for redirection.

    Raises:
        ValueError: If the resulting URL is not safe (i.e., points to an untrusted domain
                    or is a relative path that resolves outside the base origin).
    """
    # Normalise the application base URL (ensure it ends with a slash for urljoin)
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    if not parsed_redirect.scheme:
        # Relative path or fragment – treat as relative to the base URL
        joined_url = urllib.parse.urljoin(base, redirect_param)
        # Ensure the resulting URL has the same netloc as the base
        parsed_joined = urllib.parse.urlparse(joined_url)
        if parsed_joined.scheme not in ("http", "https"):
            raise ValueError("Redirect URL must use HTTP or HTTPS scheme")
        base_parsed = urllib.parse.urlparse(app_base_url)
        if parsed_joined.netloc.lower() != base_parsed.netloc.lower():
            raise ValueError("Redirect URL points outside the application domain")
        return joined_url
    else:
        # Absolute URL – validate its domain
        if parsed_redirect.scheme not in ("http", "https"):
            raise ValueError("Redirect URL must use HTTP or HTTPS scheme")

        domain = parsed_redirect.netloc.split(":")[0]  # strip port if present
        if domain.lower() not in (d.lower() for d in ALLOWED_DOMAINS):
            raise ValueError(f"Redirect URL domain '{domain}' is not allowed")
        return redirect_param