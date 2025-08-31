import os

def count_files(root_dir):
    file_count = 0
    for _, _, files in os.walk(root_dir):
        file_count += len(files)
    return file_count

if __name__ == "__main__":
    #root_dir = "D:\\画像\\Nextcloud_\\Photos" 
    root_dir = "N:\\Photos"
    print(count_files(root_dir))