import xml.sax.saxutils

def build_xml_response(content_to_add: str) -> str:
    """
    Build an XML response by inserting user-supplied content into a predefined template.

    Parameters
    ----------
    content_to_add : str
        Text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response that integrates the input from the user into the appropriate section of the template.

    Notes
    -----
    The function escapes special XML characters in ``content_to_add`` to avoid breaking the
    structure or introducing injection vulnerabilities.  It does not raise exceptions
    deliberately; any errors will propagate from the underlying XML escaping routine.
    """
    # Define the XML template with a placeholder for user content
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{content_to_add}</message>
</response>"""

    # Escape the user content to make it safe for XML
    escaped_content = xml.sax.saxutils.escape(content_to_add, entities={"'": "&apos;", '"': "&quot;"})

    # Insert the escaped content into the template
    return xml_template.format(content_to_add=escaped_content)