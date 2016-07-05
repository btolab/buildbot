from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.timed import Nightly
from buildbot.schedulers.forcesched import ForceScheduler

from buildbot.changes.filter import ChangeFilter

from cfgbb.builders import builders
from cfgbb.common import repos

schedulers = []

for rname, ropts in repos.items():
	rbns = [ rname + '-' + x for x in ropts['builders'].keys() ]
	if 'checkin' in ropts['scheduler']:
		schedulers.append(
			SingleBranchScheduler(
				name=rname+'-checkin',
				change_filter=ChangeFilter(
					project=rname,
					branch=ropts['branch'],
				),
				treeStableTimer=60*60,
				builderNames=rbns
			)
		)
	if 'nightly' in ropts['scheduler']:
		schedulers.append(
			Nightly(
				name=rname + '-nightly',
				builderNames=rbns,
				branch=ropts['branch'],
				hour=3,
				minute=0,
				onlyIfChanged=True,
			)
		)
	schedulers.append(
		ForceScheduler(
			name=rname + '-force',
			builderNames=rbns
		)
	)

