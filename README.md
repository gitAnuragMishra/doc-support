# Doc Support

Doc Support is a powerful document management and interaction application built with Streamlit. It leverages advanced language models, vector databases, and embeddings to provide a seamless experience for interacting with and querying PDF documents. The application allows users to upload PDFs, interact with them using natural language, and retrieve information from them using AI-driven conversations.

## Features

-  **Chat with PDFs**:  Upload and interact with your PDF documents using natural language. The app processes the PDFs, breaks them down into manageable chunks, and indexes them in a vector database for efficient retrieval.
-  **Persistent Chat History**:  Save and load chat histories to continue conversations later. All chats are stored as JSON files, which can be reloaded in future sessions.
-  **Customizable Language Models**:  Integrate custom models using \`CTransformers\` for efficient language processing. The app is configured to run models with GPU acceleration using Nvidia CUDA.
-  **Memory Management**:  The app uses a memory buffer to maintain conversation context, allowing for more coherent and contextually aware responses.
-  **Vector Database Integration**:  Uses ChromaDB for storing and retrieving document embeddings, enabling quick and accurate information retrieval from large documents.
-  **Configuration Flexibility**:  Configurable paths for models, embeddings, vector databases, and chat histories using a \`config.yaml\` file.

##  Installation 

###  Prerequisites 

Ensure you have Python installed and set up on your machine. The project uses Python 3.8 or above. Create a virtual environment using venv
```bash
python -m venv [env-name]
```
###  Install Dependencies 

You can install the required dependencies using \`pip\`:

```bash
pip install -r requirements.txt
```
### **Requirements:**

chromadb==0.4.23
ctransformers==0.2.27
InstructorEmbedding==1.0.1
langchain==0.1.9
langchain-community==0.0.22
llama-cpp-python==0.2.20
pypdfium2==4.27.0
pyyaml==6.0.1
sentence-transformers==2.3.1
streamlit==1.31.1
transformers==4.38.1
torch==2.2.0
types-PyYAML
ctransformers[cuda]

**Note:** For CUDA support, separately install the appropriate versions of PyTorch and related packages:

```bash
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
```
## **Usage**

### **1\. Configure the Application**

Before running the application, ensure that you have configured the necessary paths and settings in the `config.yaml` file. The configuration includes paths for model files, embeddings, vector databases and chat history storage.

### **2\. Run the Application**

To start the Streamlit application, run the following command:

```bash
streamlit run app.py
```
This will launch the Doc Support application in your web browser.

  

### **3\. Interacting with the Application**

*   **Upload PDFs:** Use the sidebar to upload one or more PDF files. The uploaded PDFs will be processed and added to the vector database.
*   **Toggle Between PDF Chat and Normal Chat:** Use the toggle in the sidebar to switch between PDF-based chat and normal chat. This will call the appropriate chat chain (`pdfChatChain` for PDF interactions and `chatChain` for normal interactions).
*   **Chat Interface:** Enter your questions or prompts in the main chat area. The application will generate responses based on the content of the uploaded PDFs or general language model capabilities.
*   **Save/Load Sessions:** Select existing sessions from the dropdown in the sidebar to load previous chats, or start a new session. The chat history is saved automatically after each interaction.

### **4\. Maintenance**

The application includes maintenance scripts to clear the vector database and chat history:

*   **Clear Vector DB:**
```bash
python clear_vector_db.py
```
*   **Clear Chat History:**
```bash
python clear_chat_history.py
```
## **Project Structure**

*   `runner.py`: The main entry point for the Streamlit application.
*   `config.yaml`: Configuration file containing paths and settings for the application.
*   `llmchains.py`: Contains functions and classes for creating language model chains and managing chat interactions.
*   `pdf_handler.py`: Handles PDF extraction, text chunking, and vector database integration.
*   `utility.py`: Utility functions for saving and loading chat history, timestamp generation, and cleanup operations.
*   `clear_vector_db.py`: Script for clearing the contents of the vector database.
*   `clear_chat_history.py`: Script for clearing saved chat histories.
*   `requirements.txt`: List of required Python packages for the project.

## **Future Enhancements**
*   **ConversationalRetrievalChain:** Integrate the `ConversationalRetrievalChain` to allow for context-aware question generation. This feature will include the user's current question, as well as previous questions and responses, to generate new questions that incorporate the full chat history and context.
*   **Advanced Search:** Implement more advanced search and filtering capabilities within the chat interface.
*   **Custom Model Integration:** Simplify the process of integrating custom models for specialized tasks.


## **Contributing**

If you would like to contribute to the project, feel free to open a pull request or issue on the project's repository. Contributions are always welcome!


## **License**

This project is licensed under the MIT License.

  
This Markdown provides a comprehensive overview of the Doc Support project, including installation instructions, usage guidelines, the project structure, and future enhancements.

  

  

  

  
