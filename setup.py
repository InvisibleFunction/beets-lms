from setuptools import setup

setup(
    name='beets-lms',
    version='0.0.1',
    description='beets plugin for Lyrion Music Server',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/InvisibleFunction/beets-lms',
    license='MIT',
    platforms='ALL',
    packages=['beetsplug'],
    install_requires=[
        'beets>=1.6.0',
        'requests'
    ],
    python_requires=">=3.7",
)
