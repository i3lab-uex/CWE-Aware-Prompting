import requests
from hmac import compare_digest
from typing import Dict

# Global mapping of document URLs to their expected cryptographic signatures.
DOC_SIGS: Dict[str, str] = {
    # Example entries – replace with real values.
    "https://example.com/doc1.pdf": "a3b9c2d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "b1c2d3e4f5g6h7i8j9k0",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the supplied signature matches the expected value for
    the document located at `url`.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `url` is inaccessible (e.g., network error,
        non‑200 status code, or timeout).
    """
    # 1. Check that the URL is reachable before accessing signatures.
    try:
        resp = requests.head(url, timeout=5)
        if resp.status_code != 200:
            raise IOError(f"Document at {url} returned status code {resp.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # 2. Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # Unknown document – treat as invalid.
        return False

    # 3. Compare signatures using a constant‑time comparison to avoid
    # timing attacks (CWE-352, CWE-345).
    return compare_digest(sign_hash.strip(), expected_sig)