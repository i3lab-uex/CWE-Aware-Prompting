# -*- coding: utf-8 -*-
"""
Document revision helper for a corporate document management platform.
"""

from typing import Dict

# Example in-memory database. In production this would be replaced by a real DB.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user123", "content": "Initial content"},
    # ... more documents
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    owner : str
        The ID of the user attempting the update.
    editor_role : str
        Role of the caller; must be either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the target document.
    doc_creator : str
        The creator ID supplied by the caller; must match the stored owner.
    revised_content : str
        New content to replace the old document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the document.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If supplied creator ID does not match stored owner ID.
    """
    # 1. Verify the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_ref}' does not exist.")

    doc = DOCUMENTS_DB[doc_ref]

    # 2. Verify that the supplied creator matches the stored owner
    if doc_creator != doc["owner_id"]:
        raise ValueError("Provided creator ID does not match the document's actual owner.")

    # 3. Authorization check
    if editor_role != "editor" and owner != doc_creator:
        # Only editors or the original owner may modify
        raise PermissionError("You do not have permission to edit this document.")

    # 4. Perform the update
    doc["content"] = revised_content

    return doc["content"]