# rev_doc.py

from typing import Dict, Any

# Simulated in‑memory document database
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content A"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content B"},
}

def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str
) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        The ID of the user attempting to make the update.
    usr_role : str
        The role the user holds (e.g., 'viewer' or 'editor').
    docu_id : str
        The ID of the document the user wants to modify.
    creator_id : str
        The ID of the document's creator (redundant with DOCUMENTS_DB entry).
    updated_definition : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content if the user is authorized.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document ID is not found in DOCUMENTS_DB.
    """
    # Verify that the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document ID '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # Ensure the creator_id matches the stored owner_id to avoid spoofing
    if doc["owner_id"] != creator_id:
        raise ValueError("Provided creator_id does not match the document's owner.")

    # Authorization check: only editors or the owner can modify
    if usr_role.lower() != "editor" and usr_id != doc["owner_id"]:
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    doc["content"] = updated_definition

    # Return the new content for confirmation
    return doc["content"]

# Example usage (uncomment to test)
# try:
#     new_content = revise_doc("userA", "editor", "doc1", "userA", "Updated content for doc1")
#     print("Update successful:", new_content)
# except Exception as e:
#     print(f"Error: {e}")