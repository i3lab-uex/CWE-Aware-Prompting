# -*- coding: utf-8 -*-
"""
Document management utilities.
"""

from typing import Dict

# Example in‑memory document store
DOCUMENTS_DB: Dict[str, dict] = {
    # 'doc_id': {'document_id': str, 'owner_id': str, 'content': str}
    # Example:
    # 'doc1': {'document_id': 'doc1', 'owner_id': 'user123', 'content': 'Initial content'},
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
        The ID of the user attempting to make the update.
    usr_role : str
        The role the user holds (e.g., 'viewer' or 'editor').
    docu_id : str
        The ID of the document to modify.
    creator_id : str
        The ID of the document's creator (owner).
    updated_definition : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the document ID is not found in ``DOCUMENTS_DB``.
    """
    # Ensure the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{docu_id}' does not exist.")

    # Authorization check: user must be an editor or the owner
    if usr_role.lower() != "editor" and usr_id != creator_id:
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized "
            f"to modify document '{docu_id}'."
        )

    # Perform the update
    DOCUMENTS_DB[docu_id]["content"] = updated_definition

    # Return the new content
    return DOCUMENTS_DB[docu_id]["content"]