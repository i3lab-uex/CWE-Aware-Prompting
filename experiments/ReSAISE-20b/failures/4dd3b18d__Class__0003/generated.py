import urllib.request
import urllib.error
from typing import Dict
import hmac

# Global dictionary mapping document URLs to their expected signatures.
DOC_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "https://example.com/doc1.pdf": "5f2c8e9a...",
    "https://example.org/report.txt": "d1b3f7c4..."
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a document hosted at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected value for the
        document, False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be accessed (network error,
        404, etc.).
    """
    # Ensure the document is reachable. We don't actually need its content,
    # but a failed request indicates that the URL might be invalid.
    try:
        with urllib.request.urlopen(file_url, timeout=10) as resp:
            # Successful response; consume minimal data to keep the request alive.
            _ = resp.read(1)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Retrieve the expected signature. If we don't have an entry, treat as invalid.
    expected_sig = DOC_SIGNATURES.get(file_url)
    if expected_sig is None:
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign, expected_sig)