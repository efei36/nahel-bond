# Custom Character Chatbot (Nahel-Bond)

This project is a lightweight CLI interface with Anthropic's Claude LLM, which supports realistic conversations with custom characters. The spren from Brandon Sanderson's Stormlight Archive series are used as a generic template for conversations to give users an idea of this application's capabilities, but you are free to add your own characters.

Users can switch between text and speech input modes. The speech input mode allows the user to directly speak their queries, and also converts the LLM responses into audio that the user can listen to.

## Installation
- Python 3.10.11 or later
- API Key: You will need an Anthropics Claude API key. Add it to a `.env` file in the root project directory
    ```ANTHROPIC_API_KEY=your_api_key_here```
- Required libraries listed in `requirements.txt`