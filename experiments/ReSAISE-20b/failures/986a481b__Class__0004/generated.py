# -*- coding: utf-8 -*-
"""
Document revision module.

The function `revise_document` updates a document's content in the
in-memory database `DOCUMENTS_DB`.  Authorization is performed by checking
that either:
    • the caller is the original owner of the document, or
    • the caller has an editor role.

If neither condition is met a `PermissionError` is raised.
"""

from __future__ import annotations
from typing import Dict

# Sample in‑memory database. In a real system this would be replaced
# by persistent storage (e.g., a relational database or document store).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "user_a", "content": "Initial text."}
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document after performing authorization checks.

    Parameters
    ----------
    owner : str
        The ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller, either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to be modified.
    doc_creator : str
        The ID of the user who originally created the document.
    revised_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the document.
    KeyError
        If `doc_ref` does not exist in the database.

    Notes
    -----
    - The function assumes that `DOCUMENTS_DB` contains entries in the form:
      {document_id: {"document_id": str, "owner_id": str, "content": str}}
    - The `doc_creator` argument is used to validate the original owner
      in case the caller's `owner` ID does not match the database record.
    """
    # 1. Verify that the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_ref}' does not exist.")

    doc_record = DOCUMENTS_DB[doc_ref]

    # 2. Authorization check
    is_owner = owner == doc_record["owner_id"]
    is_editor_role_valid = editor_role.lower() == "editor"

    # The caller must be the owner or have an editor role
    if not (is_owner or is_editor_role_valid):
        raise PermissionError(
            f"User '{owner}' with role '{editor_role}' is not authorized to modify document '{doc_ref}'."
        )

    # 3. Update the content
    doc_record["content"] = revised_content

    # 4. Return the new content
    return doc_record["content"]