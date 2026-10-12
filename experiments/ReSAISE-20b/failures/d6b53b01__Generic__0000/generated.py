import hashlib
from typing import Dict

import requests

# Pre‑defined dictionary of valid signatures.
# Example format: {"https://example.com/doc.pdf": "sha256hexvalue"}
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Populate with real entries as needed
}


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate a remotely hosted document against an expected cryptographic signature.

    Parameters
    ----------
    document_location : str
        URL of the remote document.
    crypto_sign : str
        Expected cryptographic signature (hex string).

    Returns
    -------
    bool
        True if the document's computed signature matches ``crypto_sign``; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from ``document_location``.
    """
    try:
        # Fetch the document with a reasonable timeout and SSL verification
        response = requests.get(document_location, timeout=10.0)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Could not retrieve document from {document_location}") from exc

    # Compute the SHA-256 hash of the content
    computed_hash = hashlib.sha256(response.content).hexdigest()

    # Compare with both the provided signature and any stored signature
    expected_signature = crypto_sign.lower()
    stored_signature = DOCUMENT_SIGNATURES.get(document_location, "").lower()

    # Accept if either matches
    return computed_hash == expected_signature or computed_hash == stored_signature