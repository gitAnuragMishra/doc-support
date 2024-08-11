import time
import os
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def main():
    time.sleep(2)  # time to release 
    if os.path.exists(config['chat_history_path']):
            for root, dirs, files in os.walk(config['chat_history_path']):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        print(f"Error deleting file {file}: {e}")                
            print(f"Cleared chat history at: {config['chat_history_path']}")    


if __name__ == '__main__':
    main()