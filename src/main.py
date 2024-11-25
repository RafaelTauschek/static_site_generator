from textnode import TextNode
import os
import shutil


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
        


def main():
    copy_static()
        

main()