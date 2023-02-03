

class Permissions:
    """Permission levels for the users & commands

    :ivar Any: Permissions for any user (including users, that doesn't have no one permission)
    :ivar User: Permission for User level
    :ivar AdvUser: Permission for Advanced User level
    :ivar Trusted: Permission for trusted users. It recommended to use, if command may be used as spam or DoS
    :ivar Admin: Permission for Admin level. It recommended to use, when command doing administrative actions
    :ivar Danger: Permission for Danger level. It recommended to use, when command may harm to framework, system or use danger functions, commands, etc. as example - :func:`eval()`, :func:`exec()`
    :ivar Owner: Permission for Owner level. It recommended to use, if command is changing some framework options
    """

    Any          = -1
    User         = 0
    AdvUser      = 1
    Trusted      = 2
    Admin        = 3
    Danger       = 4
    Owner        = 5
