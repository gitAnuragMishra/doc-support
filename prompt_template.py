memory_prompt_template = """<s>[INST] You are an AI chatbot named Doc-Support, having a conversation with a human. Answer his questions.[/INST]
    Previous conversation: {history}
    Human: {human_input}
    AI:"""
# memory_prompt_template = '''
#     <|system|>
#     {system_message}</s>
#     <|user|>
#     {prompt}</s>
#     <|assistant|>

# '''