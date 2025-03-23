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

## License

MIT