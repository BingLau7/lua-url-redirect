# -*- coding: utf-8 -*-

from fabric.api import local, env, run, put, cd
from fabric.contrib.files import exists

env.roledefs = {
    'ol': {
        'hosts': [
            'root@10.10.0.240',
            'root@10.11.172.102'
        ]
    },
    't1': {
        'hosts': [
            'root@10.10.126.140',
        ]
    },
}

nginx_pid = '/opt/openresty/nginx/logs/nginx.pid'


def docker_build():
    local('cd docker && docker build -t m_openresty . && cd ..')


# 执行docker run
def docker_run():
    local('docker run --name url-r --rm -p 80:80 -v $PWD/conf.d:/opt/openresty/nginx/conf/conf.d -v $PWD/lua:/opt/openresty/nginx/lua m_openresty /opt/openresty/bin/openresty -g "daemon off;"')
    # local('docker run --name url-r -it --rm -p 10800:80 -v $PWD/conf.d:/opt/openresty/nginx/conf/conf.d -v $PWD/lua:/opt/openresty/nginx/lua m_openresty /bin/bash')


def add_lib(lib_name):
    put('docker/%s' % lib_name, '/opt/openresty/lualib')


def backup():
    with(cd('/opt/openresty/nginx')):
        if exists('lua_bak') and exists('lua'):
            run('rm -rf lua_bak')
            run('cp -r lua lua_bak')
    with(cd('/opt/openresty/nginx/conf/')):
        if exists('sites-enabled_bak') and exists('sites-enabled'):
            run('rm -rf sites-enabled_bak')
            run('cp -r sites-enabled sites-enabled_bak')


def deploy():
    backup()

    role = env['effective_roles'][0]
    nginx_conf = 'conf.d/redirect.conf'
    if role == 't1':
        nginx_conf = 'conf.d/redirect-test.conf'
    put(nginx_conf, '/opt/openresty/nginx/conf/sites-enabled')
    put('lua', '/opt/openresty/nginx')


def rollback():
    with(cd('/opt/openresty/nginx')):
        run('rm -rf lua')
        run('cp -r lua_bak lua')
    with(cd('/opt/openresty/nginx/conf/')):
        run('rm -rf sites-enabled')
        run('cp -r sites-enabled_bak sites-enabled')
    reload_nginx()


def reload_nginx():
    if exists(nginx_pid):
        run('/opt/openresty/bin/openresty -s reload')
    else:
        run('/opt/openresty/bin/openresty')


def tail_file(file_name):
    run('tail -f %s' % file_name)
