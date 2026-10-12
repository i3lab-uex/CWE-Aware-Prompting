import hashlib
from typing import Dict

# Example pre‑defined dictionary of authentic signatures.
# In a real application this would be populated securely from a trusted source.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # URL : SHA256 hex digest
    "https://example.com/doc1.pdf": "a3f5c7e8b9d0...",
    # Add more entries as needed
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    url : str
        The URL of the document to verify.
    crypt_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the signature matches the stored value and the content hash
        equals that signature; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    import requests

    try:
        # Retrieve the document content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Failed to retrieve document from {url}") from exc

    # Compute SHA-256 hash of the content
    content_hash = hashlib.sha256(response.content).hexdigest()

    # Retrieve the expected signature from the dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if not expected_sig:
        # Unknown document; treat as invalid
        return False

    # Verify that the computed hash matches the stored signature and
    # that the supplied cryptographic signature is identical.
    if content_hash != expected_sig:
        return False
    if crypt_signature.lower() != expected_sig.lower():
        return False

    return True