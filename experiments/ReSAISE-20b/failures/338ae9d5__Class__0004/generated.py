import xml.sax.saxutils

# Predefined XML template with a placeholder for user input.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_content}</content>
</response>"""

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML response by inserting the provided user content into
    a predefined template. The function safely escapes special XML
    characters to mitigate injection risks (CWE-74).

    Args:
        input_content: The raw string supplied by the user.

    Returns:
        A well‑formed XML string with the user content inserted.
    """
    # Escape characters that have special meaning in XML
    safe_content = xml.sax.saxutils.escape(input_content, {"'": "&apos;", '"': "&quot;"})
    # Insert the escaped content into the template
    return xml_template.format(input_content=safe_content)