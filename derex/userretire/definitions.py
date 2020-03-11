"""Common definitions across derex.userretire
"""
from pathlib import PosixPath

from derex.runner.project import Project


def config_yaml_location(project: Project,) -> PosixPath:
    return project.private_filepath("userretire-config.yaml")
