import os
from dotenv import load_dotenv
import chainlit as cl
from openai import AsyncOpenAI
import time

# Load environment variables from .env file
load_dotenv()

# Default model settings
DEFAULT_SETTINGS = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Provide clear and concise responses."

@cl.on_chat_start
async def start():
    """
    Initialize the chat session
    """
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Initialize OpenAI client (without test request)
        client = AsyncOpenAI(api_key=api_key)
        cl.user_session.set("client", client)
        
        # Initialize message history with system prompt
        message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        cl.user_session.set("message_history", message_history)
        
        # Save model settings
        cl.user_session.set("settings", DEFAULT_SETTINGS)
        
        await cl.Message(
            content="Hello! I'm your AI assistant powered by OpenAI. How can I help you today?"
        ).send()
        
    except ValueError as e:
        await cl.Message(
            content=f"⚠️ Configuration Error: {str(e)}\nPlease make sure OPENAI_API_KEY is set in the environment variables."
        ).send()
    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        if "session" in str(e).lower():
            error_msg = "⚠️ Session error. Please refresh the page and try again."
        await cl.Message(content=error_msg).send()

@cl.on_stop
async def on_stop():
    """Cleanup when the chat session ends"""
    try:
        cl.user_session.clear()
    except Exception:
        pass

async def handle_error(error: Exception) -> str:
    """Helper function to format error messages"""
    if "session" in str(error).lower():
        return "⚠️ Session error occurred. Please refresh the page and try again."
    return f"⚠️ An error occurred: {str(error)}"

@cl.on_message
async def main(user_message: cl.Message):
    """
    Process user messages and generate AI responses
    """
    try:
        # Retrieve session data
        client = cl.user_session.get("client")
        message_history = cl.user_session.get("message_history")
        settings = cl.user_session.get("settings")
        
        if not client or not message_history or not settings:
            raise ValueError("Session data not found. Please refresh the page.")
        
        # Add user message to history
        message_history.append({"role": "user", "content": user_message.content})
        
        # Prepare response message with loading state
        response_message = cl.Message(content="")
        await response_message.send()
        
        # Call OpenAI API to get response
        stream = await client.chat.completions.create(
            messages=message_history,
            stream=True,
            **settings
        )
        
        # Stream the response with buffering
        full_response = ""
        buffer = ""
        update_interval = 0.1  # Update every 100ms
        last_update_time = 0
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                buffer += chunk.choices[0].delta.content
                current_time = time.time()
                
                # Update UI when buffer reaches certain size or time has passed
                if len(buffer) >= 50 or (current_time - last_update_time) >= update_interval:
                    full_response += buffer
                    response_message.content = full_response
                    await response_message.update()
                    buffer = ""  # Clear buffer
                    last_update_time = current_time
        
        # Send any remaining buffer content
        if buffer:
            full_response += buffer
            response_message.content = full_response
            await response_message.update()
        
        # Add AI response to message history
        message_history.append({"role": "assistant", "content": full_response})
        cl.user_session.set("message_history", message_history)
        
    except Exception as e:
        error_message = await handle_error(e)
        response_message.content = error_message
        await response_message.update() 