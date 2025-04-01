# Installing LLM Integration for ProjectAlice

This guide will help you install and configure the LLM conversation capability for ProjectAlice.

## Step 1: Add LLM Manager and Models

Copy the following directories to your ProjectAlice installation:

- `core/llm` - Contains the LLM Manager and provider implementations

## Step 2: Add LLM Conversation Skill

Copy the `skills/LlmConversation` directory to your ProjectAlice skills directory.

## Step 3: Update Configuration Template

Merge the `llm_config_patch.json` file into your `configTemplate.json`.

## Step 4: Register LLM Manager in SuperManager

Update the `SuperManager.py` file to include the LLM Manager:

1. Add `self.LlmManager = None` to the __init__ method
2. Add `from core.llm.LlmManager import LlmManager` to the imports
3. Add `self.LlmManager = LlmManager()` to the initialization code

## Step 5: Configure Your LLM API Keys

Configure your API keys through the ProjectAlice configuration interface:

1. OpenAI API Key (if using OpenAI): [Get API Key](https://platform.openai.com/api-keys)
2. Anthropic API Key (if using Anthropic): [Get API Key](https://console.anthropic.com/account/keys)
3. Google Gemini API Key (if using Gemini): [Get API Key](https://aistudio.google.com/app/apikey)

## Step 6: Restart ProjectAlice

Restart your ProjectAlice installation to apply the changes.

## Using LLM Conversation

Once installed, simply say "Let's talk" to your Alice assistant to start an LLM conversation.
Say "exit", "end conversation", or "stop talking" to return to normal Alice operation.

## Configuration Options

You can customize:
- Which LLM provider to use (OpenAI, Anthropic, or Gemini)
- The trigger phrases that activate LLM conversation mode
- System prompts for each LLM provider
- Temperature (creativity) and max tokens (response length) settings

## Troubleshooting

If you encounter issues:
1. Check API key validity
2. Ensure internet connectivity
3. Check logs for error messages
4. Verify that the LLM Manager is properly initialized