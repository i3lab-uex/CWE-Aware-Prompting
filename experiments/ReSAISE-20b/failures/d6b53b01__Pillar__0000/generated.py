import hashlib
import requests
from typing import Dict

# Pre‑defined mapping of document URLs to their authentic SHA‑256 signatures
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries – in real usage this would be populated elsewhere
    "https://example.com/doc1.pdf": "3a7bd3e2360a... (hex signature)",
    "https://example.com/doc2.pdf": "f5c8d3b12e9f... (hex signature)",
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    document_location : str
        The HTTPS URL of the document to be verified.
    crypto_sign : str
        The expected SHA‑256 hexadecimal signature of the document.

    Returns
    -------
    bool
        ``True`` if the computed hash matches ``crypto_sign``, otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved from ``document_location``.
    """
    # Enforce HTTPS to avoid man‑in‑the‑middle attacks
    if not document_location.lower().startswith("https://"):
        raise ValueError("Only HTTPS URLs are allowed for security reasons.")

    try:
        # Retrieve the document with a reasonable timeout
        response = requests.get(document_location, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {document_location}") from exc

    # Compute the SHA‑256 hash of the retrieved content
    sha256 = hashlib.sha256()
    sha256.update(response.content)
    computed_hash = sha256.hexdigest()

    # Compare the computed hash with the supplied signature
    return computed_hash.lower() == crypto_sign.lower()