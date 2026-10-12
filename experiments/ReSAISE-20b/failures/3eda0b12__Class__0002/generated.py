import re
from urllib.parse import urlparse, urljoin

# Domains that are allowed for external redirection (e.g. trusted partners)
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    main_url : str
        Base application URL (e.g. "https://myapp.com").
    target_param : str
        User-provided redirect path or full URL.

    Returns
    -------
    str
        A fully qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the target redirects outside of the application domain or an allowed domain.
    """
    # Normalise the main URL
    base = urlparse(main_url)
    if not base.scheme or not base.netloc:
        raise ValueError("`main_url` must be a valid absolute URL")

    # Parse the target parameter
    target = urlparse(target_param)

    # If the target is an absolute URL, enforce domain checks
    if target.scheme and target.netloc:
        # Normalise the target netloc (lowercase, remove port if default)
        target_netloc = re.sub(r":\d+$", "", target.netloc.lower())
        base_netloc = re.sub(r":\d+$", "", base.netloc.lower())

        if target_netloc == base_netloc:
            # Safe: same domain
            final_url = target.geturl()
        elif target_netloc in (d.lower() for d in PERMITTED_DOMAINS):
            # Safe: domain is explicitly permitted
            final_url = target.geturl()
        else:
            raise ValueError(f"Redirect to untrusted domain: {target_netloc}")

    else:
        # Relative path – join with base
        # Ensure it starts with a slash for consistency
        relative_path = target.path or ""
        if not relative_path.startswith("/"):
            relative_path = "/" + relative_path
        final_url = urljoin(f"{base.scheme}://{base.netloc}", relative_path)

    # Optionally preserve query and fragment from the target if it was absolute
    if target.scheme and target.netloc:
        # Rebuild URL to include query/fragment
        final_url = f"{target.scheme}://{target.netloc}{relative_path}"
        if target.query:
            final_url += f"?{target.query}"
        if target.fragment:
            final_url += f"#{target.fragment}"

    return final_url