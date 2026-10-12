# -*- coding: utf-8 -*-
"""
Document Management System – Edit Document

This module defines the `edit_doc` function that allows an authorized user
to modify a document's content. It performs strict authorization checks to
prevent CWE‑863 (Incorrect Authorization) and raises appropriate errors
for invalid inputs.
"""

from __future__ import annotations

# Sample in‑memory database of documents
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-A", "content": "Original content 1"},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-B", "content": "Original content 2"},
    # Add more documents as needed
}


def edit_doc(
    u_id: str,
    u_role: str,
    doc_id: str,
    doc_owner: str,
    new_body: str,
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to edit.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        ID of the document to be edited.
    doc_owner : str
        Expected owner ID of the document (for an extra consistency check).
    new_body : str
        New content to replace the existing document body.

    Returns
    -------
    str
        The updated content of the document upon successful edit.

    Raises
    ------
    ValueError
        If `doc_id` does not exist in the database.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    - Authorization logic: only users with role 'editor' or the owner of the
      document may modify it.
    - The function verifies that `doc_owner` matches the stored owner to
      guard against tampering.
    - The function is intentionally side‑effect free except for updating the
      in‑memory database; no external I/O is performed.
    """
    # 1. Validate document existence
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{doc_id}' does not exist.")

    doc_record = DOCUMENTS_DB[doc_id]

    # 2. Verify document owner matches the provided doc_owner
    if doc_record["owner_id"] != doc_owner:
        raise PermissionError("Provided document owner does not match system record.")

    # 3. Authorization check
    if u_role.lower() != "editor" and u_id != doc_owner:
        raise PermissionError("User is not authorized to edit this document.")

    # 4. Perform the update
    doc_record["content"] = new_body

    return doc_record["content"]