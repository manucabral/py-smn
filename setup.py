from setuptools import setup, find_packages

setup(
    name='py-smn',
    version='0.1.0',
    description='A Python wrapper for the SMN API Argentina',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/manucabral/py-smn',
    project_urls={
        'Documentation': 'https://github.com/manucabral/py-smn/blob/main/README.md',
        'Bug Tracker': 'https://github.com/manucabral/py-smn/issues',
    },
    author='Manuel Cabral',
    keywords=['smn', 'weather', 'forecast', 'api', 'argentina', 'smn-api'],
    license='MIT',
    packages=find_packages(),
    install_requires=['aiohttp'],
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
