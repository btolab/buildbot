from buildbot.steps.shell import SetPropertyFromCommand
from buildbot.process.properties import Interpolate

from cfgbb.slaves import slaves, get_slaves, names

environment = {
	'PATH': '/usr/lib64/ccache/bin:/usr/lib/ccache/bin:/opt/osxcross/target/bin:/opt/mxe/usr/bin:/usr/local/bin:/usr/bin:/usr/sbin:/bin',
	'MACOSX_DEPLOYMENT_TARGET': '10.7',
	'OSXCROSS_MP_INC': '1',
	'MINGW32': '/opt/mxe/usr',
	'MINGW64': '/opt/mxe/usr',
	'BUILDROOT': Interpolate('%(prop:builddir)s'),
}

envandroid = {
	'PATH': '/usr/lib64/ccache:/usr/lib/ccache/bin:/usr/local/bin:/usr/bin:/usr/sbin:/bin',
	'ANDROID_HOME': '/opt/android-sdk-linux',
	'ANDROID_NDK': '/opt/android-ndk',
	'ANDROID_NDK_ROOT': '/opt/android-ndk',
	'ANDROID_NDK_LLVM': '/opt/android-ndk/toolchains/llvm/prebuilt/linux-x86_64',
	'ANDROID_NDK_ARM': '/opt/android-ndk/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64',
	'ANDROID_NDK_ARM64': '/opt/android-ndk/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64',
	'ANDROID_NDK_MIPS': '/opt/android-ndk/toolchains/mipsel-linux-android-4.9/prebuilt/linux-x86_64',
	'ANDROID_NDK_MIPS64': '/opt/android-ndk/toolchains/mips64el-linux-android-4.9/prebuilt/linux-x86_64',
	'ANDROID_NDK_X86': '/opt/android-ndk/toolchains/x86-4.9/prebuilt/linux-x86_64',
	'ANDROID_NDK_X64': '/opt/android-ndk/toolchains/x86_64-4.9/prebuilt/linux-x86_64',
	'BUILDROOT': Interpolate('%(prop:builddir)s'),
}

envwin = {
	'BUILDROOT': Interpolate('%(prop:builddir)s'),
}

repos = {
	'mame': {
		'url': 'https://github.com/mamedev/mame.git',
		'branch': 'master',
		'builders': {
			'mingw64': names(get_slaves(mingw64=True)),
			'vs2015': names(get_slaves(vs2015=True)),
			'android-arm': names(get_slaves(android=True)),
			'android-arm64': names(get_slaves(android=True)),
			'android-mips': names(get_slaves(android=True)),
			'android-mips64': names(get_slaves(android=True)),
			'android-x86': names(get_slaves(android=True)),
			'android-x64': names(get_slaves(android=True)),
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always | sed 's/^mame//'", property='gitversion', haltOnFailure=True),
		'environment': {
			'mingw64': environment,
			'vs2015': envwin,
			'android-arm': envandroid,
			'android-arm64': envandroid,
			'android-mips': envandroid,
			'android-mips64': envandroid,
			'android-x86': envandroid,
			'android-x64': envandroid,
		},
		'scheduler': ['nightly'],
	},
	'hbmame': {
		'url': 'https://github.com/Robbbert/hbmame.git',
		'branch': 'master',
		'builders': {
			'mingw64': names(get_slaves(mingw64=True))
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always | sed 's/^hbmame//'", property='gitversion', haltOnFailure=True),
		'environment': {
			'mingw64': environment,
		},
		'scheduler': ['checkin'],
	},
	'attractmode': {
		'url': 'https://github.com/mickelson/attract.git',
		'branch': 'master',
		'builders': {
			'windows': names(get_slaves(mingw32=True,mingw64=True)),
			'osx': names(get_slaves(osxcross=True)),
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always | sed 's/-[^-]\\{8\\}$//'", property='gitversion', haltOnFailure=True),
		'environment': {
			'windows': environment,
			'osx': environment,
		},
		'scheduler': ['checkin'],
	},
	'hypseus': {
		'url': 'https://github.com/btolab/hypseus.git',
		'branch': 'master',
		'builders': {
			'mingw64': names(get_slaves(mingw64=True))
		},
		'gitversion': SetPropertyFromCommand(command="git describe --always", property='gitversion', haltOnFailure=True),
		'environment': {
			'mingw64': environment,
		},
		'scheduler': ['checkin'],
	},
}

