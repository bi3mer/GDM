from setuptools import find_packages, setup
setup(
    name='GSDM',
    packages=find_packages(),
    version='0.1.0',
    description='Graph-based sequential decision making (GDSM) is a simple library for MDP and model-free methods using networkx.',
    author='Colan Biemer',
    license='MIT',
    install_requires=['networkx'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='Tests',
)