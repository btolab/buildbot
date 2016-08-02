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
			command="git describe --always | sed 's/^hbmame//'",
			property='gitversion', haltOnFailure=True
		)
	)
	bf.addStep(
		steps.ShellCommand(
			name="fetch support",
			command=["git", "clone", "--depth=1", "--branch=hbmame", "https://github.com/btolab/buildsupport.git", ".buildsupport"],
			description="download latest build support tool",
			haltOnFailure=True
		)
	)
	bf.addStep(
		steps.Compile(
			command=['bash', '-c', '.buildsupport/build.sh'],
			haltOnFailure=True
		)
	)
	bf.addStep(
		steps.ShellCommand(
			name="package",
			command=['bash', '-c', '.buildsupport/release.sh'],
			haltOnFailure=True, flunkOnFailure=True
		)
	)
	bf.addStep(
		steps.MultipleFileUpload(
			slavesrcs=[
				util.Interpolate("hbmame-mingw-gcc-x64-%(prop:gitversion)s.md5"),
				util.Interpolate("hbmame-mingw-gcc-x64-%(prop:gitversion)s.exe"),
			],
			masterdest="~/sites/com.btolab/build/public/project/hbmame/archive",
			url="/project/hbmame",
			haltOnFailure=False, flunkOnFailure=False, mode=0644
		)
	)
	return bf
