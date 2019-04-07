

from setuptools import setup, find_packages

package_version = '0.1.0'
package_name = 'slackpyez'


def requirements(filename='requirements.txt'):
    return open(filename.strip()).readlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name=package_name,
    version=package_version,
    description='For creating Slack apps in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jeremy Schulman',
    packages=find_packages(),
    install_requires=requirements(),
)
