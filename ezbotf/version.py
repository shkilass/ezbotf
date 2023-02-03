"""
Defines VersionLabel with labels of version and version information
"""


class VersionLabel:
    InDevelopment  = '[indev]'
    Unstable       = '[unstable]'

ezbotf_labels   = [VersionLabel.InDevelopment]

ezbotf_version_string = '1.0.0.dev2'
ezbotf_version_string_full = ' '.join([ezbotf_version_string] + ezbotf_labels)
