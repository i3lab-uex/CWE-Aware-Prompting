import html

# The base HTML template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def construct_html_response(content: str) -> str:
    """
    Construct a safe HTML response by escaping user-provided content
    and injecting it into the html_template.

    Parameters:
        content (str): The dynamic content supplied by the user.

    Returns:
        str: A complete HTML string with the escaped user content.
    """
    # Escape special characters to prevent injection (CWE-74)
    safe_content = html.escape(content, quote=True)

    # Inject the escaped content into the template
    return html_template.format(user_content=safe_content)