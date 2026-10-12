from __future__ import annotations

import typing as _t

# Example in‑memory database; in a real system this would be replaced by
# persistent storage (e.g., SQL, NoSQL, or a document store).
DOCUMENTS_DB: dict[str, dict[str, _t.Any]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    # ... other documents ...
}


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        ID of the user attempting to modify the document.
    operator_role : str
        Role of the user. Must be 'editor' to modify documents.
    doc_id : str
        Unique ID of the target document.
    doc_owner_id : str
        Owner ID stored in the database for comparison.
    updated_content : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated content after a successful modification.

    Raises
    ------
    PermissionError
        If the operator does not have permission to modify the document.
    KeyError
        If the specified document ID does not exist in ``DOCUMENTS_DB``.
    ValueError
        If required parameters are missing or invalid.

    Notes
    -----
    The function performs a simple role‑based access control check:
    only users with the 'editor' role and who own the document may modify it.
    """
    # Validate inputs
    if not all([operator_id, operator_role, doc_id, doc_owner_id, updated_content]):
        raise ValueError("All parameters must be provided and non‑empty.")

    # Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Enforce ownership and role checks
    if operator_role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role can modify documents.")

    # Optionally enforce that the operator is indeed the owner
    if operator_id != doc_owner_id:
        raise PermissionError("Only the document owner may modify this document.")

    # Update the document
    DOCUMENTS_DB[doc_id]["content"] = updated_content

    return DOCUMENTS_DB[doc_id]["content"]