from derex import runner  # type: ignore
from derex.runner.project import Project
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

class UserRetireService:
    @staticmethod
    @runner.hookimpl
    def local_compose_options(project: Project) -> Optional[Dict[str, Union[str, List[str]]]]:
        return None
