import json
from langchain.schema.messages import AIMessage, HumanMessage
from datetime import datetime



def save_chat_history_json(chat_history, file_path):
    with open(file_path, 'w') as f:

        json_data = [message.dict() for message in chat_history]
        json.dump(json_data, f)

def load_chat_history_json(file_path):
    with open(file_path, 'r') as f:
        # data = json.load(f)
        # messages = [] 
        # for message in data:
        #     messages.append([HumanMessage(**message) if message[type] == 'human' else AIMessage(**message)])
        # return messages
        json_data = json.load(f)
        messages = [HumanMessage(**message) if message["type"] == "human" else AIMessage(**message) for message in json_data]
        return messages
    
def get_timestamp():
    return datetime.now().strftime("%d.%m.%Y_%H.%M.%S")