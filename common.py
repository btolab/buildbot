from buildbot.steps.shell import SetPropertyFromCommand
from buildbot.process.properties import Interpolate

from cfgbb.slaves import slaves, get_slaves, names

environment = {
	'PATH': '/usr/lib64/ccache:/usr/lib/ccache/bin:/opt/osxcross/target/bin:/opt/mxe/usr/bin:/usr/local/bin:/usr/bin:/usr/sbin:/bin',
	'MACOSX_DEPLOYMENT_TARGET': '10.7',
	'OSXCROSS_MP_INC': '1',
	'MINGW32': '/opt/mxe/usr',
	'MINGW64': '/opt/mxe/usr',
	'BUILDROOT': Interpolate('%(prop:builddir)s'),
}

repos = {
	'mame': {
		'url': 'https://github.com/mamedev/mame.git',
		'branch': 'master',
		'builders': {
			'windows': names(get_slaves(mingw64=True))
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always | sed 's/^mame//'", property='gitversion', haltOnFailure=True),
		'environment': environment,
		'scheduler': ['trigger'],
	},
	'attractmode': {
		'url': 'https://github.com/mickelson/attract.git',
		'branch': 'master',
		'builders': {
			'windows': names(get_slaves(mingw32=True,mingw64=True)),
			'osx': names(get_slaves(osxcross=True)),
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always | sed 's/-[^-]\\{8\\}$//'", property='gitversion', haltOnFailure=True),
		'environment': environment,
		'scheduler': ['trigger'],
	},
	'hypseus': {
		'url': 'https://github.com/btolab/hypseus.git',
		'branch': 'master',
		'builders': {
			'windows': names(get_slaves(mingw64=True))
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always", property='gitversion', haltOnFailure=True),
		'environment': environment,
		'scheduler': ['trigger'],
	},
}

