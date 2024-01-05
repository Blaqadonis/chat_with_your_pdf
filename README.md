# Chat With Your PDF
### Powered by 🅱🅻🅰🆀 
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Overview
```Chat With Your PDF``` is an innovative tool that allows users to interact with PDF documents through a conversational interface. Leveraging the power of OpenAI's language models and Cassandra's database capabilities, this application provides a unique way to extract and query information from PDF files.

## Features
- **Interactive Chat Interface:** Users can ask questions and get information directly from their uploaded PDF documents.
- **Powered by OpenAI:** Utilizes advanced language models for accurate text interpretation and response generation.
- **Efficient Data Handling:** Integrates with Cassandra for robust data management and querying capabilities.
- **PDF Processing:** Processes PDF documents to extract and index their contents for easy querying.

## Technologies
- Streamlit
- OpenAI Language Models
- Cassandra Database
- LangChain
- Python

## Installation
Before you can run the application, ensure you have Python installed along with the necessary libraries. Follow these steps to set up the project:

```bash
git clone https://github.com/Blaqadonis/chat-with-your-pdf.git
cd chat-with-your-pdf
pip install -r requirements.txt
```

## Usage
To run the application:
``` streamlit run chatbot.py ```

Make sure your Cassandra instance is up and running, and the necessary files (secure-connect-pdf-qa1.zip, PDF documents, etc.) are correctly placed.

## Configuration
Set up your environment variables for Cassandra (```ASTRA_DB_CLIENTID``` and ```ASTRA_DB_SECRET```) and OpenAI (```OPENAI_API_KEY```).

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- OpenAI for the GPT models
- DataStax Astra for the Cassandra database solutions
- The Streamlit team for the web app framework

