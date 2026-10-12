# SPDX-License-Identifier: MIT
"""
Document management helper module.

This module contains a single function, `modify_document`, that safely updates
the content of a document stored in the global ``DOCUMENTS_DB`` dictionary.
The function enforces strict authorization checks to mitigate CWE‑863
(Incorrect Authorization) and other potential security risks.
"""

from __future__ import annotations

# Simulated in‑memory document database
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "userA", "content": "Initial text"}
}

def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str
) -> str:
    """
    Replace the content of an existing document after performing strict authorization.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the requesting user. Expected values are 'viewer' or 'editor'.
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        Owner ID stored in the document record (used for double‑check).
    modified_content : str
        New content that will replace the existing document text.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the requester is not authorized to modify the document.
    KeyError
        If the requested document does not exist in ``DOCUMENTS_DB``.
    ValueError
        If any of the required arguments are missing or invalid.

    Notes
    -----
    * The function performs **two** independent checks:
      1. `requester_role` must be 'editor'.
      2. The document ID in the database must match ``document_owner_id``.
    * These checks guard against accidental or malicious bypasses of the
      authorization logic (CWE‑863).
    * The function is intentionally stateless; it only mutates the global
      ``DOCUMENTS_DB`` entry for the given document.
    """

    # Basic input validation
    if not all(isinstance(arg, str) and arg for arg in [
        requester_id,
        requester_role,
        document_identifier,
        document_owner_id,
        modified_content
    ]):
        raise ValueError("All arguments must be non‑empty strings")

    # Ensure the document exists
    if document_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document {document_identifier} does not exist")

    # Retrieve the stored document record
    doc_record = DOCUMENTS_DB[document_identifier]

    # Validate that the supplied owner ID matches the stored one
    if doc_record.get("owner_id") != document_owner_id:
        raise PermissionError("Owner ID mismatch – potential tampering detected")

    # Authorization check: only editors can modify documents
    if requester_role.lower() != "editor":
        raise PermissionError("Insufficient permissions: only editors can modify documents")

    # Optional: verify that the requester is indeed the owner
    if requester_id != document_owner_id:
        raise PermissionError("Only the document owner can modify its content")

    # Perform the update
    doc_record["content"] = modified_content

    # Return the updated content for confirmation
    return doc_record["content"]