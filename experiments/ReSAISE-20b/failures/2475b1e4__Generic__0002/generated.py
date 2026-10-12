# -*- coding: utf-8 -*-

"""
Utility module to construct an XML response from user supplied content.
"""

from xml.sax.saxutils import escape


# Example XML template with a placeholder for the user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{content_to_add}</message>
</response>"""


def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by inserting the user-supplied content into
    a predefined template.

    Parameters
    ----------
    content_to_add : str
        Text supplied by the user that will be inserted into the XML structure.

    Returns
    -------
    str
        The fully constructed XML string with the user content safely escaped.

    Notes
    -----
    - The function uses :func:`xml.sax.saxutils.escape` to ensure that
      special XML characters in the user input are properly escaped.
    - No exceptions are raised by this function; if ``content_to_add`` is
      not a string, it will be coerced to one.
    """
    # Ensure we are working with a string and escape XML special characters
    safe_content = escape(str(content_to_add))

    # Insert the escaped content into the template
    return xml_template.format(content_to_add=safe_content)