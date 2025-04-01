#  Copyright (c) 2025
#
#  This file, LlmManager.py, is part of Project Alice.
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

from typing import Dict, Optional

from core.base.model.Manager import Manager
from core.commons import constants
from core.dialog.model.DialogSession import DialogSession
from core.llm.model.Llm import Llm
from core.llm.model.OpenAiLlm import OpenAiLlm
from core.llm.model.AnthropicLlm import AnthropicLlm
from core.llm.model.GeminiLlm import GeminiLlm


class LlmManager(Manager):
	"""Manager for Large Language Model integration"""

	def __init__(self):
		super().__init__()
		self._llms: Dict[str, Llm] = {}
		self._activeLlm: Optional[Llm] = None
		self._triggerPhrases = []

	def onStart(self):
		super().onStart()
		
		# Initialize LLM providers
		self._llms['openai'] = OpenAiLlm()
		self._llms['anthropic'] = AnthropicLlm()
		self._llms['gemini'] = GeminiLlm()
		
		# Set active LLM from config
		activeLlmName = self.ConfigManager.getAliceConfigByName('activeLlm') or 'openai'
		self._activeLlm = self._llms.get(activeLlmName)
		
		if not self._activeLlm:
			self.logWarning(f"Configured LLM '{activeLlmName}' not found, defaulting to OpenAI")
			self._activeLlm = self._llms.get('openai')
		
		# Load trigger phrases
		self._triggerPhrases = self.ConfigManager.getAliceConfigByName('llmTriggerPhrases') or ["let's talk", "let us talk"]
		
		# Check if we have at least one LLM available
		if not any(llm.online for llm in self._llms.values()):
			self.logWarning("No LLM is available. Please check API keys in configuration.")
			return
			
		self.logInfo(f'Using {self._activeLlm.name} as active LLM provider')

	def onBooted(self):
		self.MqttManager.subscribeSkillIntents(intents=['hermes/intent/#'])

	def getResponse(self, session: DialogSession, text: str) -> Optional[str]:
		"""
		Get a response from the active LLM for the given text
		:param session: the dialog session
		:param text: the text to get a response for
		:return: the LLM response or None if an error occurred
		"""
		if not self._activeLlm or not self._activeLlm.online:
			self.logWarning('No active LLM available')
			return None
			
		return self._activeLlm.getResponse(session, text)
		
	def isLlmTrigger(self, text: str) -> bool:
		"""
		Check if the text contains a trigger phrase for LLM integration
		:param text: the text to check
		:return: True if the text contains a trigger phrase
		"""
		text = text.lower()
		return any(phrase.lower() in text for phrase in self._triggerPhrases)
	
	def clearHistory(self, deviceUid: str) -> None:
		"""
		Clear conversation history for all LLMs for the given device
		:param deviceUid: the device UID
		"""
		for llm in self._llms.values():
			llm.clearHistory(deviceUid)
			
	@property
	def triggerPhrases(self) -> list:
		return self._triggerPhrases
		
	@property
	def activeLlm(self) -> Optional[Llm]:
		return self._activeLlm