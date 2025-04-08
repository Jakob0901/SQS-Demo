from setuptools import setup, find_packages

setup(
    name='your_flask_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-WTF',
        'SQLAlchemy',
        'psycopg2',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'run_app=app:main',
        ],
    },
)