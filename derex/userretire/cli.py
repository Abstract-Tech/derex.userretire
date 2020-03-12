import json
import os
from tempfile import mkstemp

import click
from derex.runner.cli import ensure_project
from derex.runner.project import DebugProject
from derex.runner.utils import abspath_from_egg
from jinja2 import Template

from .definitions import config_yaml_location
from .port_me_to_derexrunner import exit_cm


@click.command("userretire-setup")
@click.pass_obj
@ensure_project
def userretire_setup(project):
    """Setup user retire functionality
    """
    with exit_cm():
        setup_states(project)
        setup_users(project)


def setup_users(project):
    """Create OAUth users to be used by the user retire script
    and writes the config required by the retire users script.
    """
    from derex.runner.compose_utils import run_compose

    user_name = "RETIREMENT_SERVICE_USER"
    app_name = "RETIREMENT_SERVICE_APP"
    fp, result_path = mkstemp(".json", "derex-userretire-")
    args = [
        "run",
        "--rm",
        "-v",
        f"{result_path}:/result",
        "lms",
        "sh",
        "-c",
        PRINT_CLIENT_ID_AND_SECRET_COMMAND.format(**locals()),
    ]

    try:
        run_compose(args, project=DebugProject())
    finally:
        os.close(fp)
        result_json = open(result_path).read()
        os.unlink(result_path)
    result = json.loads(result_json)

    template_path = abspath_from_egg(
        "derex.userretire", "derex/userretire/config.yaml.j2"
    )

    tmpl = Template(template_path.read_text())
    text = tmpl.render(**dict(result, project=project))
    config_yaml_location(project).write_text(text)


def setup_states(project):
    """Invoke populate_retirement_states to populate database states.
    """
    from derex.runner.compose_utils import run_compose

    args = [
        "run",
        "--rm",
        "lms",
        "sh",
        "-c",
        "./manage.py lms populate_retirement_states",
    ]
    run_compose(args, project=DebugProject())


PRINT_CLIENT_ID_AND_SECRET_COMMAND = r"""
cat > /script.py <<'EOF'
from django.contrib.auth.models import User;
from oauth2_provider.models import get_application_model;
from student.management.commands.manage_user import Command as manage_user
from openedx.core.djangoapps.oauth_dispatch.management.commands.create_dot_application import Command as create_dot_application


Application = get_application_model();
app_name = "{app_name}";
user_name = "{user_name}";
manage_user().run_from_argv(["manage.py", "manage_user", user_name, user_name + "@example.com", "--staff", "--superuser"])
create_dot_application().run_from_argv(["manage.py", "create_dot_application", app_name, user_name])
app = Application.objects.get(name=app_name, user=User.objects.get(username=user_name));
print("{{\"client_id\": \"" + app.client_id + "\",\n\"client_secret\": \"" + app.client_secret + "\"}}\n")
EOF
echo "exec(open('/script.py').read())" | ./manage.py lms shell > /result
"""
