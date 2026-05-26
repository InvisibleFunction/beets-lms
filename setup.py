from setuptools import setup, find_namespace_packages

setup(
    name='beets-lms',
    version='0.0.3',
    description='beets plugin for Lyrion Music Server',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/InvisibleFunction/beets-lms',
    license='MIT',
    platforms='ALL',
    packages=find_namespace_packages(include=['beetsplug']),
    install_requires=[
        'beets>=2.4.0',
        'requests'
    ],
    python_requires=">=3.11",
)
