# -*- coding: utf-8 -*-
"""
Document management helper.

The `edit_doc` function performs a safe authorization check before
allowing content modifications.  It guards against the common CWE‑863
“Incorrect Authorization” flaw by ensuring that only an editor or the
document owner can update a document.
"""

from __future__ import annotations

# Example in‑memory database; replace with real persistence as needed.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entries:
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Another document."},
}


def edit_doc(u_id: str, u_role: str, doc_id: str, doc_owner: str, new_body: str) -> str:
    """
    Modify the content of a document if the caller is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to edit.
    u_role : str
        Role of the caller (e.g., 'viewer', 'editor').
    doc_id : str
        Identifier of the document to edit.
    doc_owner : str
        Owner ID of the target document (used for quick check; should match the DB).
    new_body : str
        The new content to store.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    ValueError
        If the document does not exist in `DOCUMENTS_DB`.

    Notes
    -----
    * Authorization is enforced by verifying that the caller is either
      an editor (`u_role == 'editor'`) or the owner of the document.
    * The `doc_owner` argument is cross‑checked against the database to
      prevent tampering.
    """
    # 1. Validate document existence
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # 2. Verify the document's actual owner matches the supplied `doc_owner`
    stored_doc = DOCUMENTS_DB[doc_id]
    if doc_owner != stored_doc["owner_id"]:
        raise ValueError("Provided document owner does not match the record.")

    # 3. Authorization check (CWE‑863 safe)
    if u_role != "editor" and u_id != doc_owner:
        return "Error: User is not authorized to edit this document."

    # 4. Perform the update
    stored_doc["content"] = new_body

    return stored_doc["content"]