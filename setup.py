from setuptools import setup, find_namespace_packages

setup(
    name='vsdkx-cli',
    url='https://gitlab.com/natix/cvison/vsdkx/vsdkx-cli',
    author='Helmut',
    author_email='helmut@natix.io',
    namespace_packages=['vsdkx'],
    packages=find_namespace_packages(include=['vsdkx*']),
    dependency_links=[
        'git+https://gitlab+deploy-token-485942:VJtus51fGR59sMGhxHUF@gitlab.com/natix/cvison/vsdkx/vsdkx-core.git#egg=vsdkx-core'
    ],
    install_requires=[
        'vsdkx-core',
        'argparse',
        'argcomplete',
        'minio'
    ],
    entry_points = {
        'console_scripts': ['vsdkx-cli=vsdkx.cli.vsdkx_cli:main'],
    },
    version='1.0',
)
