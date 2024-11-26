import os
import shutil
from markdown import markdown_to_html_node


def copy_static():
    if os.path.exists(os.path.join('public')):
        shutil.rmtree(os.path.join('public'))
    os.mkdir(os.path.join('public'))
    copy_files_recursive(os.path.join('static'), os.path.join('public'))

    

def copy_files_recursive(source_dir, dest_dir):
    directory = os.listdir(source_dir)
    
    for path in directory:
        if os.path.isfile(os.path.join(source_dir, path)):
            shutil.copy(os.path.join(source_dir, path), dest_dir)
        else:
            os.mkdir(os.path.join(dest_dir, path))
            copy_files_recursive(os.path.join(source_dir, path), os.path.join(dest_dir, path))


def extract_title(markdown):
    splitted_markdown = markdown.split("\n")
    
    for line in splitted_markdown:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header inside markdown")



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()
    
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    with open(dest_path, "w") as file:
        file.write(template)
        
def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    content_directory = os.listdir(dir_path_content)
    
    for element in content_directory:
        full_path = os.path.join(dir_path_content, element)

        if os.path.isdir(full_path):
            os.makedirs(os.path.join(dest_dir_path, element))
            generate_page_recursive(full_path, template_path, os.path.join(dest_dir_path, element))
        elif os.path.isfile(full_path):
            destination_file = os.path.join(dest_dir_path, element.replace('.md', '.html'))
            generate_page(full_path, template_path, destination_file)


def main():
    copy_static()
    generate_page_recursive(os.path.join("content"), os.path.join("template.html"), "public")
    
        

if __name__ == '__main__':
    main()