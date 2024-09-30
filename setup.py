from setuptools import setup, find_packages

setup(
    name='pentest',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'paramiko',
        'termcolor',
        'chardet',
        'pydantic',
        'ipykernel '
    ],
    include_package_data=True,
)
