#  Copyright (c) 2025
#
#  This file, Llm.py, is part of Project Alice.
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

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from core.base.model.ProjectAliceObject import ProjectAliceObject
from core.dialog.model.DialogSession import DialogSession


class Llm(ProjectAliceObject, ABC):
	"""Base abstract class for LLM (Large Language Model) implementations"""

	def __init__(self, name: str, **kwargs):
		super().__init__(**kwargs)
		self._name = name
		self._online = False
		self._conversations: Dict[str, List[Dict[str, str]]] = {}
		self._maxHistoryLength = self.ConfigManager.getAliceConfigByName('llmMaxHistoryLength') or 10

	@property
	def name(self) -> str:
		return self._name

	@property
	def online(self) -> bool:
		return self._online

	@abstractmethod
	def getResponse(self, session: DialogSession, text: str) -> Optional[str]:
		"""
		Get a response from the LLM for the given text
		:param session: the dialog session
		:param text: the text to get a response for
		:return: the LLM response or None if an error occurred
		"""
		pass

	def getConversationHistory(self, session: DialogSession) -> List[Dict[str, str]]:
		"""
		Get the conversation history for the given session
		:param session: the dialog session
		:return: the conversation history
		"""
		deviceUid = session.deviceUid
		if deviceUid not in self._conversations:
			self._conversations[deviceUid] = []
		return self._conversations[deviceUid]

	def addToHistory(self, session: DialogSession, role: str, content: str) -> None:
		"""
		Add a message to the conversation history
		:param session: the dialog session
		:param role: the role of the message (user or assistant)
		:param content: the content of the message
		"""
		history = self.getConversationHistory(session)
		history.append({"role": role, "content": content})
		
		# Trim history if it exceeds the maximum length
		if len(history) > self._maxHistoryLength * 2:  # *2 because each exchange has 2 messages
			self._conversations[session.deviceUid] = history[-self._maxHistoryLength * 2:]

	def clearHistory(self, deviceUid: str) -> None:
		"""
		Clear the conversation history for the given device
		:param deviceUid: the device UID
		"""
		self._conversations.pop(deviceUid, None)