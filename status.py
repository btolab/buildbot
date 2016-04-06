status = []

from buildbot.status import html
from buildbot.status import words
from buildbot.status.web.auth import BasicAuth
from buildbot.status.web.authz import Authz

users = [
	('dev', 'bbot!')
]

authz = Authz(
	auth=BasicAuth(users),
	forceBuild='auth',
	forceAllBuilds='auth',
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
