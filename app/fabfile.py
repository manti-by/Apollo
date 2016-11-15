from fabric.api import task, prefix
from fabric.state import env
from fabric.operations import run, sudo, put
from fabric.contrib.files import exists
from fabric.context_managers import cd, settings
from contextlib import contextmanager


def set_defaults():
    if 'app_name' not in env.keys():
        env.app_name = 'traugott'
    if 'app_path' not in env.keys():
        env.app_path = '/home/%s/www/%s/src/app' % (env.user, env.app_name)
    if 'root_path' not in env.keys():
        env.root_path = '/home/%s/www/%s/src' % (env.user, env.app_name)


@contextmanager
def virtualenv():
    with prefix('source %s/../venv/bin/activate' % env.root_path):
        yield


@task
def m53():
    env.hosts = ['vagrant@127.0.0.1:2222']
    env.target = 'vagrant'
    env.user = 'vagrant'
    env.passwords = {'vagrant@127.0.0.1:2222': 'vagrant'}

    set_defaults()


@task
def rpi():
    env.hosts = ['pi@192.168.0.112:22']
    env.target = 'rpi'
    env.user = 'pi'
    env.passwords = {'pi@192.168.0.112:22': env.password}

    set_defaults()


@task
def provision():
    sudo('apt-get update')
    sudo('apt-get upgrade -y')
    sudo('apt-get install -y git python-pip python-dev libpq-dev')
    if env.target == 'staging':
        sudo('apt-get install -y nginx supervisor postgresql')


@task
def create_db():
    with settings(warn_only=True):
        sudo('psql -c "CREATE DATABASE %s;"' % env.app_name, user='postgres')
        sudo('psql -c "CREATE USER %s WITH PASSWORD \'pa$$word\';"' % env.app_name, user='postgres')
        sudo('psql -c "ALTER ROLE %s SET client_encoding TO \'utf8\';"' % env.app_name, user='postgres')
        sudo('psql -c "ALTER ROLE %s SET default_transaction_isolation TO \'read committed\';"' % env.app_name, user='postgres')
        sudo('psql -c "ALTER ROLE %s SET timezone TO \'UTC\';"' % env.app_name, user='postgres')
        sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s;"' % (env.app_name, env.app_name), user='postgres')


@task(default=True)
def pull(branch='master'):
    if not exists('~/.ssh/deploy'):
        put('../deploy/keys/deploy', '~/.ssh/deploy')
        put('../deploy/confs/github.conf', '~/.ssh/config')
        run('chmod 400 ~/.ssh/deploy')
        run('ssh-keyscan github.com >> ~/.ssh/known_hosts')

        run('mkdir %s' % env.root_path)
        run('git clone git@github.com:manti-by/Apollo.git %s' % env.root_path)

        with cd('../' % env.root_path):
            run('mkdir log')
            run('chmod 777 log/')

    with cd(env.root_path):
        run('git checkout %s' % branch)
        run('git pull origin %s' % branch)


@task
def pip_install():
    if not exists('%s/../venv/' % env.root_path):
        with cd('%s/../' % env.root_path):
            run('virtualenv --no-site-packages --prompt="%s" venv' % env.app_name)
    with virtualenv(), cd(env.app_path):
            run('pip install -r requirements.txt')


@task
def setup():
    with settings(warn_only=True):
        with cd(env.app_path):
            run('cp -n %s/settings/local.py.example %s/settings/local.py' % (env.app_name, env.app_name))

        if env.target == 'staging':
            with cd('/etc/nginx/sites-enabled'):
                sudo('ln -s %s/deploy/confs/nginx.conf %s.conf' % (env.root_path, env.app_name))
            with cd('/etc/supervisor/conf.d'):
                sudo('ln -s %s/deploy/confs/supervisor.conf %s.conf' % (env.root_path, env.app_name))


@task
def migrate():
    with virtualenv(), cd(env.app_path):
        run('python manage.py migrate')


@task
def collect_static():
    with virtualenv(), cd(env.app_path):
        run('python manage.py collectstatic --noinput')


@task
def reload_app():
    if env.target == 'staging':
        sudo('supervisorctl update')
        sudo('supervisorctl restart %s' % env.app_name)


@task
def deploy():
    pull()
    pip_install()
    migrate()
    collect_static()
    reload_app()


@task
def deploy_all():
    provision()
    create_db()
    pull()
    pip_install()
    setup()
    migrate()
    collect_static()
    reload_app()