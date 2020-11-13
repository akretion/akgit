# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

long_description = []
with open(os.path.join("README.rst")) as f:
    long_description.append(f.read())
with open(os.path.join("CHANGES.rst")) as f:
    long_description.append(f.read())


setup(
    name="akgit",
    description="Git helper for akretion",
    long_description="\n".join(long_description),
    long_description_content_type="text/x-rst",
    use_scm_version=True,
    packages=["akgit"],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
    license="AGPLv3+",
    author="Akretion",
    author_email="contact@akretion.com",
    url="http://github.com/akretion/akgit",
    install_requires=[
        r.strip() for r in open('requirements.txt').read().splitlines() ],
    entry_points="""
    [console_scripts]
    akgit=akgit.main:main
    """,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Framework :: Odoo",
    ],
)
