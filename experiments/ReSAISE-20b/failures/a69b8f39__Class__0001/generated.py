import urllib.parse
from typing import Set

# Domains that are allowed to be used as a return URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add other trusted domains here.
}


def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct an SSO redirect URL that points to the third‑party service.

    The resulting URL contains two query parameters:
        * `user_ref`: the unique identifier of the user.
        * `back_url`: a fully qualified URL to return to after authentication.

    Parameters
    ----------
    sso_service : str
        The base URL of the SSO service. Must be a valid absolute URL.
    user_ref : str
        The unique identifier of the user.  It will be URL‑encoded.
    back_url : str
        The URL to redirect back after the SSO flow.  Its domain must be in
        ``ALLOWED_RETURN_DOMAINS`` to avoid an open‑redirect vulnerability.

    Returns
    -------
    str
        The fully formed SSO redirect URL.

    Raises
    ------
    ValueError
        If ``sso_service`` is not a valid absolute URL, or if the domain of
        ``back_url`` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the SSO service URL
    sso_parsed = urllib.parse.urlparse(sso_service)
    if not (sso_parsed.scheme and sso_parsed.netloc):
        raise ValueError(f"Invalid SSO service URL: {sso_service!r}")

    # Validate the return URL
    back_parsed = urllib.parse.urlparse(back_url)
    if not (back_parsed.scheme and back_parsed.netloc):
        raise ValueError(f"Return URL must be an absolute URL: {back_url!r}")

    # Ensure the domain is allowed (CWE‑610 mitigation)
    if back_parsed.netloc.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(
            f"Return URL domain '{back_parsed.netloc}' is not allowed."
        )

    # Build the query parameters
    query_params = {
        "user_ref": user_ref,
        "back_url": back_url,
    }
    encoded_query = urllib.parse.urlencode(query_params, safe="/:?=&")

    # Construct the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            sso_parsed.scheme,
            sso_parsed.netloc,
            sso_parsed.path,
            sso_parsed.params,
            encoded_query,
            sso_parsed.fragment,
        )
    )

    return redirect_url