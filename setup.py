from setuptools import setup, find_namespace_packages

setup(
    name='vsdkx-cli',
    url='https://github.com/natix-io/vsdkx-cli',
    author='Helmut',
    author_email='helmut@natix.io',
    namespace_packages=['vsdkx'],
    packages=find_namespace_packages(include=['vsdkx*']),
    dependency_links=[
        'https://github.com/natix-io/vsdkx-core#egg=vsdkx-core'
    ],
    install_requires=[
        'vsdkx-core',
        'argparse',
        'argcomplete',
        'minio',
        'pyyaml'
    ],
    entry_points = {
        'console_scripts': ['vsdkx-cli=vsdkx.cli.vsdkx_cli:main'],
    },
    version='1.0',
)
