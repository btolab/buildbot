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
			command="git describe --always | sed 's/^mame//'",
			property='gitversion', haltOnFailure=True
		)
	)
	bf.addStep(
		steps.ShellCommand(
			name="fetch support",
			command=["git", "clone", "--depth=1", "--branch=mame", "https://github.com/btolab/buildsupport.git", ".buildsupport"],
			description="download latest build support tool",
			haltOnFailure=True, flunkOnFailure=False
		)
	)
	bf.addStep(
		steps.Compile(
			command=['bash', '-c', '.buildsupport/build.sh $0', buildname],
			haltOnFailure=True
		)
	)
	if buildname.startswith("android"):
		bf.addStep(
			steps.FileUpload(
				slavesrc="android-project/app/build/outputs/apk/app-release-unsigned.apk",
				masterdest=util.Interpolate("~/sites/com.btolab/build/public/project/mame/archive/%(prop:buildername)s-%(prop:gitversion)s.apk"),
				url="/project/mame",
				description="upload apk",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	else:
		bf.addStep(
			steps.ShellCommand(
				name="package",
				command=['bash', '-c', '.buildsupport/release.sh $0', buildname],
				haltOnFailure=True, flunkOnFailure=False
			)
		)
	if buildname == "mingw64":
		bf.addStep(
			steps.MultipleFileUpload(
				slavesrcs=[
					util.Interpolate("mame-mingw-gcc-x64-%(prop:gitversion)s.md5"),
					util.Interpolate("mame-mingw-gcc-x64-%(prop:gitversion)s.exe"),
				],
				masterdest="~/sites/com.btolab/build/public/project/mame/archive",
				url="/project/mame",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	if buildname == "vs2015":
		bf.addStep(
			steps.MultipleFileUpload(
				slavesrcs=[
					util.Interpolate("mame-vs2015-x64-%(prop:gitversion)s.md5"),
					util.Interpolate("mame-vs2015-x64-%(prop:gitversion)s.exe"),
				],
				masterdest="~/sites/com.btolab/build/public/project/mame/archive",
				url="/project/mame",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	return bf
