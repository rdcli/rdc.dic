from setuptools import setup, find_packages

tolines = lambda c: filter(None, map(lambda s: s.strip(), c.split('\n')))

def read(filename, flt=None):
    with open(filename) as f:
        content = f.read().strip()
        return flt(content) if callable(flt) else content

def requirements_filter(c):
    install_requires = []
    for requirement in tolines(c):
        _pound_pos = requirement.find('#')
        if _pound_pos != -1:
            requirement = requirement[0:_pound_pos].strip()
        if len(requirement):
            install_requires.append(requirement)
    return install_requires

version = read('version.txt')

setup(
    name='rdc.dic',
    namespace_packages = ['rdc'],
    version=version,
    description="Simple dependency injection container",
    long_description=read('README.rst'),
    classifiers=read('classifiers.txt', tolines),
    author='Romain Dorgueil',
    author_email='romain@dorgueil.net',
    url='http://dic.rdc.li/',
    download_url='https://github.com/rdcli/rdc.dic/tarball/' + version,
    license='Apache License, Version 2.0',
    packages=find_packages(exclude=['ez_setup', 'example', 'test']),
    include_package_data=True,
    install_requires=read('requirements.txt', requirements_filter),
)
