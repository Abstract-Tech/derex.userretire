"""Common definitions across derex.userretire
"""

def config_yaml_location(project: "derex.runner.project.Project") -> "pathlib.PosixPath":
    return project.private_filepath("userretire-config.yaml")
