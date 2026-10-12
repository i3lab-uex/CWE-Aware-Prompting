import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Inject user-supplied content into an HTML template after proper escaping.

    Parameters
    ----------
    input_content : str
        The raw content provided by the user. It may contain characters that need to be escaped.

    Returns
    -------
    str
        A complete HTML document with the user content safely embedded.
    """
    # Escape special HTML characters to prevent injection attacks and ensure well‑formedness.
    escaped_content = html.escape(input_content, quote=True)

    # Safely format the template. Using .format with a single placeholder ensures
    # that any remaining braces in escaped_content are treated as literal characters.
    final_html = html_template.format(user_content=escaped_content)

    return final_html