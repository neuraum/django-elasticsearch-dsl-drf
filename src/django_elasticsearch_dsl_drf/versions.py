"""
Contains information about the current Elasticsearch version in use,
including (LTE and GTE).
"""

from packaging.version import Version as LooseVersion, InvalidVersion

__title__ = 'django_elasticsearch_dsl_drf.versions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = [
    'get_elasticsearch_version',
    'LOOSE_ELASTICSEARCH_VERSION',
    'LOOSE_ELASTICSEARCH_MINOR_VERSION',
]


def get_elasticsearch_version(default=(2, 0, 0)):
    """Get Elasticsearch version.

    :param default: Default value. Mainly added for building the docs
        when Elasticsearch is not running.
    :type default: tuple
    :return:
    :rtype: list
    """
    try:
        from elasticsearch.dsl import __version__
        return __version__
    except ImportError:
        return default


def _coerce_to_version(value) -> LooseVersion:
    """Coerce tuples/lists/strings into a packaging Version object.

    `packaging.version.Version` expects a string, so we normalize common forms
    used by elasticsearch-dsl (e.g. (8, 11, 0)).
    """
    if isinstance(value, LooseVersion):
        return value

    if isinstance(value, (tuple, list)):
        value = '.'.join(str(v) for v in value)
    else:
        value = str(value)

    try:
        return LooseVersion(value)
    except InvalidVersion:
        # Fallback for unexpected values (e.g. non-PEP440-ish strings)
        return LooseVersion('0')


LOOSE_ELASTICSEARCH_VERSION = _coerce_to_version(get_elasticsearch_version())

# `Version.release` is a tuple like (major, minor, patch, ...)
_release = LOOSE_ELASTICSEARCH_VERSION.release
_major = _release[0] if len(_release) > 0 else 0
_minor = _release[1] if len(_release) > 1 else 0

LOOSE_ELASTICSEARCH_MINOR_VERSION = LooseVersion(f"{_major}.{_minor}")

# Loose versions
LOOSE_VERSIONS = (
    '2.0',
    '2.1',
    '2.2',
    '5.0',
    '5.1',
    '5.2',
    '5.3',
    '5.4',
    '6.0',
    '6.1',
    '6.2',
    '6.3',
    '7.0',
    '7.1',
    '7.2',
    '7.3',
    '7.4',
    '8.0',
    '9.0',
)

for __v in LOOSE_VERSIONS:
    __var_name = 'LOOSE_VERSION_{0}'.format(__v.replace('.', '_'))
    globals()[__var_name] = LooseVersion(__v)
    __all__.append(__var_name)

# Exact versions
EXACT_VERSIONS = LOOSE_VERSIONS[:-1]

for __i, __v in enumerate(EXACT_VERSIONS):
    __l_cur = globals()['LOOSE_VERSION_{0}'
                        ''.format(LOOSE_VERSIONS[__i].replace('.', '_'))]
    __l_nxt = globals()['LOOSE_VERSION_{0}'
                        ''.format(LOOSE_VERSIONS[__i + 1].replace('.', '_'))]
    __var_name = 'ELASTICSEARCH_{0}'.format(__v.replace('.', '_'))
    globals()[__var_name] = (__l_cur <= LOOSE_ELASTICSEARCH_VERSION < __l_nxt)
    __all__.append(__var_name)

# LTE list
LTE_VERSIONS = LOOSE_VERSIONS[:-1]

for __i, __v in enumerate(EXACT_VERSIONS):
    __l_cur = globals()['LOOSE_VERSION_{0}'
                        ''.format(LOOSE_VERSIONS[__i].replace('.', '_'))]
    __var_name = 'ELASTICSEARCH_LTE_{0}'.format(__v.replace('.', '_'))
    globals()[__var_name] = (LOOSE_ELASTICSEARCH_MINOR_VERSION <= __l_cur)
    __all__.append(__var_name)

# GTE list
GTE_VERSIONS = LOOSE_VERSIONS[:-1]

for __i, __v in enumerate(EXACT_VERSIONS):
    __l_cur = globals()['LOOSE_VERSION_{0}'
                        ''.format(LOOSE_VERSIONS[__i].replace('.', '_'))]
    __var_name = 'ELASTICSEARCH_GTE_{0}'.format(__v.replace('.', '_'))
    globals()[__var_name] = (
        LOOSE_ELASTICSEARCH_MINOR_VERSION >= __l_cur
    )
    __all__.append(__var_name)

__all__ = tuple(__all__)

# Clean up
try:
    del __l_cur
    del __l_nxt
    del __var_name
    del __i
    del __v
except NameError:
    pass

del _release
del _major
del _minor
del _coerce_to_version
del InvalidVersion
del LooseVersion
