from pathlib import Path
from typing import Dict, List, Optional, Union

from derex import runner  # type: ignore
from derex.runner.project import Project
from derex.runner.utils import abspath_from_egg
from jinja2 import Template

from .definitions import config_yaml_location


class UserRetireService:
    @staticmethod
    @runner.hookimpl
    def local_compose_options(
        project: Project,
    ) -> Optional[Dict[str, Union[str, List[str]]]]:
        if "userretire" not in project.config.get("plugins", {}):
            return None
        local_compose_path = generate_local_docker_compose(project)
        options = ["-f", str(local_compose_path)]
        return {
            "options": options,
            "name": "userretire",
            "priority": ">base",
            "variant": "openedx",
        }


def generate_local_docker_compose(project: Project) -> Path:
    """This function is called every time ddc-project is run.
    It assembles a docker-compose file from the given configuration.
    It should execute as fast as possible.
    """
    dc_path = abspath_from_egg(
        "derex.userretire", "derex/userretire/docker-compose.yml.j2"
    )
    tmpl = Template(dc_path.read_text())
    text = tmpl.render(project=project, yaml_location=config_yaml_location(project))
    local_compose_path = project.private_filepath("docker-compose-userretire.yml")
    local_compose_path.write_text(text)
    return local_compose_path
