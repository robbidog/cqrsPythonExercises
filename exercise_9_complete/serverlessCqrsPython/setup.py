from setuptools import setup

setup(
    name='serverlessCqrsPython',
    version='1.0',
    packages=['azure-functions', 'photonpump',  'asyncio', 'Flask'],
    url='',
    license='',
    author='Rob Hale',
    author_email='rob.hale@adaptechgroup.com',
    description='An implementation of CQRS in Python suitable for server-less deployment', install_requires=['azure-function', 'Flask', 'photonpump', 'asyncio']
)
