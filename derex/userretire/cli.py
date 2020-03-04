import click
from derex.runner.cli import ensure_project
from derex.runner.project import DebugProject
from .port_me_to_derexrunner import exit_cm


@click.command("userretire-setup")
@click.pass_obj
@ensure_project
def userretire_setup(project):
    with exit_cm():
        setup_states(project)
        setup_users(project)


def setup_users(project):
    """Create OAUth users to be used by the user retire script
    """
    from derex.runner.compose_utils import run_compose

    user_name = "retirement_user3"
    app_name = "retirement_app3"
    args = [
        "run",
        "--rm",
        "lms",
        "sh",
        "-c",
        f"echo Creating user;"
        f"./manage.py lms manage_user {user_name} {user_name}@example.com --staff --superuser;"
        f"echo Creating dot application;"
        f"./manage.py lms create_dot_application {app_name} {user_name}"
    ]
    run_compose(args, project=DebugProject())



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

PRINT_CLIENT_ID_AND_SECRET_COMMAND = """
echo 'from django.contrib.auth.models import User;
from oauth2_provider.models import get_application_model;
Application = get_application_model();
appname = "{appname}";
username = "{username}";
app = Application.objects.get(name=appname, user=User.objects.get(username=username));
print("client_id=\"" + app.client_id + "\"\nclient_secret=\"" + app.client_secret + "\"\n")'| ./manage.py lms shell 2> /dev/null
"""
