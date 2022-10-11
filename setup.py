from setuptools import find_packages, setup

setup(
    name='dash_app',
    version='1.0',
    description='COMP0034 Coursework 1 2021-22',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plotly',
        'pandas',
        'dash',
        'dash-bootstrap-components',
        'dash-daq'
    ],
)
