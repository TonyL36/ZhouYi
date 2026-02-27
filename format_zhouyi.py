import re

def process_zhouyi(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define regex patterns for formatting
    # 1. Ensure "子曰" starts on a new line and is quoted properly
    # The previous content often had: "初九曰：... 子曰：..." or just "子曰：..." inline.
    # We want to format it as:
    # - **初九**：...
    #   > *子曰：...*
    # Or just a new line blockquote.

    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append("")
            continue

        # Handle "象曰" (Xiang Yue) inside Yao lines
        # Pattern: "- **Six/Nine...**: ... 象曰：..."
        if "象曰：" in line and (line.startswith("- **") or line.startswith("**")):
            # Split into two lines
            parts = line.split("象曰：")
            main_text = parts[0].strip()
            xiang_text = parts[1].strip()
            processed_lines.append(main_text)
            processed_lines.append(f"  > *象曰：{xiang_text}*")
            continue

        # Handle "子曰" (Zi Yue)
        # If line contains "子曰", it usually follows a question or statement.
        # Check if it's inline
        if "子曰" in line and not line.startswith("> **子曰") and not line.startswith("子曰"):
             # It might be "Something something. 子曰：..."
             parts = re.split(r'(子曰[：:])', line)
             # parts will be [pre, '子曰：', post, '子曰：', post...]
             
             current_line_text = ""
             for i, part in enumerate(parts):
                 if part.startswith("子曰"):
                     if current_line_text:
                         processed_lines.append(current_line_text)
                         current_line_text = ""
                     # Add Zi Yue as a blockquote
                     # Look ahead for the content
                     if i + 1 < len(parts):
                         ziyue_content = parts[i+1]
                         processed_lines.append(f"\n> *{part}{ziyue_content}*")
                         # Skip next part as it's consumed
                 elif i > 0 and parts[i-1].startswith("子曰"):
                     continue # Already handled
                 else:
                     current_line_text += part
             
             if current_line_text:
                 processed_lines.append(current_line_text)
             continue
        
        # General cleanup for lines starting with "象曰" or "子曰" not caught above
        if line.startswith("象曰："):
            processed_lines.append(f"> *{line}*")
        elif line.startswith("子曰：") or line.startswith("子曰"):
            processed_lines.append(f"> *{line}*")
        else:
            processed_lines.append(line)

    # Reassemble and do global replaces if needed
    result = "\n".join(processed_lines)
    
    # Fix potential double newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result

input_path = "backend/src/main/resources/data/ZhouYi.md"
output_path = "backend/src/main/resources/data/ZhouYi_formatted.md"

try:
    formatted_content = process_zhouyi(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    print("Formatting complete.")
    
    # Preview
    print(formatted_content[:1000])
    
except Exception as e:
    print(f"Error: {e}")
