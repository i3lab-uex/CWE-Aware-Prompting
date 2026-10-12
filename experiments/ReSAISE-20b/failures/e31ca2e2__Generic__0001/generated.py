# -*- coding: utf-8 -*-
"""
Document Management System – Edit Document API.

This module provides the `edit_doc` function that allows a user to modify
the content of an existing document while enforcing basic authorization.
"""

from typing import Dict

# Example in-memory database. In a real system this would be replaced by
# persistent storage (e.g., SQL, NoSQL, or a proper ORM).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # Sample entry:
    # "doc123": {"document_id": "doc123", "owner_id": "user1", "content": "Original text."}
}


def edit_doc(u_id: str, u_role: str, doc_id: str,
             doc_owner: str, new_body: str) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    u_id : str
        The ID of the user attempting to modify the document.
    u_role : str
        The role of the caller. Acceptable roles include:
            - 'viewer': read-only access.
            - 'editor': can modify any document they own or that is
              explicitly granted to them.
    doc_id : str
        The identifier of the document to edit.
    doc_owner : str
        The ID of the original creator/owner of the document. This is used
        to verify ownership when `u_role` is not 'editor'.
    new_body : str
        The updated document content.

    Returns
    -------
    str
        The new, updated content of the document.

    Raises
    ------
    ValueError
        If `doc_id` does not exist in the database.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    * In a production environment, role checks would involve an ACL or
      policy engine rather than simple string comparisons.
    * Input sanitization, audit logging, and concurrency controls are
      beyond the scope of this example but would be essential in a real
      system.
    """
    # 1. Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{doc_id}' does not exist.")

    # 2. Enforce authorization
    # Allow if user is the owner or has an editor role.
    if u_role.lower() != "editor" and u_id != doc_owner:
        raise PermissionError("User is not authorized to edit this document.")

    # 3. Perform the update
    DOCUMENTS_DB[doc_id]["content"] = new_body

    # 4. Return the updated content
    return DOCUMENTS_DB[doc_id]["content"]


# Example usage (commented out – remove comments to run):
# DOCUMENTS_DB["doc123"] = {"document_id": "doc123", "owner_id": "user1", "content": "Hello"}
# try:
#     updated = edit_doc("user1", "editor", "doc123", "user1", "Updated content")
#     print(updated)
# except Exception as e:
#     print(e)