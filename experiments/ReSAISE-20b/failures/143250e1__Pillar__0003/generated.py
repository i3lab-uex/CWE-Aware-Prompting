# --------------------------------------------------------------
# Document modification with proper access control (CWE-284)
# --------------------------------------------------------------

from typing import Dict

# Simulated in‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content."},
    # Additional documents can be added here
}

def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str
) -> str:
    """
    Update the content of a document if the modifier is authorized.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the user, expected values: 'viewer' or 'editor'.
    doc_identifier : str
        Unique identifier of the document to be updated.
    creator_id : str
        The ID of the original document owner (for double‑check).
    updated_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated document content upon successful modification.

    Raises
    ------
    PermissionError
        If the user does not have edit privileges or if document ownership
        does not match the provided creator_id.
    KeyError
        If the specified document identifier is not present in DOCUMENTS_DB.
    ValueError
        If an unsupported role is supplied.
    """
    # Validate user role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role: {user_role}")

    # Only editors may modify documents
    if user_role != "editor":
        raise PermissionError("User does not have edit privileges.")

    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # Ensure the document's stored owner matches the provided creator_id
    if doc["owner_id"] != creator_id:
        raise PermissionError("Creator ID does not match the document owner.")

    # Ensure the modifier is indeed the owner
    if doc["owner_id"] != modifier_id:
        raise PermissionError("Only the document owner can modify its content.")

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]