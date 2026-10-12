# -*- coding: utf-8 -*-

"""
Document revision module.

This module provides a single function, `revise_document`, that updates
the content of a document in the global `DOCUMENTS_DB` dictionary.
The function enforces proper access control based on ownership and
role, mitigating CWE-284 (Improper Access Control).
"""

from typing import Dict

# Example in-memory database structure.
# In a real application this would be replaced by persistent storage
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # "doc_id": {"document_id": "doc_id", "owner_id": "user123", "content": "original text"}
}

def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str
) -> str:
    """
    Update the content of a document if the caller has sufficient privileges.

    Parameters
    ----------
    owner : str
        The ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller. Must be either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to be updated.
    doc_creator : str
        The ID of the original creator/owner of the document.
    revised_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the document.
    KeyError
        If the specified document does not exist in the database.

    Notes
    -----
    * The function checks that `doc_ref` exists in `DOCUMENTS_DB`.
      It also verifies that the caller is either the owner of the
      document or has an 'editor' role.
    * The `doc_creator` argument is compared against the stored
      `owner_id` field to ensure consistency.
    * No external libraries are used; the function is intentionally
      lightweight for educational purposes.

    Security Considerations
    -----------------------
    * This implementation mitigates CWE-284 by enforcing explicit
      ownership or role-based checks before performing the update.
    * Input sanitization is not performed here; callers should ensure
      that `revised_content` does not contain malicious code if it is
      later executed or rendered in a web context.
    """
    # Validate that the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_ref}' does not exist.")

    doc_record = DOCUMENTS_DB[doc_ref]

    # Verify that the provided creator matches the stored owner_id
    if doc_creator != doc_record["owner_id"]:
        raise PermissionError("Document creator mismatch; access denied.")

    # Authorization check: owner or editor role
    if not (owner == doc_creator or editor_role.lower() == "editor"):
        raise PermissionError("You do not have permission to modify this document.")

    # Perform the update
    doc_record["content"] = revised_content

    return doc_record["content"]