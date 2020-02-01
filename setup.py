from setuptools import setup

with open("README.md", "r") as f:
	README = f.read()

with open("LICENSE", "r") as f:
	LICENSE = f.read()

with open("requirements.txt", "r") as f:
	requirements = f.read().split("\n")

setup(
	name="kokos",
	author="kokos",
	author_email="kokos",
	version="0.1.4",
	description="kokos is a multi-use package",
	long_description=README,
	long_description_content_type="text/markdown",
	license=LICENSE,
	packages=["kokos"],
	keywords="kokos package multi-use",
	url="https://github.com/kokosxD/kokos",
	download_url="https://github.com/kokosxD/kokos/archive/master.zip",
	install_requires=requirements,
	project_urls={
		"Documentation": "https://github.com/kokosxD/kokos/blob/master/README.md",
		"Source Code": "https://github.com/kokosxD/kokos",
	},
	classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    	"Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
