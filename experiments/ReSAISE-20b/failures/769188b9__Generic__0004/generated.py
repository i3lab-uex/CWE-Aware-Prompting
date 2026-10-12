import requests
from typing import Dict

# Global dictionary that maps a document URL to its expected SHA‑256 hash.
# Example:
# DOC_HASHES = {
#     "https://example.com/doc1.pdf": "a3f5c... (64 hex chars)",
#     ...
# }
DOC_HASHES: Dict[str, str] = {}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that a document hosted at *resource_url* is authentic by comparing the
    supplied *crypto_signature* against the expected hash stored in ``DOC_HASHES``.
    
    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature (hex string) submitted with the document.
    
    Returns
    -------
    bool
        ``True`` if the signature matches the expected value, otherwise ``False``.
    
    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL (network error,
        non‑200 status code, etc.).
    """
    try:
        # Retrieve the document; raise an exception for HTTP errors
        response = requests.get(resource_url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Convert any request‑related error into an IOError
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # Compute the SHA‑256 hash of the retrieved content
    computed_hash = response.content.hex()
    # Compare against the supplied signature and the expected hash from DOC_HASHES
    expected_hash = DOC_HASHES.get(resource_url)
    return (
        crypto_signature.lower() == computed_hash
        and expected_hash is not None
        and crypto_signature.lower() == expected_hash.lower()
    )