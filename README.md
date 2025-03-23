---
title: OpenAI Chainlit Chat App
emoji: 💬
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "latest"
app_file: app.py
pinned: false
---

# OpenAI Chainlit Chat App

A streamlined, production-ready chat application powered by OpenAI's GPT models and built with Chainlit. This app provides an interactive chat experience with streaming responses, similar to ChatGPT.

## Features

- 💬 **Real-time streaming responses** - See AI replies as they're being generated
- 🧠 **Full conversation memory** - AI maintains context throughout the chat
- 🔄 **Async processing** for optimal performance
- 🛠️ **Error handling** for robust operation

## Technical Details

This application is built with:
- **Chainlit** - Provides the modern chat interface
- **OpenAI API** - Powers the AI responses using GPT models
- **Docker** - Containerizes the application for easy deployment
- **UV** - Efficient Python package management

## Local Development

To run this application locally:

1. Clone the repository:
2. Create a `.env` file with your OpenAI API key:

3. Build and run with Docker:

4. Access the application at http://localhost:7860

## Deployment

This app is configured for easy deployment on Hugging Face Spaces. The Docker container automatically runs on port 7860 as required by Hugging Face.

Remember to add your OpenAI API key as a secret in the Hugging Face Space settings.

## Hugging Face Spaces Deployment

To deploy this app on Hugging Face Spaces:

1. Fork this repository to your GitHub account
2. Create a new Space on Hugging Face:
   - Choose "Docker" as the SDK
   - Connect to your GitHub repository

3. **Important**: Add your OpenAI API key to the Space:
   - Go to your Space's Settings
   - Find "Repository Secrets"
   - Add a new secret:
     - Name: `OPENAI_API_KEY`
     - Value: Your OpenAI API key
   - Click "Add Secret"

4. The Space will automatically rebuild with your API key configured

Note: Make sure your OpenAI API key has sufficient credits and proper permissions.

## License

MIT