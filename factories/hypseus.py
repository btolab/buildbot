from buildbot.plugins import steps, util

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
	if 'gitversion' in cfg:
		bf.addStep(cfg['gitversion'])
	if buildname == "windows":
		bf.addStep(
			steps.Compile(
				name="cmake",
				command=["cmake", "-DCMAKE_TOOLCHAIN_FILE=/opt/mxe/usr/x86_64-w64-mingw32.static/share/cmake/mxe-conf.cmake", "-DBUILDBOT=ON", "src"],
				description="create makefiles",
				haltOnFailure=True
			)
		)
		bf.addStep(
			steps.Compile(
				command=['make'],
				haltOnFailure=True
			)
		)
		bf.addStep(
			steps.FileUpload(
				slavesrc="hypseus.zip",
				masterdest=util.Interpolate("~/sites/com.btolab/build/public/project/hypseus/archive/hypseus-mingw-gcc-x64-%(prop:gitversion)s.zip"),
				url="/project/hypseus",
				description="upload archive",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
		bf.addStep(
			steps.FileUpload(
				slavesrc="hypseus.md5",
				masterdest=util.Interpolate("~/sites/com.btolab/build/public/project/hypseus/archive/hypseus-mingw-gcc-x64-%(prop:gitversion)s.md5"),
				url="/project/hypseus",
				description="upload checksum",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	return bf
