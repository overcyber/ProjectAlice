#  Copyright (c) 2025
#
#  This file, AnthropicLlm.py, is part of Project Alice.
#
#  Project Alice is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>
#
#  Last modified: 2025.03.31

import json
import requests
from typing import Dict, List, Optional

from core.dialog.model.DialogSession import DialogSession
from core.llm.model.Llm import Llm


class AnthropicLlm(Llm):
	"""Implementation of Anthropic's Claude API"""

	def __init__(self, **kwargs):
		super().__init__(name='anthropic', **kwargs)
		self._apiKey = self.ConfigManager.getAliceConfigByName('anthropicApiKey')
		self._model = self.ConfigManager.getAliceConfigByName('anthropicModel') or 'claude-3-haiku-20240307'
		self._apiUrl = 'https://api.anthropic.com/v1/messages'
		self._systemPrompt = self.ConfigManager.getAliceConfigByName('anthropicSystemPrompt') or 'You are a helpful assistant integrated with a smart home system. Respond in a concise and friendly manner.'
		self._temperature = self.ConfigManager.getAliceConfigByName('anthropicTemperature') or 0.7
		self._maxTokens = self.ConfigManager.getAliceConfigByName('anthropicMaxTokens') or 150
		self._online = bool(self._apiKey)

	def getResponse(self, session: DialogSession, text: str) -> Optional[str]:
		"""Get a response from Anthropic Claude"""
		if not self._apiKey or not self.InternetManager.online:
			self.logWarning('Anthropic integration is not available: missing API key or no internet connection')
			return None

		try:
			history = self.getConversationHistory(session)
			messages = []
			
			# Convert message history to Anthropic format
			for message in history:
				messages.append(message)

			headers = {
				'Content-Type': 'application/json',
				'x-api-key': self._apiKey,
				'anthropic-version': '2023-06-01'
			}

			data = {
				'model': self._model,
				'messages': messages,
				'system': self._systemPrompt,
				'temperature': self._temperature,
				'max_tokens': self._maxTokens
			}

			response = requests.post(self._apiUrl, headers=headers, data=json.dumps(data), timeout=10)
			response.raise_for_status()
			
			responseJson = response.json()
			answer = responseJson['content'][0]['text'].strip()
			
			# Add the exchange to history
			self.addToHistory(session, "user", text)
			self.addToHistory(session, "assistant", answer)
			
			return answer
			
		except Exception as e:
			self.logError(f'Error getting response from Anthropic: {e}')
			return None