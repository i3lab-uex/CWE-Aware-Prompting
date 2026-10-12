#!/usr/bin/env python3
"""
Utility to load a file only if its cryptographic signature is known and trusted.
"""

import os
from pathlib import Path
from typing import Dict

# Global dictionary mapping filenames to their valid signatures.
# Example: {"example.txt": "a1b2c3d4..."}
VALID_SIGNATURES: Dict[str, str] = {
    # Populate with actual file names and signatures as required.
}


def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from the filesystem only if its signature is trusted.

    Parameters
    ----------
    file_name : str
        Name of the file to load. Must be a relative path within the current working directory.
    signature : str
        Cryptographic signature (e.g., SHA-256 hex digest) claimed for the file.

    Returns
    -------
    int
        1 if the signature is valid and the file was loaded successfully, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the provided file name attempts a path traversal attack.

    Notes
    -----
    - The function checks that the file name is relative and does not contain '..' segments
      to prevent directory traversal attacks.
    - The signature verification is performed by comparing the supplied signature against
      a pre‑trusted dictionary `VALID_SIGNATURES`. No additional cryptographic checks are
      performed on the file contents.
    """
    # Prevent directory traversal by ensuring the path is relative and does not contain '..'
    p = Path(file_name)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"Invalid file name: {file_name!r}")

    # Resolve the path relative to current working directory
    full_path = Path.cwd() / p

    # Check file existence; raise FileNotFoundError if missing
    if not full_path.is_file():
        raise FileNotFoundError(f"No such file: {full_path}")

    # Verify signature against the trusted dictionary
    expected_sig = VALID_SIGNATURES.get(file_name)
    if expected_sig is None or expected_sig != signature:
        # Signature mismatch; do not load the file
        return 0

    # At this point, the signature is trusted. Load the file (here we simply read its contents).
    # The content can be processed as needed; for this example, we'll just read it.
    with full_path.open("rb") as fh:
        _ = fh.read()  # placeholder for actual processing

    return 1