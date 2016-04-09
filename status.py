status = []

import os
from buildbot.status import html
from buildbot.status import words
from buildbot.status.web.auth import HTPasswdAprAuth
from buildbot.status.web.authz import Authz

http_auth=HTPasswdAprAuth(os.path.join(os.path.dirname(__file__), ".htpasswd"))

authz = Authz(
    auth=http_auth,
#	view='auth',
	gracefulShutdown='auth',
	forceBuild='auth',
	forceAllBuilds='auth',
	pingBuilder='auth',
	stopBuild='auth',
	stopAllBuilds='auth',
	cancelPendingBuild='auth',
	cancelAllPendingBuilds='auth',
	stopChange='auth',
	cleanShutdown='auth',
	pauseSlave='auth',
	showUsersPage='auth',
)

status.append(html.WebStatus(
	http_port="tcp:8010:interface=127.0.0.1",
	authz=authz,
	order_console_by_time=True,
))

status.append(words.IRC(
	host="irc.servercentral.net",
	nick="h0tbb",
	useColors=True,
	notify_events={
		'exception': 1,
		'successToFailure': 1,
		'failureToSuccess': 1
	},
	channels=['#zaplabs']
))
