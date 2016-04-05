from buildbot.process.factory import BuildFactory
from buildbot.steps.shell import Compile, ShellCommand
from buildbot.steps.source.git import Git

def attractmode(cfg):
	f = BuildFactory()
	f.addStep(
		Git(
		repourl=cfg['url'],
			branch=cfg['branch'],
			mode='full',
			method='clean',
			logEnviron=False
		)
	)
	if 'gitversion' in cfg:
		f.addStep(cfg['gitversion'])
	f.addStep(
		ShellCommand(
			name="create package",
			command=['bash', '-c', 'util/win/create-pkg.sh'],
			description='make and package',
			haltOnFailure=True
		)
	)
	return f

def uxme(cfg):
	f = BuildFactory()
	f.addStep(
		Git(
		repourl=cfg['url'],
			branch=cfg['branch'],
			mode='full',
			method='clean',
			logEnviron=False
		)
	)
	if 'gitversion' in cfg:
		f.addStep(cfg['gitversion'])
	f.addStep(
		ShellCommand(
			name="create package",
			command=['bash', '-c', 'util/win/create-pkg.sh'],
			description='make and package',
			haltOnFailure=True
		)
	)
	return f

def mame(cfg):
	f = BuildFactory()
	f.addStep(
		Git(
		repourl=cfg['url'],
			branch=cfg['branch'],
			mode='full',
			method='clean',
			logEnviron=False
		)
	)
	if 'gitversion' in cfg:
		f.addStep(cfg['gitversion'])
	f.addStep(
		ShellCommand(
			name="create package",
			command=['bash', '-c', 'util/win/create-pkg.sh'],
			description='make and package',
			haltOnFailure=True
		)
	)
	return f

