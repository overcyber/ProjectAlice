#  Copyright (c) 2025
#
#  This file, OpenAiLlm.py, is part of Project Alice.
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


class OpenAiLlm(Llm):
	"""Implementation of OpenAI's GPT API"""

	def __init__(self, **kwargs):
		super().__init__(name='openai', **kwargs)
		self._apiKey = self.ConfigManager.getAliceConfigByName('openAiApiKey')
		self._model = self.ConfigManager.getAliceConfigByName('openAiModel') or 'gpt-3.5-turbo'
		self._apiUrl = 'https://api.openai.com/v1/chat/completions'
		self._systemPrompt = self.ConfigManager.getAliceConfigByName('openAiSystemPrompt') or 'You are a helpful assistant, responding in a concise and friendly manner.'
		self._temperature = self.ConfigManager.getAliceConfigByName('openAiTemperature') or 0.7
		self._maxTokens = self.ConfigManager.getAliceConfigByName('openAiMaxTokens') or 150
		self._online = bool(self._apiKey)

	def getResponse(self, session: DialogSession, text: str) -> Optional[str]:
		"""Get a response from OpenAI GPT"""
		if not self._apiKey or not self.InternetManager.online:
			self.logWarning('OpenAI integration is not available: missing API key or no internet connection')
			return None

		try:
			history = self.getConversationHistory(session)
			messages = [{"role": "system", "content": self._systemPrompt}]
			messages.extend(history)
			messages.append({"role": "user", "content": text})

			headers = {
				'Content-Type': 'application/json',
				'Authorization': f'Bearer {self._apiKey}'
			}

			data = {
				'model': self._model,
				'messages': messages,
				'temperature': self._temperature,
				'max_tokens': self._maxTokens
			}

			response = requests.post(self._apiUrl, headers=headers, data=json.dumps(data), timeout=10)
			response.raise_for_status()
			
			responseJson = response.json()
			answer = responseJson['choices'][0]['message']['content'].strip()
			
			# Add the exchange to history
			self.addToHistory(session, "user", text)
			self.addToHistory(session, "assistant", answer)
			
			return answer
			
		except Exception as e:
			self.logError(f'Error getting response from OpenAI: {e}')
			return None