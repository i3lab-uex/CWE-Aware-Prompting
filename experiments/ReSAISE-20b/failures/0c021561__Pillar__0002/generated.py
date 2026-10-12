# -*- coding: utf-8 -*-
"""
Document management helper module.

Provides the `revise_doc` function which updates a document's content
only if the caller has proper authorization.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Example in‑memory database of documents.
# In a real system this would be replaced with persistent storage
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # Example document structure:
    # "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."}
}

def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        ID of the user attempting to modify the document.
    usr_role : str
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the target document.
    creator_id : str
        The original creator's user ID for this document.
    updated_definition : str
        New content to replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If `docu_id` does not exist in the database.

    Notes
    -----
    * Authorization logic:
        - The user must be either the document owner (`owner_id`) or
          have an 'editor' role.
        - The `creator_id` argument is used only for additional validation
          and should match the document's stored owner.
    * All inputs are treated as strings. No further sanitization is
      performed here; callers should ensure that `updated_definition`
      does not contain malicious content before passing it.
    """
    # Verify the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # Basic validation of creator consistency
    if doc.get("owner_id") != creator_id:
        raise ValueError(
            "Provided creator_id does not match the document's owner."
        )

    # Authorization check
    is_owner = usr_id == doc.get("owner_id")
    has_editor_privilege = usr_role.lower() == "editor"

    if not (is_owner or has_editor_privilege):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized "
            "to modify document '{}'.".format(docu_id)
        )

    # Perform the update
    doc["content"] = updated_definition

    # Return the new content
    return doc["content"]