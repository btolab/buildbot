from buildbot.plugins import changes

from cfgbb.common import repos

change_source = []

for rname, rcfg in repos.items():
	change_source.append(
		changes.GitPoller(
			rcfg['url'],
			workdir='gitpoller-'+rname,
			branch=rcfg['branch'],
			project=rname,
			pollinterval=5*60,
			pollAtLaunch=True
		)
	)
