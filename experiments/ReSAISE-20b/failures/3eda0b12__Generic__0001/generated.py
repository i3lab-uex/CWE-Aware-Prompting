import urllib.parse

# Domains that are allowed for external redirects (e.g. analytics, help pages)
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    main_url : str
        Base application URL (e.g. "https://app.example.com").
    target_param : str
        Path or full URL to redirect to after login.

    Returns
    -------
    str
        Full, validated redirect URL.

    Raises
    ------
    ValueError
        If the target is not within the application domain or an allowed external domain.
    """
    if not target_param:
        return main_url

    # Parse the base URL to get its components
    base_parsed = urllib.parse.urlparse(main_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # If target_param is a relative path, prepend the base scheme and netloc
    if not urllib.parse.urlparse(target_param).scheme:
        # Ensure a leading slash for relative paths
        rel_path = target_param if target_param.startswith("/") else f"/{target_param}"
        final_url = urllib.parse.urljoin(f"{base_parsed.scheme}://{base_parsed.netloc}", rel_path)
        return final_url

    # target_param is a full URL; validate its domain
    target_parsed = urllib.parse.urlparse(target_param)

    # Normalize the host for comparison (lowercase)
    target_host = target_parsed.hostname.lower() if target_parsed.hostname else ""

    # Allow if the host matches the base domain or is in PERMITTED_DOMAINS
    base_host = base_parsed.hostname.lower()
    if target_host == base_host or target_host in (d.lower() for d in PERMITTED_DOMAINS):
        return target_param

    raise ValueError(
        f"Redirect to {target_param!r} is not allowed: "
        f"host '{target_host}' is neither the app domain nor a permitted domain."
    )