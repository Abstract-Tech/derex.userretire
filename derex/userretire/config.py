from typing import Dict, List, Optional, Union

from derex import runner  # type: ignore
from derex.runner.project import Project


class UserRetireService:
    @staticmethod
    @runner.hookimpl
    def local_compose_options(
        project: Project,
    ) -> Optional[Dict[str, Union[str, List[str]]]]:
        return None
