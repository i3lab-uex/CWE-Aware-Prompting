# -------------------------------------------------------------
# Document revision module
# -------------------------------------------------------------
from typing import Dict

# Simulated document database
DOCUMENTS_DB: Dict[str, dict] = {
    # Example entry:
    # "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial text."}
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
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        The ID of the document to modify.
    creator_id : str
        The ID of the document's creator (owner).
    updated_definition : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document ID does not exist in the database.
    """
    # Check that the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document ID '{docu_id}' does not exist.")

    # Authorization check: only an editor who is also the owner may modify
    if usr_role.lower() != "editor" or usr_id != creator_id:
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # Perform the update
    DOCUMENTS_DB[docu_id]["content"] = updated_definition

    # Return the new content
    return DOCUMENTS_DB[docu_id]["content"]