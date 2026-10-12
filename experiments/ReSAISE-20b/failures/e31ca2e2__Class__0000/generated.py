# -*- coding: utf-8 -*-

"""
Document Management System – Edit Document Utility

This module provides a single function `edit_doc` that allows authorized users
to modify the content of documents stored in an in‑memory database.
"""

from typing import Dict

# In‑memory representation of the document store.
# Each entry is a dict with keys: 'document_id', 'owner_id', and 'content'.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
    # Add more documents as needed.
}


def edit_doc(u_id: str, u_role: str, doc_id: str,
             doc_owner: str, new_body: str) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the document.
    u_role : str
        Role of the user ('viewer', 'editor', etc.).
    doc_id : str
        ID of the document to modify.
    doc_owner : str
        Expected owner ID of the document (for consistency check).
    new_body : str
        New content to store in the document.

    Returns
    -------
    str
        The updated document content if the operation succeeds.

    Raises
    ------
    ValueError
        If `doc_id` does not exist in the database.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    The function enforces that only users with role 'editor' and who are the
    document owner may modify a document.  The `doc_owner` argument is
    validated against the stored record to prevent tampering.
    """
    # 1. Validate that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # 2. Retrieve the stored document
    doc = DOCUMENTS_DB[doc_id]

    # 3. Cross‑check owner consistency
    if doc["owner_id"] != doc_owner:
        raise ValueError("Provided document owner does not match the record.")

    # 4. Authorization check – only editors who are the owner may modify
    if u_role.lower() != "editor" or u_id != doc_owner:
        raise PermissionError("User is not authorized to edit this document.")

    # 5. Perform the update
    doc["content"] = new_body

    # 6. Return the updated content
    return doc["content"]