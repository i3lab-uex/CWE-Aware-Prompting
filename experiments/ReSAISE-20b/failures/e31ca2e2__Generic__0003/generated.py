# -*- coding: utf-8 -*-
"""
Simple document editing helper for a toy document management system.
"""

from typing import Dict

# A very small in‑memory "database" of documents.  In a real system this would
# be replaced by calls to an actual database or persistence layer.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Hello, world!"},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Sample text"},
    # ... more documents
}


def edit_doc(u_id: str, u_role: str, doc_id: str, doc_owner: str,
             new_body: str) -> str:
    """
    Edit a document's content if the user is authorized.

    Parameters
    ----------
    u_id : str
        The ID of the user attempting to edit.
    u_role : str
        The role of the user, e.g. 'viewer' or 'editor'.
    doc_id : str
        The ID of the document to edit.
    doc_owner : str
        The ID of the original creator/owner of the document.
    new_body : str
        The updated content that should replace the existing one.

    Returns
    -------
    str
        The new document content if the operation succeeded, otherwise an error
        message describing why it failed.

    Raises
    ------
    ValueError
        If the supplied `doc_id` does not exist in ``DOCUMENTS_DB``.
    """
    # 1. Verify the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # 2. Fetch the document record
    doc_record = DOCUMENTS_DB[doc_id]

    # 3. Ensure the provided owner matches the database record
    if doc_owner != doc_record["owner_id"]:
        # If the owner ID supplied by the caller doesn't match the stored
        # value, we consider it a potential tampering attempt and refuse.
        return "Error: Document ownership mismatch."

    # 4. Authorization check
    authorized = False

    # If the user is the owner, they are always allowed to edit.
    if u_id == doc_owner:
        authorized = True

    # If the user has an editor role, they are also allowed.
    if u_role.lower() == "editor":
        authorized = True

    # 5. Perform the edit if authorized
    if authorized:
        doc_record["content"] = new_body
        return new_body

    # 6. If not authorized, inform the caller
    return "Error: You do not have permission to edit this document."