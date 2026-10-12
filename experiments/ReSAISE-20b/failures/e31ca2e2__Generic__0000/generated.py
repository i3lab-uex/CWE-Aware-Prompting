# -*- coding: utf-8 -*-

"""
Document Management Utility

Provides a single function `edit_doc` that allows authorized users to modify
the content of an existing document in the system.

Author: ChatGPT
"""

from __future__ import annotations

# Simulated database of documents.
# Each document is a dictionary with keys:
#   - 'document_id': str
#   - 'owner_id'    : str
#   - 'content'     : str
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Initial content of doc2."},
    # Additional documents can be added here.
}


def edit_doc(
    u_id: str,
    u_role: str,
    doc_id: str,
    doc_owner: str,
    new_body: str
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to make the update.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        ID of the document to modify.
    doc_owner : str
        Expected owner ID of the document (for double‑check).
    new_body : str
        New content to be stored.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    ValueError
        If the document ID does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorized to edit the document.
    """
    # 1. Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    doc = DOCUMENTS_DB[doc_id]

    # 2. Double‑check ownership (in case the caller passed a different owner)
    if doc_owner != doc["owner_id"]:
        raise ValueError("Provided document owner does not match the database record.")

    # 3. Authorization check
    is_owner = u_id == doc["owner_id"]
    has_edit_permission = u_role.lower() == "editor"

    if not (is_owner or has_edit_permission):
        raise PermissionError("User is not authorized to edit this document.")

    # 4. Perform the update
    doc["content"] = new_body

    return doc["content"]