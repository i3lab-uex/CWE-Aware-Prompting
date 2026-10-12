import requests
from typing import Dict

# Example pre‑defined mapping of document URLs to their authentic signatures.
# In a real system this would be securely populated from a trusted source.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    "https://example.com/doc1.pdf": "d41d8cd98f00b204e9800998ecf8427e",
    "https://example.com/doc2.pdf": "0cc175b9c0f1b6a831c399e269772661",
    # ... add more mappings as needed
}


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the
    pre‑stored signature for a document at the given URL.

    Parameters
    ----------
    url : str
        The HTTPS URL of the document to validate.
    crypt_signature : str
        The signature supplied by the caller (e.g., from a header or query param).

    Returns
    -------
    bool
        True if the signature matches the trusted value for the URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (network error, non‑200 status,
        SSL verification failure, etc.).
    """
    # 1. Ensure we can reach the document (minimal integrity check)
    try:
        resp = requests.get(url, timeout=10.0, verify=True)  # SSL verification enabled
        resp.raise_for_status()  # Raises HTTPError for bad status codes
    except requests.exceptions.RequestException as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

    # 2. Compare the provided signature with the trusted one
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # No trusted signature known for this URL; treat as invalid
        return False

    # Constant‑time comparison to mitigate timing attacks
    def _compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _compare(crypt_signature, expected_sig)