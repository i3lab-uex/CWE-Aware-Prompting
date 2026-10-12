import re
import html

def build_html_content(html_template: str, user_values: dict) -> str:
    """
    Replace placeholders in an HTML template with user-supplied values, ensuring
    that all inserted content is properly escaped to prevent XSS attacks.

    Args:
        html_template (str): The HTML template containing placeholders.
                             Placeholders are identified by curly braces,
                             e.g. {name} or {{name}}.
        user_values (dict): Mapping from placeholder names to values.

    Returns:
        str: The processed HTML with placeholders replaced by escaped user values.

    Raises:
        ValueError: If a placeholder in the template has no corresponding entry
                    in `user_values`, or if any error occurs during processing.
    """
    # Regular expression to find placeholders like {name} or {{name}}
    placeholder_pattern = re.compile(r'\{({\w+})\}|\{\{(\w+)\}\}')

    def _replace(match: re.Match) -> str:
        # Determine which group matched
        key = match.group(1) or match.group(2)
        if key not in user_values:
            raise ValueError(f"Missing value for placeholder '{key}'")
        # Escape the user-provided value
        return html.escape(str(user_values[key]), quote=True)

    try:
        result = placeholder_pattern.sub(_replace, html_template)
    except re.error as exc:
        raise ValueError(f"Regex error while processing template: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Unexpected error during template processing: {exc}") from exc

    return result