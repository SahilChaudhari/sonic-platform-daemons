from setuptools import setup

setup(
    name='sonic-interruptd',
    version='1.0',
    description='Interrupt info gathering daemon for SONiC',
    license='Apache 2.0',
    author='SONiC Team',
    author_email='linuxnetdev@microsoft.com',
    url='https://github.com/Azure/sonic-platform-daemons',
    maintainer='AMD',
    maintainer_email='sahil.chaudhari@amd.com',
    scripts=[
        'scripts/interruptd',
    ],
    setup_requires=[
        'wheel'
    ],
    tests_require=[
        'mock>=2.0.0; python_version < "3.3"',
        'pytest',
        'pytest-cov',
        'sonic_platform_common'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Hardware',
    ],
    keywords='sonic SONiC INTERRUPT interrupt INTERRUPTD interruptd',
)