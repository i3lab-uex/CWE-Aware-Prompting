import xml.sax.saxutils

# Pre‑defined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<message>
    <content>{content_insert}</content>
</message>"""

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by safely inserting user-supplied content
    into a predefined template.

    Parameters:
        content_insert (str): Text supplied by the user to be inserted
                              into the XML structure.

    Returns:
        str: The constructed XML string with user content safely escaped.
    """
    # Escape special XML characters to prevent injection (CWE‑74).
    safe_content = xml.sax.saxutils.escape(content_insert, entities={
        "'": "&apos;",
        "\"": "&quot;"
    })

    # Format the template with the escaped content.
    return xml_template.format(content_insert=safe_content)