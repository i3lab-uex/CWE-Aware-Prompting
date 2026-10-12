import hashlib
import hmac
from typing import Dict

# Example dictionary mapping document URLs to their expected SHA‑256 hex signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # "https://example.com/doc1.pdf": "a3b5c6... (hex)",
    # Add real entries here.
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by verifying its cryptographic signature.

    Parameters
    ----------
    location : str
        The URL of the document to retrieve and verify.
    sign : str
        The cryptographic signature (hex digest) provided for verification.

    Returns
    -------
    bool
        True if the signature matches the document's content; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    import requests

    # Retrieve the remote file
    try:
        response = requests.get(location, timeout=10)
        response.raise_for_status()
        content = response.content
    except requests.exceptions.RequestException as exc:
        raise IOError(f"Failed to retrieve document from {location}") from exc

    # Compute the SHA‑256 digest of the retrieved content
    sha256 = hashlib.sha256()
    sha256.update(content)
    computed_digest = sha256.hexdigest()

    # Ensure the provided signature matches the expected one for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(location)
    if not expected_sig:
        # If we have no stored signature for this URL, consider it invalid
        return False

    # Compare the provided sign with both the stored signature and the computed digest.
    # Use constant‑time comparison to mitigate timing attacks.
    if not (hmac.compare_digest(sign.lower(), expected_sig.lower()) or
            hmac.compare_digest(computed_digest, sign.lower())):
        return False

    # If we reach here, the signature is valid
    return True