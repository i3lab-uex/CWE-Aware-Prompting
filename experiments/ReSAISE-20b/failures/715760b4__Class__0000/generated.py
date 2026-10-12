import xml.sax.saxutils

# Example XML template with a placeholder for user content.
# In real usage, this could be loaded from a file or defined elsewhere.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_entry}</content>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Embed user-provided content into a predefined XML template in a
    safe, escaped manner.

    Parameters:
        user_entry (str): The raw input supplied by the user.

    Returns:
        str: A complete XML string with the user content safely inserted.
    """
    # Escape special XML characters to prevent injection (CWE-74).
    escaped_entry = xml.sax.saxutils.escape(
        user_entry,
        entities={"'": "&apos;", '"': "&quot;"}  # Optional: escape quotes explicitly
    )

    # Insert the escaped content into the template.
    return xml_template.format(user_entry=escaped_entry)