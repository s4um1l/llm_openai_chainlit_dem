import os
from dotenv import load_dotenv
import chainlit as cl
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

# Default model settings
DEFAULT_SETTINGS = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Provide clear and concise responses."

@cl.on_chat_start
async def start():
    """
    Initialize the chat session:
    - Create OpenAI client
    - Set up message history with system prompt
    - Configure model settings
    - Send welcome message
    """
    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    cl.user_session.set("client", client)
    
    # Initialize message history with system prompt
    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    cl.user_session.set("message_history", message_history)
    
    # Save model settings
    cl.user_session.set("settings", DEFAULT_SETTINGS)
    
    # Send welcome message
    await cl.Message(
        content="Hello! I'm your AI assistant powered by OpenAI. How can I help you today?"
    ).send()


@cl.on_message
async def main(user_message: cl.Message):
    """
    Process user messages and generate AI responses:
    - Update message history with user input
    - Call OpenAI API with current conversation context
    - Stream the response back to the user
    - Update message history with AI response
    
    Args:
        user_message: The message sent by the user
    """
    # Retrieve session data
    client = cl.user_session.get("client")
    message_history = cl.user_session.get("message_history")
    settings = cl.user_session.get("settings")
    
    # Add user message to history
    message_history.append({"role": "user", "content": user_message.content})
    
    # Prepare response message with loading state
    response_message = cl.Message(content="")
    await response_message.send()
    
    try:
        # Call OpenAI API to get response
        stream = await client.chat.completions.create(
            messages=message_history,
            stream=True,
            **settings
        )
        
        # Stream the response
        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content_chunk = chunk.choices[0].delta.content
                full_response += content_chunk
                
                # Update message in real-time
                response_message.content = full_response
                await response_message.update()
        
        # Add AI response to message history
        message_history.append({"role": "assistant", "content": full_response})
        cl.user_session.set("message_history", message_history)
        
    except Exception as e:
        # Handle errors
        response_message.content = f"Error: {str(e)}"
        await response_message.update() 