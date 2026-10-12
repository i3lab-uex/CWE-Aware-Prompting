import re
from urllib.parse import urlparse, urljoin

# Domains that are considered safe for external redirects.
APPROVED_DOMAINS = [
    "example.com",
    "trusted-site.org",
    # Add more domains as needed
]

def _is_approved_domain(netloc: str) -> bool:
    """
    Check whether the given netloc matches any of the approved domains.
    Netloc may include a port number; strip it before comparison.
    """
    # Remove optional port
    host = netloc.split(":")[0].lower()
    return any(host == domain.lower() or host.endswith("." + domain.lower())
               for domain in APPROVED_DOMAINS)


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_url : str
        Base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        User supplied path or full URL to redirect to.

    Returns
    -------
    str
        A fully-qualified redirect URL that is guaranteed to stay within the
        application or an approved external domain.

    Raises
    ------
    ValueError
        If the resolved URL points outside the application or to an unapproved domain.
    """
    if not isinstance(app_url, str) or not isinstance(redirect_param, str):
        raise TypeError("Both arguments must be strings")

    # Parse the base application URL
    parsed_app = urlparse(app_url)
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError("app_url must be a valid absolute URL")

    # Resolve the redirect parameter relative to the base app URL
    resolved_url = urljoin(app_url, redirect_param)

    parsed_resolved = urlparse(resolved_url)

    # 1. If the redirect is relative (no netloc) it's safe.
    if not parsed_resolved.netloc:
        return resolved_url

    # 2. If the netloc matches the app's domain, it's safe.
    if parsed_resolved.netloc.lower() == parsed_app.netloc.lower():
        return resolved_url

    # 3. If the netloc is in the approved domains list, allow it.
    if _is_approved_domain(parsed_resolved.netloc):
        return resolved_url

    # Anything else is disallowed.
    raise ValueError(f"Redirect URL '{resolved_url}' points to an unapproved domain.")


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     base = "https://app.example.com"
#     print(generate_redirect_link(base, "/dashboard"))
#     print(generate_redirect_link(base, "https://trusted-site.org/welcome"))
#     # This would raise ValueError
#     # print(generate_redirect_link(base, "https://malicious.com"))