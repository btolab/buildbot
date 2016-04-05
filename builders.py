import textwrap
import itertools

from buildbot.config import BuilderConfig

from cfgbb.common import repos, environment
from cfgbb.slaves import lock
from cfgbb import factories

builders = []

for rname, rcfg in repos.items():
	for bn, slns in rcfg['builders'].items():
		f = getattr(factories, rname)(rcfg, bn)
		builders.append(
			BuilderConfig(
				name=rname+'-'+bn,
				slavenames=slns,
				locks=[lock.access('counting')],
				env=rcfg['environment'],
				factory=f
			)
		)
