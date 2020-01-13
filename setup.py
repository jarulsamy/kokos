from setuptools import setup

with open("README.md", "r") as f:
	README = f.read()

with open("LICENSE", "r") as f:
	LICENSE = f.read()

setup(
	name="kokos",
	author="kokos",
	version="0.1.3",
	description="kokos is a multi-use package",
	long_description=README,
	long_description_content_type="text/markdown",
	license=LICENSE,
	py_packages=[
		"cpu_stress_test",
		"fof_management",
	],
	package_dir={"": "src"},
	keywords="kokos package multi-use",
	url="https://github.com/kokosxD/kokos",
	download_url="https://github.com/kokosxD/kokos/archive/master.zip",
	install_requires=[
		"bcrypt>=3.1.7",
		"datetime>=4.3",
	],
	project_urls={
		"Documentation": "https://github.com/kokosxD/kokos/blob/master/README.md",
		"Source Code": "https://github.com/kokosxD/kokos",
	},
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    	"Operating System :: Microsoft :: Windows",
    ],
	scripts=[
		"scripts/kokos.bat",
		"scripts/main.py",
	],
)
