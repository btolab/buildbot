from buildbot.plugins import steps, util
from buildbot.steps.shell import SetPropertyFromCommand

def build(cfg, buildname):
	bf = util.BuildFactory()
	bf.addStep(
		steps.Git(
		repourl=cfg['url'],
			branch=cfg['branch'],
			mode='full',
			logEnviron=False
		)
	)
	bf.addStep(
		SetPropertyFromCommand(
			command="git describe --always | sed 's/-[^-]\\{8\\}$//'",
			property='gitversion', haltOnFailure=True
		)
	)
	if buildname == "osx":
		bf.addStep(
			steps.Compile(
				command=['bash', '-c', 'source /opt/osxcross/buildbot-env; util/' + buildname[:3] + '/create-pkg.sh'],
				haltOnFailure=True
			)
		)
		bf.addStep(
			steps.MultipleFileUpload(
				slavesrcs=[
					util.Interpolate("attract-%(prop:gitversion)s.dmg"),
				],
				masterdest="~/sites/com.btolab/build/public/project/attractmode/osx",
				url="/project/attractmode/osx",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	elif buildname == "windows":
		bf.addStep(
			steps.Compile(
				command=['bash', '-c', 'util/' + buildname[:3] + '/create-pkg.sh'],
				haltOnFailure=True
			)
		)
		bf.addStep(
			steps.MultipleFileUpload(
				slavesrcs=[
					util.Interpolate('attract-%(prop:gitversion)s-win32.zip'),
					util.Interpolate('attract-%(prop:gitversion)s-win64.zip'),
				],
				masterdest="~/sites/com.btolab/build/public/project/attractmode/windows",
				url="/project/attractmode/windows",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	return bf

