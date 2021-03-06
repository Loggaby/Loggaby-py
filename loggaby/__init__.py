from time import localtime, strftime
from re import match

from loggaby.transports.TerminalTransport import TerminalTransport
from loggaby.transports.Transport import Transport

class Loggaby:
	def __init__(self, debug=True, levels=[], transports=[TerminalTransport()]):
		self.debug = debug
		self.levels = levels
		self.transports = transports

		levels = [
			{
				'color': 'cyan',
				'name': 'Log'
			},
			{
				'color': 'green',
				'name': 'Debug',
				'debug': True
			},
			{
				'color': 'yellow',
				'name': 'Warn'
			},
			{
				'color': 'red',
				'name': 'Error'
			},
			{
				'color': 'red',
				'name': 'Fatal',
				'fatal': True
			},
			*self.levels
		]

		for level in levels:
			_levelfunc = self.create_level(level)
			if level.get('call'): funcname = level.get('call')
			else: funcname = self.make_valid(level['name'].lower())
			setattr(self, funcname, _levelfunc)

	def create_level(self, level):
		def _level(*args, **kwargs):
			if match(r'#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$', level.get('color')) is not None: 
				i = int(level.get('color')[1:], 16)
				r = (i >> 16) & 255
				g = (i >> 8) & 255
				b = i & 255;
				color = self.rgb(r, g, b)
			else:
				color = '{%s}' % (level.get('color'))
			attribs = {
				'reset': '\x1b[0m',
				'bold': '\x1b[1m',
				'dim': '\x1b[2m',
				'italic': '\x1b[3m',
				'underline': '\x1b[4m',
				'bold-off': '\x1b[22m',
				'underline-off': '\x1b[24m',
				'black': '\x1b[30m',
				'red': '\x1b[31m',
				'green': '\x1b[32m',
				'yellow': '\x1b[33m',
				'blue': '\x1b[34m',
				'magenta': '\x1b[35m',
				'cyan': '\x1b[36m',
				'white': '\x1b[37m',
				'red-bg': '\x1b[41m',
				'green-bg': '\x1b[42m',
				'yellow-bg': '\x1b[43m',
				'blue-bg': '\x1b[44m',
				'magenta-bg': '\x1b[45m',
				'cyan-bg': '\x1b[46m',
				'white-bg': '\x1b[49m',
				'bright-black': '\x1b[90m',
				'gray': '\x1b[90m',
				'grey': '\x1b[90m',
				'bright-red': '\x1b[91m',
				'bright-green': '\x1b[92m',
				'bright-yellow': '\x1b[93m',
				'bright-blue': '\x1b[94m',
				'bright-magenta': '\x1b[95m',
				'bright-cyan': '\x1b[96m'
			}
			for t in self.transports:
				if level.get('fatal') == True: formatted = ('{gray}%s {bold}{underline}{%s}%s{underline-off} {white}> {underline}%s{reset}' % (self.time(), level['color'], level['name'], args[0])).format(**attribs)
				else: formatted = ('{gray}%s %s%s {reset}> %s' % (self.time(), color, level['name'], args[0])).format(**attribs)
				t.transmit(formatted, *args[1::], **kwargs)
		return _level

	def time(self):
		return strftime('%I:%M:%S %p', localtime())

	def rgb(self, r, g, b):
		return '\x1b[38;2;%s;%s;%am' % (r, g, b)

	def make_valid(self, name):
		return ''.join(name.split())