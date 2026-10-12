import hashlib
import requests

# Pre‑defined dictionary mapping document URLs to their authentic SHA256 signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL : signature)
    "https://example.com/doc1.pdf": "5d41402abc4b2a76b9719d911017c592",
    "https://example.com/doc2.pdf": "6f1ed002ab5595859014ebf0951522d9",
    # Add more entries as needed
}


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    document_location : str
        URL pointing to the target document.
    crypto_sign : str
        Cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the document's SHA256 signature matches both the stored
        signature for the URL and the supplied crypto_sign; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (network error or non‑200 status).
    """
    try:
        resp = requests.get(document_location, timeout=10)
        resp.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {document_location}") from exc

    # Compute SHA256 of the content
    sha256_hash = hashlib.sha256(resp.content).hexdigest()

    # Retrieve the expected signature for this URL
    expected_signature = DOCUMENT_SIGNATURES.get(document_location)

    # Perform a constant‑time comparison to mitigate timing attacks
    def _constant_time_eq(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    # Verify that the computed hash matches both the stored signature and the supplied one
    if expected_signature is None:
        return False

    return (
        _constant_time_eq(sha256_hash, expected_signature) and
        _constant_time_eq(sha256_hash, crypto_sign)
    )