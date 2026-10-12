import urllib.parse
from typing import List

# Predefined list of safe external domains
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add other trusted domains here
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_redirect_param : str
        The path or absolute URL the user wishes to visit after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Parse the base URL to extract its components
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid base URL provided.")

    # Join the next param with the base to get a full URL
    joined_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resulting URL
    result_parsed = urllib.parse.urlparse(joined_url)

    # If the path is relative (no netloc), it's safe to return
    if not result_parsed.netloc:
        # Ensure the path does not escape the base domain (e.g., "../../../../etc/passwd")
        cleaned_path = urllib.parse.urljoin("/", result_parsed.path)
        return f"{base_parsed.scheme}://{base_parsed.netloc}{cleaned_path}"

    # If the URL is absolute, verify that its domain is allowed
    host = result_parsed.hostname or ""
    if host.lower() != base_parsed.hostname.lower() and host.lower() not in (d.lower() for d in ALLOWED_DOMAINS):
        raise ValueError(f"Redirect URL host '{host}' is not allowed.")

    # Return the fully qualified absolute URL
    return joined_url