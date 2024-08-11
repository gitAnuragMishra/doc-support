import time
import os
import shutil
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
def main():  #clear all contents of vector db
        ##to be noted: having this function out of the main funtion causes a permission error 
        time.sleep(2)  # time to release 
        if os.path.exists(config['vector_db_path']):
            for root, dirs, files in os.walk(config['vector_db_path']):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        print(f"Error deleting file {file}: {e}")
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir))
                    except Exception as e:
                        print(f"Error deleting directory {dir}: {e}")
            print(f"Cleared contents of vector DB folder: {config['vector_db_path']}")


if __name__ == '__main__':
    main()