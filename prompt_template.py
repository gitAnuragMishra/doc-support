memory_prompt_template = '''
    <s>[INST] You are an AI RAG chat bot application. You're are having a conversation with a human. Answer his questions.
    Previous conversation: {history}
    Human: {human_input}
    AI: [/INST] '''