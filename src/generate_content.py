from markdown_to_html import markdown_to_html_node
import os

def extract_title(markdown:str):
    lines = markdown.split("\n")
    for line in lines:
        if line.split(" ", 1)[0] == "#":
            return line.split(" ", 1)[1].strip()
    raise ValueError("No h1 headings found")

def generate_page(from_path:str, template_path:str, dest_path:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        markdown_data = f.read()
    
    with open(template_path, encoding="utf-8") as f:
        template_data = f.read()
    
    html_string = markdown_to_html_node(markdown_data).to_html()
    
    title = extract_title(markdown_data)
    
    full_html = template_data.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
  
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)