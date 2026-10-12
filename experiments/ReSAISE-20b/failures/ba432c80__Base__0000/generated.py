import requests
import hmac

# Global dictionary mapping URLs to their expected cryptographic signatures.
# Example:
# DOC_SIGS = {
#     "https://example.com/doc1.pdf": "abcdef1234567890",
#     "https://example.org/report.txt": "1234abcd5678efgh",
# }
DOC_SIGS = {}


def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate the cryptographic signature of a document located at ``url``.

    Parameters
    ----------
    url : str
        The URL of the remote document.
    sign_hash : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        ``True`` if the supplied signature matches the expected value,
        otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL (e.g., network
        error, 4xx/5xx HTTP status code).
    """
    # Ensure the URL is reachable before verifying the signature.
    try:
        response = requests.head(url, timeout=5)
        # Some servers may not support HEAD; fallback to GET with no body.
        if response.status_code >= 400:
            # Attempt a lightweight GET to confirm accessibility
            get_resp = requests.get(url, stream=True, timeout=5)
            get_resp.close()
            if get_resp.status_code >= 400:
                raise IOError(f"Document at {url} is inaccessible (status "
                              f"{get_resp.status_code}).")
    except requests.RequestException as e:
        raise IOError(f"Unable to access document at {url}: {e}") from e

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # If the URL isn't known, we treat it as an invalid signature.
        return False

    # Perform a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign_hash, expected_sig)