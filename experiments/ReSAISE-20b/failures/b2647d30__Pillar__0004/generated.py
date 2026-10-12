# SPDX-License-Identifier: MIT
"""
A minimal document management helper that enforces access control.

The implementation focuses on preventing CWE‑284: Improper Access Control.
Only users with the 'editor' role or the document owner may modify a
document. Unauthorized attempts raise PermissionError.
"""

from __future__ import annotations

# Example in‑memory database. In a real system this would be replaced by
# a persistent store (SQL, NoSQL, etc.).
DOCUMENTS_DB: dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    # Additional documents can be added here.
}


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of an existing document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting to modify the document.
    operator_role : str
        The role of the user; accepted values are 'viewer' or 'editor'.
    doc_id : str
        The unique identifier of the document to be updated.
    doc_owner_id : str
        The owner ID that should match the stored document's owner.
    updated_content : str
        New content to replace the current document text.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the operator does not have permission to modify the document.
    KeyError
        If `doc_id` is not found in ``DOCUMENTS_DB``.
    ValueError
        If an unexpected role value is supplied.

    Notes
    -----
    * The function performs a strict equality check for the document owner.
    * Only users with role 'editor' or who are the document owner may modify a
      document. Viewers and any other roles are denied.
    * The function is intentionally stateless; it only mutates the in‑memory
      dictionary for demonstration purposes.
    """
    # Validate role input early to avoid ambiguous behavior
    if operator_role not in {"viewer", "editor"}:
        raise ValueError(f"Unknown role: {operator_role!r}")

    # Ensure the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document {doc_id!r} does not exist")

    # Retrieve the document record
    doc = DOCUMENTS_DB[doc_id]

    # Enforce access control: only editors or the owner can modify
    if operator_role != "editor" and operator_id != doc_owner_id:
        raise PermissionError(
            f"User {operator_id!r} does not have permission to modify document {doc_id!r}"
        )

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]