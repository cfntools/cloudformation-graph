from setuptools import setup


def get_version():
    with open('version.txt', 'r') as fh:
        return fh.read().strip()


setup(
    name='cfn-graph',
    version=get_version(),
    description="Tool to turn CloudFormation related resources into graphs",
    author='Ben Bridts',
    author_email='ben.bridts@gmail.com',
    url='',  # todo
    packages=['cfn_graph'],
    entry_points={
        'console_scripts': [
            'cfn-graph = cfn_graph.cli:main',
        ]
    },
    install_requires=[
          'graphviz',
      ],
)
