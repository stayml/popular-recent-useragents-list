import os, sys, time, random, logging, json

try:
	import requests
except ImportError as e:
	sys.exit("Error while importing modules. Please install the modules in requirements.txt")

class UAME:
	def __init__(self, n, device = None, balance = None):
		self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		self.file = os.path.join(self.location, 'uame.json')
		try:
			last_mod_time = os.path.getmtime(self.file)
			if last_mod_time <= (time.time() - 2592000): # 30 days
				logging.warn('UAME last updated over 30 days ago. Please update by calling UAME.update()')
			with open(self.file, 'r') as f:
				self.data = json.loads(f.read())
		except FileNotFoundError:
			sys.exit("source file not found - check installation")
		except Exception as e:
			sys.exit(f"error: {e}")

		self.list = []
		self.device = device
		self.balance = balance

		if len(self.device) == 0:
			logging.warn('devices not specified, so default (desktop, mobile, tablet) are provided')
			self.device = ['desktop', 'mobile', 'tablet']

		if self.balance == None:
			self.balance = [1 / len(self.device) for _ in self.device]
		else:
			if not sum(self.balance) == 1:
				logging.warn('balance of devices does not sum to 1, so have been reset to default')
				self.balance = [1 / len(self.device) for _ in self.device]

		try:
			for choice in random.choices(population=self.device, weights=balance, k=n):
				self.list.append(random.choice(self.data['device'][choice]))
		except KeyError as e:
			sys.exit(e)

	def ualist(self):
		return self.list

	def update(self):
		try:
			r = requests.get('https://useragents.me/uame.json')
			r.raise_for_status()
			with open(self.file, 'w') as f:
				f.write(r.json())
		except requests.exceptions.RequestException as e:
			logging.warn(f"could not update due to {e}")


