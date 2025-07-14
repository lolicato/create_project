from setuptools import setup, find_packages

setup(
    name='start-md-project',
    version='0.1.0',
    description='A tool to easily create MD project templates',
    author='Fabio Lolicato',
    author_email='lolicato.fabio@gmail.com',
    url='https://github.com/yourusername/start-md-project',
    packages=find_packages(),
    install_requires=[],  # Add dependencies here
    entry_points={
        'console_scripts': [
            'start-md-project=start-md-project.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)