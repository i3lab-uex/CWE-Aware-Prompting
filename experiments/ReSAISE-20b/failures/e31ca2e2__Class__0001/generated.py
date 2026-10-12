# -*- coding: utf-8 -*-
"""
Document editing module.

Author: ChatGPT
"""

from typing import Dict

# Example in-memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content"},
    # Add more documents as needed.
}


def edit_doc(u_id: str, u_role: str, doc_id: str,
             doc_owner: str, new_body: str) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the document.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        ID of the document to modify.
    doc_owner : str
        Owner ID stored in the document record.
    new_body : str
        New content to be saved.

    Returns
    -------
    str
        Updated document content if authorized, otherwise an error message.

    Raises
    ------
    ValueError
        If the document ID does not exist in DOCUMENTS_DB.
    """
    # Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # Authorization check: user must be the owner or have an editor role
    if u_id != doc_owner and u_role.lower() != "editor":
        return "Error: Unauthorized to edit this document."

    # Update the content
    DOCUMENTS_DB[doc_id]["content"] = new_body

    return DOCUMENTS_DB[doc_id]["content"]