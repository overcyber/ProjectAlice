#  Copyright (c) 2025
#
#  This file, GeminiLlm.py, is part of Project Alice.
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


class GeminiLlm(Llm):
	"""Implementation of Google's Gemini API"""

	def __init__(self, **kwargs):
		super().__init__(name='gemini', **kwargs)
		self._apiKey = self.ConfigManager.getAliceConfigByName('geminiApiKey')
		self._model = self.ConfigManager.getAliceConfigByName('geminiModel') or 'gemini-1.0-pro'
		self._apiUrl = f'https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent'
		self._systemPrompt = self.ConfigManager.getAliceConfigByName('geminiSystemPrompt') or 'You are a helpful assistant integrated with a smart home system. Respond in a concise and friendly manner.'
		self._temperature = self.ConfigManager.getAliceConfigByName('geminiTemperature') or 0.7
		self._maxTokens = self.ConfigManager.getAliceConfigByName('geminiMaxTokens') or 150
		self._online = bool(self._apiKey)

	def getResponse(self, session: DialogSession, text: str) -> Optional[str]:
		"""Get a response from Google Gemini"""
		if not self._apiKey or not self.InternetManager.online:
			self.logWarning('Gemini integration is not available: missing API key or no internet connection')
			return None

		try:
			history = self.getConversationHistory(session)
			contents = []
			
			# Add system prompt
			contents.append({
				"role": "user",
				"parts": [{"text": self._systemPrompt}]
			})
			
			contents.append({
				"role": "model",
				"parts": [{"text": "I'll help you as a smart home assistant."}]
			})
			
			# Add conversation history
			for message in history:
				role = "user" if message["role"] == "user" else "model"
				contents.append({
					"role": role,
					"parts": [{"text": message["content"]}]
				})
			
			# Add current message
			contents.append({
				"role": "user",
				"parts": [{"text": text}]
			})

			params = {
				"key": self._apiKey
			}

			data = {
				"contents": contents,
				"generationConfig": {
					"temperature": self._temperature,
					"maxOutputTokens": self._maxTokens,
					"topP": 0.95,
					"topK": 40
				}
			}

			response = requests.post(self._apiUrl, params=params, json=data, timeout=10)
			response.raise_for_status()
			
			responseJson = response.json()
			answer = responseJson["candidates"][0]["content"]["parts"][0]["text"].strip()
			
			# Add the exchange to history
			self.addToHistory(session, "user", text)
			self.addToHistory(session, "assistant", answer)
			
			return answer
			
		except Exception as e:
			self.logError(f'Error getting response from Gemini: {e}')
			return None