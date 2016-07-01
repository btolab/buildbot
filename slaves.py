import os
from buildbot.buildslave import BuildSlave
from buildbot import locks

class BotSlaveBase(object):
	# true if this box should use a 'simple' factory
	# meaning no virtualenv (windows)
	use_simple = False
	max_count = 1
	databases = {}
	mingw64 = False
	mingw32 = False
	vs2015 = False
	osxcross = False
	fastbuild = False
	android = False

	def extract_attrs(self, name, **kwargs):
		self.slavename = name
		remaining = {}
		for k in kwargs:
			if hasattr(self, k):
				setattr(self, k, kwargs[k])
			else:
				remaining[k] = kwargs[k]
		return remaining

	def get_pass(self, name):
		path = os.path.join(os.path.dirname(__file__), "%s.pass" % name)
		pw = open(path).read().strip()
		return pw

class BotSlave(BotSlaveBase, BuildSlave):
	def __init__(self, name, **kwargs):
		password = self.get_pass(name)
		kwargs = self.extract_attrs(name, **kwargs)
		BuildSlave.__init__(self, name, password, **kwargs)

slaves = [
	BotSlave('deathstar',
		properties = {
			'os': 'fedora',
			'osversion': '22',
		},
		max_count=1,
		osxcross=True
	),
	BotSlave('archct',
		properties = {
			'os': 'archlinux',
		},
		max_count=1,
		mingw32=True, mingw64=True,
		android=True,
	),
	BotSlave('h0tw10vm',
		properties = {
			'os': 'windows10',
		},
		max_count=1,
		vs2015=True,
		fastbuild=True,
	),
]

def get_locks():
	rv = {}
	for sl in slaves:
		rv[sl.slavename] = getattr(sl, 'max_count')
	return rv

db_lock = locks.MasterLock("database")
lock = locks.SlaveLock(
	"slave_builds",
	maxCount = 1,
	maxCountForSlave = get_locks()
)

def get_slaves(db=None, *args, **kwargs):
	rv = {}
	for arg in args:
		rv.update(arg)
	for sl in slaves:
		if db and db not in sl.databases:
			continue
		for k in kwargs:
			if getattr(sl, k) != kwargs[k]:
				break
			else:
				rv[sl.slavename] = sl
	return rv

def names(slavedict):
	return slavedict.keys()
