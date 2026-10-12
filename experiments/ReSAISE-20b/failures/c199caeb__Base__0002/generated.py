import urllib.parse

# Domains that are allowed for external redirects.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL from the base application URL and a user‑supplied
    ``redirect_param``.  The function ensures that the final URL either points
    within the same domain as ``app_url`` or to one of the approved external
    domains.  If it does not, a ``ValueError`` is raised.

    Parameters:
        app_url (str): Base URL of the application, e.g. "https://myapp.com".
        redirect_param (str): Path or full URL supplied by the user.

    Returns:
        str: A fully qualified redirect URL that is safe to use.
    """
    # Normalise the base application URL
    base = urllib.parse.urlparse(app_url)
    if not base.scheme or not base.netloc:
        raise ValueError("app_url must be a valid absolute URL")

    # Resolve the redirect parameter relative to the base
    joined = urllib.parse.urljoin(app_url, redirect_param)
    parsed = urllib.parse.urlparse(joined)

    # If the URL is relative (no netloc), it stays within the app
    if not parsed.netloc:
        return joined

    # Check that the domain is either the same as app_url or in approved list
    if parsed.netloc == base.netloc:
        return joined

    # Normalise domain for comparison (strip port if present)
    def _domain_without_port(netloc: str) -> str:
        return netloc.split(":")[0].lower()

    target_domain = _domain_without_port(parsed.netloc)
    allowed_domains = {d.lower() for d in APPROVED_DOMAINS}
    if target_domain not in allowed_domains:
        raise ValueError(
            f"Redirect to unapproved domain: {target_domain}"
        )

    return joined