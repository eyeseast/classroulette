from fabric.api import local, env

env.exclude_requirements = [
    'wsgiref', 'readline', 'ipython',
    'git-remote-helpers',
]

def deploy():
    """
    Push to origin and heroku
    """
    local('git push origin master')
    local('git push heroku master')

def freeze():
    """
    pip freeze > requirements.txt, excluding virtualenv clutter
    """
    reqs = local('pip freeze', capture=True).split('\n')
    reqs = [r for r in reqs if r.split('==')[0] not in env.exclude_requirements]
    reqs = '\n'.join(reqs)

    with open('requirements.txt', 'wb') as f:
        f.write(reqs)

    print reqs