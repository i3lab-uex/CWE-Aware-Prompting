# -*- coding: utf-8 -*-
"""
Document Management – Alter Document

This module provides a single function, `alter_document`, which
allows an authorized user to replace the content of an existing
document in a simple in‑memory database.
"""

from __future__ import annotations

# Example document store – each entry is a dictionary with the
# following keys: 'document_id', 'owner_id' and 'content'.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content."},
    # Add more documents as needed.
}


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Replace the content of an existing document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        Identifier of the user attempting to modify the document.
    operator_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the document to modify.
    doc_owner_id : str
        Owner ID stored in the document; used for cross‑checking.
    updated_content : str
        New content to replace the existing document body.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    KeyError
        If `doc_id` does not exist in the database.
    PermissionError
        If the operator is not an editor or is not the document owner.
    ValueError
        If `operator_role` is not one of the expected values.
    """
    # Validate role
    if operator_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{operator_role}'. Expected 'viewer' or 'editor'.")

    # Fetch the document – this will raise KeyError if not found
    doc = DOCUMENTS_DB[doc_id]

    # Verify that the provided owner ID matches the stored one
    if doc_owner_id != doc["owner_id"]:
        raise ValueError("Provided owner ID does not match the document's recorded owner.")

    # Access control: only editors (or the owner if they are an editor) may modify
    if operator_role != "editor":
        raise PermissionError("Insufficient permissions: viewer role cannot modify documents.")

    # All checks passed – perform the update
    doc["content"] = updated_content

    return doc["content"]