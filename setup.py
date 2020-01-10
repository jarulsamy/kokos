from setuptools import setup

with open("README.md", "r") as f:
	README = f.read()

setup(
	name="kokos",
	author="kokos",
	version="0.1.1",
	description="kokos is a multi-use package",
	long_description=README,
	long_description_type="text/markdown",
	py_packages=["cpu_stress_test"],
	package_dir={"": "kokos"},
	keywords="kokos package multi-use",
	url="https://pypi.org/project/kokos/",
	install_requires=[
		"bcrypt > =3.1.7",
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
		"scripts/cpu_stress_test",
	],
)
