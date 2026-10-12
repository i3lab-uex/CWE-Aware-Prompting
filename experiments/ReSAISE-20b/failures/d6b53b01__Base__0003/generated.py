import requests
from typing import Dict

# Pre‑defined dictionary containing the canonical signatures for each document.
# In a real system this would be stored in a secure location and protected
# against tampering.  For the purpose of this example we assume it is read‑only.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries (URL : signature)
    "https://example.com/doc1.pdf": "a3f5c2e7d8b9...",
    "https://example.com/doc2.txt": "f1e3c4b6d7a8...",
    # Add more entries as needed
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    document_location : str
        URL pointing to the remote document.
    crypto_sign : str
        The cryptographic signature supplied by the caller.

    Returns
    -------
    bool
        True if the provided signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from ``document_location``.
    """
    # 1. Ensure we can reach the document; use a short timeout and verify SSL.
    try:
        response = requests.get(document_location, timeout=10, stream=True, verify=True)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to retrieve document from {document_location}") from exc

    # 2. We don't actually need the content for signature comparison, but
    #    consuming the response ensures that any network errors are caught.
    #    Discard the content to keep memory usage low.
    for _ in response.iter_content(chunk_size=8192):
        pass  # just consume the stream

    # 3. Retrieve the expected signature from the dictionary.
    expected_signature = DOCUMENT_SIGNATURES.get(document_location)

    # 4. If no entry exists, treat it as a mismatch.
    if expected_signature is None:
        return False

    # 5. Compare signatures in a constant‑time manner to avoid timing attacks.
    #    The built-in `hmac.compare_digest` is suitable for this purpose.
    import hmac
    return hmac.compare_digest(crypto_sign, expected_signature)