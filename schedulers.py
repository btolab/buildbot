from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.timed import NightlyTriggerable
from buildbot.schedulers.forcesched import ForceScheduler

from buildbot.changes.filter import ChangeFilter

from cfgbb.builders import builders
from cfgbb.common import repos

schedulers = []

for rname, ropts in repos.items():
	rbns = [ rname + '-' + x for x in ropts['builders'].keys() ]
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
	#schedulers.append(
	#	NightlyTriggerable(
	#		name=rname + '-nightly',
	#		builderNames=rbns,
	#		hour=3,
	#		minute=0,
	#	)
	#)
	schedulers.append(
		ForceScheduler(
			name=rname + '-force',
			builderNames=rbns
		)
	)

