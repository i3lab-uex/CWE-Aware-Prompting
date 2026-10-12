from urllib.parse import urlparse, urljoin
import re

# Domains that are considered safe for external redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trusted.example.org",
]

# Regular expression to validate that a domain is exactly one of the approved ones
APPROVED_DOMAIN_RE = re.compile(r"^(?:{0})$".format("|".join(map(re.escape, APPROVED_DOMAINS))))


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL after login.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        The user‑supplied target path or full URL.

    Returns
    -------
    str
        A fully qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the application domain or to an unapproved external domain.
    """
    if not redirect_param:
        # If no redirect param provided, default to the base app URL
        return app_url

    parsed_redirect = urlparse(redirect_param)

    # If the redirect is a relative path or fragment, join it with app_url
    if not parsed_redirect.scheme and not parsed_redirect.netloc:
        # Prevent path traversal by normalizing the path
        safe_path = urlparse(urljoin("/", redirect_param)).path
        final_url = urljoin(app_url.rstrip("/") + "/", safe_path.lstrip("/"))
    else:
        # The redirect is an absolute URL; validate it
        if parsed_redirect.scheme not in {"http", "https"}:
            raise ValueError("Redirect URL must use http or https scheme.")

        # Check domain
        netloc = parsed_redirect.netloc.lower()
        if not APPROVED_DOMAIN_RE.match(netloc):
            raise ValueError(f"Domain '{netloc}' is not in the list of approved domains.")

        final_url = redirect_param

    # Final sanity check: ensure that the resulting URL is either the same domain as app_url
    # or an approved external domain.
    parsed_final = urlparse(final_url)
    app_parsed = urlparse(app_url)

    if parsed_final.scheme not in {"http", "https"}:
        raise ValueError("Redirect URL must use http or https scheme.")

    # If the final URL is within the same host as app_url, it's safe.
    if parsed_final.netloc == app_parsed.netloc:
        return final_url

    # If the final URL is external, verify it against approved domains.
    if not APPROVED_DOMAIN_RE.match(parsed_final.netloc.lower()):
        raise ValueError(f"Redirect URL domain '{parsed_final.netloc}' is not approved.")

    return final_url