import textwrap
import itertools
import importlib

from buildbot.config import BuilderConfig

from cfgbb.common import repos, environment
from cfgbb.slaves import lock

builders = []
factories = {}

for rname, rcfg in repos.items():
	if not factories.has_key(rname):
		factories[rname] = importlib.import_module('cfgbb.factories.'+rname)
	for bn, slns in rcfg['builders'].items():
		f = getattr(factories[rname], 'build')(rcfg, bn)
		builders.append(
			BuilderConfig(
				name=rname+'-'+bn,
				slavenames=slns,
				locks=[lock.access('counting')],
				tags=[rname,bn],
				env=rcfg['environment'],
				factory=f
			)
		)
