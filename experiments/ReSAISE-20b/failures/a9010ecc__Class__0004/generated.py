import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Generate a safe URL to which the user should be redirected after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    redirect_param : str
        The user-provided URL path or full address to navigate to after login.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the generated redirect URL points to a domain that is neither the
        application's own domain nor an allowed external domain.
    """
    # Parse base URL to extract its components
    parsed_base = urllib.parse.urlparse(app_base_url)

    # Normalize the redirect_param by stripping leading/trailing whitespace
    redirect_param = redirect_param.strip()

    # If the redirect param is a full URL, parse it; otherwise treat as path
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If the redirect has a netloc, it is an absolute URL
    if parsed_redirect.netloc:
        # Check that the domain is either the same as the base or in allowed list
        target_netloc = parsed_redirect.netloc.lower()
        if (
            target_netloc != parsed_base.netloc.lower()
            and target_netloc not in {d.lower() for d in ALLOWED_DOMAINS}
        ):
            raise ValueError(
                f"Redirect target domain '{target_netloc}' is not allowed."
            )
        # Construct the final URL (use the redirect as-is)
        return urllib.parse.urlunparse(parsed_redirect)

    # If no netloc, treat redirect_param as a relative path
    # Use urljoin to combine with the base URL safely
    final_url = urllib.parse.urljoin(app_base_url, redirect_param)

    # Verify that the resulting URL stays within the same domain
    parsed_final = urllib.parse.urlparse(final_url)
    if parsed_final.netloc.lower() != parsed_base.netloc.lower():
        raise ValueError(
            f"Redirect path '{redirect_param}' resolves to an external domain."
        )

    return final_url