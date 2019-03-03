import random

from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/fbidu/superlists.git"

def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f"git reset --hard {current_commit}")

def _update_pipenv():
    if not exists(f"/home/{env.user}/miniconda3/bin/pipenv"):
        run(f"pip install --user pipenv")

    run("pipenv install")

def _update_dotenv():
    pass

def _update_static_files():
    run("pipenv python run manage.py collectstatic --noinput")

def _update_database():
    run("pipenv python manage.py migrate --noinput")

def deploy():
    site_folder = f"/home/{env.user}/django-apps/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_pipenv()
        _update_dotenv()
        _update_static_files()
        _update_database()