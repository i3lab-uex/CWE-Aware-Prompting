import requests
from typing import Dict
import hmac

# Example global dictionary of document signatures (URL -> signature)
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # "https://example.com/doc1.pdf": "abcdef123456...",
    # Add actual signatures here
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for the document at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    crypt_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., 404 or network error).
    """
    # Ensure we have a stored signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(file_url)
    if expected_sig is None:
        # No known signature for this URL
        raise IOError(f"No stored signature found for {file_url}")

    try:
        # Perform a lightweight HEAD request to confirm existence
        resp = requests.head(file_url, allow_redirects=True, timeout=10)
        if resp.status_code != 200:
            raise IOError(f"Document not found (status {resp.status_code}) at {file_url}")

        # Optionally, we could download the document to verify integrity.
        # For this function we only compare signatures, so no need to fetch the body.

    except requests.RequestException as exc:
        raise IOError(f"Failed to access {file_url}: {exc}") from exc

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_sig)