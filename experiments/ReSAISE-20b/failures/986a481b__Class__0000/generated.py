# -*- coding: utf-8 -*-
"""
Document revision helper for a corporate document management system.

The implementation ensures that only authorized users can modify documents.
It performs the following checks in order:

1. Verify that the requested document exists in ``DOCUMENTS_DB``.
2. Ensure the user is either:
   - The original creator of the document, or
   - An editor (role == 'editor').

If any check fails a :class:`PermissionError` is raised.  On success the
document's ``content`` field is updated and returned.
"""

from typing import Dict

# Sample in-memory database for demonstration purposes
DOCUMENTS_DB: Dict[str, Dict] = {
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Another document."},
    # ... more documents ...
}

def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str
) -> str:
    """
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    owner : str
        The ID of the user attempting the update.
    editor_role : str
        Role of the user ('viewer' or 'editor').
    doc_ref : str
        Unique identifier of the document to modify.
    doc_creator : str
        ID of the original creator of the document (redundant but validated).
    revised_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the requested document does not exist in ``DOCUMENTS_DB``.
    """
    # 1. Validate that the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_ref}' does not exist.")

    document = DOCUMENTS_DB[doc_ref]

    # 2. Validate that the provided creator matches the stored one
    if document["owner_id"] != doc_creator:
        raise PermissionError("Document creator mismatch; potential tampering detected.")

    # 3. Authorization check
    if owner != doc_creator and editor_role.lower() != "editor":
        raise PermissionError("User does not have permission to revise this document.")

    # 4. Perform the revision
    document["content"] = revised_content

    return document["content"]