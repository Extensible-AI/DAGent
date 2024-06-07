from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dagent',
    version='0.0.1',
    packages=find_packages(include=['dagent', 'dagent/']),
    install_requires=required,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    author='Parth Sareen, Omkaar Kamath',
    author_email='parth@extensible.dev, omkaar@extensible.dev',
    description='AI Agents as Directed Acyclic Graphs (DAGs)',
    url='https://github.com/Extensible-AI/DAGent/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
