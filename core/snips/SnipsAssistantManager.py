import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from core.base.model.Manager import Manager


class SnipsAssistantManager(Manager):

	def __init__(self):
		super().__init__()
		self._assistantPath: Optional[Path] = None


	def onStart(self):
		super().onStart()
		self._assistantPath = Path(self.Commons.rootDir(), f'trained/assistants/assistant_{self.LanguageManager.activeLanguage}/assistant.json')
		self.checkAssistant()


	def checkAssistant(self):
		self.logInfo('Checking assistant')
		if not self._assistantPath.exists():
			self.logInfo('Assistant not found, generating')
			self.train()
		else:
			self.logInfo('Assistant existing')


	def train(self):
		self.logInfo('Training assistant')

		try:
			assistant = self.generateAssistant()
			intents = dict()
			slots = dict()

			for skillPath in Path(self.Commons.rootDir(), 'skills/').glob('*/'):
				if skillPath.is_file() or skillPath.stem.startswith('_'):
					continue

				resource = skillPath / f'dialogTemplate/{self.LanguageManager.activeLanguage}.json'
				if not resource.exists():
					self.logWarning(f'Skill "{skillPath.stem}" is missing dialogTemplate for lang "{self.LanguageManager.activeLanguage}')
					continue

				with resource.open() as fp:
					data = json.load(fp)

				if 'intents' not in data:
					self.logDebug(f'Skill "{skillPath.stem}" has no intent')
					continue

				for intent in data['intents']:
					if intent['name'] in intents:
						self.logWarning(f'Intent "{intent["name"]}" is duplicated')
						continue

					intents[intent['name']] = {
						'id'              : intent['name'],
						'type'            : 'registry',
						'version'         : '0.1.0',
						'language'        : self.LanguageManager.activeLanguage,
						'slots'           : list(),
						'name'            : intent['name'],
						'enabledByDefault': intent['enabledByDefault']
					}

					if not intent['slots']:
						continue

					for slot in intent['slots']:
						if slot['type'] not in slots:
							intentSlot = {
								'name'           : slot['name'],
								'id'             : self.Commons.randomString(9),
								'entityId'       : f'entity_{self.Commons.randomString(11)}',
								'missingQuestion': slot['missingQuestion'],
								'required'       : slot['required']
							}
							slots[slot['type']] = intentSlot
						else:
							intentSlot = {
								'name'           : slot['name'],
								'id'             : self.Commons.randomString(9),
								'entityId'       : slots[slot['type']]['entityId'],
								'missingQuestion': slot['missingQuestion'],
								'required'       : slot['required']
							}

						intents[intent['name']]['slots'].append(intentSlot)

			assistant['intents'] = [intent for intent in intents.values()]
			with self._assistantPath.open('w') as fp:
				fp.write(json.dumps(assistant, ensure_ascii=False, indent=4, sort_keys=True))

			self.broadcast(method='snipsAssistantInstalled', exceptions=[self.name], propagateToSkills=True)
			self.logInfo(f'Assistant trained with {len(intents)} intents with a total of {len(slots)} slots')
		except Exception as e:
			self.broadcast(method='snipsAssistantFailedTraining', exceptions=[self.name], propagateToSkills=True)
			if not self._assistantPath.exists():
				self.logFatal('Assistant failed training and no assistant existing, stopping here, sorry....')


	def generateAssistant(self) -> dict:
		assistant = {
			'id'              : f'proj_{self.Commons.randomString(11)}',
			'name'            : f'ProjectAlice_{self.LanguageManager.activeLanguage}',
			'analyticsEnabled': False,
			'heartbeatEnabled': False,
			'language'        : self.LanguageManager.activeLanguage,

			# Declare as google so snips doesn't try to find the snips-asr service
			'asr'             : {'type': 'google'},

			'platform'        : {'type': 'raspberrypi'},
			'createdAt'       : datetime.utcnow().isoformat() + 'Z',
			'hotword'         : 'hey_snips',
			'version'         : {'nluModel': '0.20.1'},
			'intents'         : list()
		}

		return assistant