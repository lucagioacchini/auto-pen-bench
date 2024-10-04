from setuptools import setup, find_packages

setup(
    name='autopenbench',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv==1.0.1',
        'paramiko==3.5.0',
        'termcolor==2.4.0',
        'chardet==5.2.0',
        'pydantic==2.9.2',
        'ipykernel==6.29.5',
        'pyyaml==6.0.2',
        'openai==1.51.0',
        'instructor==1.5.0'
    ],
    include_package_data=True,
)
