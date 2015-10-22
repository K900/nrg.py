from setuptools import setup, find_packages

setup(
    name='nrgpy',
    description='A library for interfacing with the "Energia" package delivery company REST API.',
    long_description=open('README.md').read(),
    version='0.0.1',
    py_modules=['nrg'],
    entry_points={
        'console_scripts': ['nrg=nrg:_track_main'],
    },
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords=['energia', 'package delivery']
)
