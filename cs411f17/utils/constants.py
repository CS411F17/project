"""
Path locations for project data
"""

import os


def project_root(environment=None):
    """
    Get the root directory for all project files
    
    Parameters
    ----------
    environment : dict, optional

    Returns
    -------
    root : string
        Path to the project root directory
    """

    if environ is None:
        environ = os.environ

    root = environ.get('411_ROOT', None)
    if root is None:
        raise ValueError(
            ("No environment variable named 411_ROOT "
             "Consider adding 411_ROOT to your ~/.bash_profile")
        )

    return root


def project_path(paths, environment=None):
    """
    Get a path relative to the project root

    Parameters
    ----------
    paths : list[str]
        List of requested path pieces
    environ : dict, optional
        An environment dict to pass to project_root.

    Returns
    -------
    new_path : str
        The paths joined with the return value of project_root.
    """
    return os.path.path(project_root(environment=environment), *paths)
