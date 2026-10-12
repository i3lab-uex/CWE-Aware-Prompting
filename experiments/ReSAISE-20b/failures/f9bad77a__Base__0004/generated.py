# ──────────────────────────────────────────────────────────────
# Secure redirect URL construction – avoids open‑redirect issues.
# ──────────────────────────────────────────────────────────────

import urllib.parse
from typing import Dict, Optional, Iterable, Set


# ------------------------------------------------------------------
# Configuration – keep these lists up to date with your environment.
# ------------------------------------------------------------------
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.anotherdomain.org",
}

ALLOWED_ENDPOINTS: Set[str] = {
    "/users",
    "/posts",
    "/comments",
    "/health",
}


def _normalize_domain(url: str) -> str:
    """
    Extract the network location (domain + port if present)
    from a URL, lower‑casing it for comparison.
    """
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname.lower() if parsed.hostname else ""


def _ensure_trailing_slash(url: str) -> str:
    """Make sure the base URL ends with a slash for urljoin to work correctly."""
    return url if url.endswith("/") else url + "/"


def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a fully‑qualified API redirect URL while guarding against
    open redirects (CWE‑601).

    Parameters
    ----------
    main_url : str
        The base API URL (e.g., "https://api.example.com").
    endpoint_name : str
        The specific API endpoint (e.g., "/users").
    params_dict : dict, optional
        Optional query parameters to be appended.

    Returns
    -------
    str
        The complete, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain
        or if the endpoint is not in the allowed list.
    """
    # ------------------------------------------------------------------
    # 1. Validate domain
    # ------------------------------------------------------------------
    normalized_domain = _normalize_domain(main_url)
    if not normalized_domain:
        raise ValueError("Main URL does not contain a valid domain.")
    if normalized_domain not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{normalized_domain}' is not in the list of approved API domains."
        )

    # ------------------------------------------------------------------
    # 2. Validate endpoint
    # ------------------------------------------------------------------
    if not endpoint_name.startswith("/"):
        raise ValueError("Endpoint must start with a leading slash (e.g., '/users').")
    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{endpoint_name}' is not allowed. Allowed endpoints: {sorted(ALLOWED_ENDPOINTS)}"
        )

    # ------------------------------------------------------------------
    # 3. Construct base URL
    # ------------------------------------------------------------------
    safe_base = _ensure_trailing_slash(main_url)

    # urljoin will correctly join the base with the endpoint.
    full_base = urllib.parse.urljoin(safe_base, endpoint_name)

    # ------------------------------------------------------------------
    # 4. Append query parameters if provided
    # ------------------------------------------------------------------
    if params_dict:
        if not isinstance(params_dict, dict):
            raise ValueError("params_dict must be a dictionary.")
        # Encode parameters safely
        query_string = urllib.parse.urlencode(params_dict, doseq=True)
        full_url = f"{full_base}?{query_string}"
    else:
        full_url = full_base

    # Final sanity check: ensure the final URL still uses an approved domain.
    final_domain = _normalize_domain(full_url)
    if final_domain not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Final URL points to unapproved domain '{final_domain}'."
        )

    return full_url


# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            main_url="https://api.example.com",
            endpoint_name="/users",
            params_dict={"id": "123", "active": "true"},
        )
        print("Constructed URL:", url)
    except ValueError as exc:
        print("Error:", exc)