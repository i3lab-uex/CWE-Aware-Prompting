import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "abcd1234efgh5678",
    "https://example.org/files/report.txt": "deadbeefcafebabe",
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate that the supplied cryptographic signature matches the expected
    signature for a document located at ``file_url``.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        ``True`` if the signature matches the expected value for the document,
        ``False`` otherwise.

    Raises
    ------
    IOError
        If the document at ``file_url`` cannot be accessed (e.g., network error,
        HTTP 404, etc.).
    """
    # Check that the URL is reachable
    try:
        with urllib.request.urlopen(file_url, timeout=10) as response:
            # We only need to verify accessibility; no need to read content.
            if response.status >= 400:
                raise IOError(f"Failed to access {file_url}: HTTP {response.status}")
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access {file_url}") from exc

    # Retrieve the expected signature for this URL
    expected_sign = DOC_SIGNATURES.get(file_url)
    if expected_sign is None:
        # No known signature for this document – treat as invalid
        return False

    # Use a timing‑safe comparison to prevent side‑channel attacks
    return hmac.compare_digest(sign, expected_sign)