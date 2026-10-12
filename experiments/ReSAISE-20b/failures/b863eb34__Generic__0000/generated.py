import requests
from typing import Dict

# Example signature dictionary (should be defined elsewhere in the real system)
DOCUMENT_SIGNATURES: Dict[str, str] = {
    "https://example.com/doc1.pdf": "abc123signature",
    "https://example.com/doc2.pdf": "def456signature",
    # Add more entries as needed
}


def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify the authenticity of a remote document by comparing its cryptographic
    signature against a trusted value stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed at the given URL.
    """
    # Ensure we can reach the document
    try:
        response = requests.head(doc_url, timeout=5)
        if not response.ok:
            raise IOError(f"Unable to access document at {doc_url} (status code {response.status_code})")
    except requests.exceptions.RequestException as exc:
        raise IOError(f"Error accessing {doc_url}: {exc}") from exc

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # If we don't have a known signature for this URL, treat it as invalid
        return False

    # Compare signatures in a timing‑safe manner
    from hmac import compare_digest
    return compare_digest(signature, expected_sig)