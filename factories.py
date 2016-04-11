from buildbot.plugins import steps, util

#class FileUploadWithUrls(FileUpload):
#	renderables = ["auxUrls"]
#
#	def __init__(self, auxUrls=None, **kwargs):
#		self.auxUrls = auxUrls
#		FileUpload.__init__(self, **kwargs)
#		self.addFactoryArguments(auxUrls=auxUrls)
#
#	def start(self):
#		if self.auxUrls is not None:
#			for url in self.auxUrls:
#				self.addURL(os.path.basename(url), url)
#		FileUpload.start(self)

def attractmode(cfg, buildname):
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
				masterdest="~/sites/com.zaplabs/build/public/project/attractmode/osx",
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
				masterdest="~/sites/com.zaplabs/build/public/project/attractmode/windows",
				url="/project/attractmode/windows",
				haltOnFailure=False, flunkOnFailure=False, mode=0644
			)
		)
	return bf

def uxme(cfg, buildname):
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
	bf.addStep(
		steps.ShellCommand(
			name="fetch support",
			command=["git", "clone", "--depth=1", "--branch=mame", "https://github.com/zaplabs/buildsupport.git", ".buildsupport"],
			description="download latest build support tool",
			haltOnFailure=True
		)
	)
	bf.addStep(
		steps.Compile(
			name="create package",
			command=['bash', '-c', 'util/win/create-pkg.sh'],
			description='make and package',
			haltOnFailure=True
		)
	)
	return bf

def mame(cfg, buildname):
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
	bf.addStep(
		steps.ShellCommand(
			name="fetch support",
			command=["git", "clone", "--depth=1", "--branch=mame", "https://github.com/zaplabs/buildsupport.git", ".buildsupport"],
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
				util.Interpolate("mame-mingw-gcc-x32-%(prop:gitversion)s.md5"),
				util.Interpolate("mame-mingw-gcc-x32-%(prop:gitversion)s.exe"),
			],
			masterdest="~/sites/com.zaplabs/build/public/project/mame",
			url="/project/mame",
			haltOnFailure=False, flunkOnFailure=False, mode=0644
		)
	)
	return bf
