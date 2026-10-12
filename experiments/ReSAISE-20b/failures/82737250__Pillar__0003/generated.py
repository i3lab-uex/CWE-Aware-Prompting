from typing import Dict

# Sample in‑memory document store. In a real system this would be replaced
# by a database or secure storage layer.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content"},
    # Add more documents as needed
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str
) -> str:
    """
    Update the content of a document if the requester has permission.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the requester ('viewer' or 'editor').
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        Owner ID of the document (used for consistency checks).
    modified_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the requester is not an editor or does not own the document.
    KeyError
        If the document_identifier does not exist in DOCUMENTS_DB.
    """
    # Validate role
    if requester_role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role can modify documents.")

    # Retrieve document from the database
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{document_identifier}' not found.") from exc

    # Ensure the owner_id matches
    if doc["owner_id"] != document_owner_id:
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Ensure the requester is indeed the owner
    if doc["owner_id"] != requester_id:
        raise PermissionError("Only the document owner can modify its content.")

    # Perform the update
    doc["content"] = modified_content

    return doc["content"]