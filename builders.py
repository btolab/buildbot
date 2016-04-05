import textwrap
import itertools

from buildbot.config import BuilderConfig
from buildbot.process.properties import Interpolate
from buildbot.steps.source.git import Git
from buildbot.steps.shell import Compile, Test, ShellCommand
from buildbot.steps.slave import RemoveDirectory, MakeDirectory
from buildbot.steps.transfer import FileDownload, FileUpload

from cfgbb.common import repos, environment
from cfgbb.slaves import slaves, get_slaves, names, lock
from cfgbb import factories

builders = []

class FileUploadWithUrls(FileUpload):
	renderables = ["auxUrls"]

	def __init__(self, auxUrls=None, **kwargs):
		self.auxUrls = auxUrls
		FileUpload.__init__(self, **kwargs)
		self.addFactoryArguments(auxUrls=auxUrls)

	def start(self):
		if self.auxUrls is not None:
			for url in self.auxUrls:
				self.addURL(os.path.basename(url), url)
		FileUpload.start(self)

for rname, rcfg in repos.items():
	for bn in rcfg['builders']:
		f = getattr(factories, rname)(rcfg)
		builders.append(
			BuilderConfig(
				name=rname+'-'+bn,
				slavenames=rcfg['slaves'],
				locks=[lock.access('counting')],
				env=rcfg['environment'],
				factory=f
			)
		)
