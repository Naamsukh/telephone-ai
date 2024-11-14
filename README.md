# AI Phone Assistant (Vocode)

An AI-powered phone assistant that handles calls using Vocode, providing intelligent responses through speech recognition and synthesis.

## Prerequisites

- Docker and Docker Compose
- Twilio account credentials
- Deepgram API key 
- ElevenLabs API key
- Ngrok auth token (for local dev)

## Quick Start

1. Create `.env` file:
```bash
BASE_URL=your_base_url
DEEPGRAM_API_KEY=your_deepgram_key
ELEVEN_LABS_API_KEY=your_elevenlabs_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
NGROK_AUTH_TOKEN=your_ngrok_token
```

2. Build Docker image:
```bash
docker build -t telephone-ai-app .
```

3.Run with Docker Compose:
```bash
docker-compose up
```
