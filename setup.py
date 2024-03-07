from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pure_clean/__init__.py
from pure_clean import __version__ as version

setup(
	name="pure_clean",
	version=version,
	description="Customization for Pure Clean",
	author="GreyCube Technologies",
	author_email="admin@greycube.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
