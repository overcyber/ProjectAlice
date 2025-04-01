# Project Alice - AI-LLM Integration

This repository contains an implementation for integrating AI Large Language Models (LLMs) with Project Alice, enabling advanced conversational capabilities.

## Features

- Integration with popular LLM providers:
  - OpenAI (GPT models)
  - Anthropic (Claude models)
  - Google (Gemini models)
- Configurable via Alice's configuration interface
- Activated by saying "Let's talk" (configurable trigger phrases)
- Allows natural, context-aware conversations with your Alice assistant
- Memory of conversation history for coherent multi-turn dialogues

## Configuration

To enable LLM conversations:

1. Add your API keys in the configuration:
   - OpenAI API key in `openAiApiKey`
   - Anthropic API key in `anthropicApiKey`
   - Google Gemini API key in `geminiApiKey`

2. Select which LLM to use in `activeLlm`

3. Customize system prompts for each provider if needed

4. Adjust temperature and token settings to control response length and creativity

## Usage

Simply say "Let's talk" to your Alice assistant, and it will activate the LLM conversation mode.
During an LLM conversation, any utterance that isn't recognized as a specific intent will be
sent to the LLM for processing.

Say "exit", "end conversation", or "stop talking" to return to normal Alice operation.

## Integration

This implementation consists of:

1. LLM Manager - Core component managing LLM API calls
2. LLM Providers - Implementation for each supported LLM API
3. LLM Conversation Skill - Skill to handle conversations with LLMs

## Requirements

- Internet connection
- API keys for at least one LLM provider
- Project Alice v1.0.0-b5 or later