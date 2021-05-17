import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


packages = ['website_checker']

requires = [
    'requests==2.25.1',
    'fire==0.4.0',
    'confluent-kafka==1.7.0',
    'psycopg2-binary==2.8.6',
    'kafka-python==2.0.2',
    'flake8==3.9.2'
]

test_requirements = [
    'pytest>=6.2.4',
    'requests-mock==1.9.2',
    'pytest-cov==2.12.0'
]

setup(
    name='website_checker',
    version='1.0.0',
    description='Python website checker to produce, consume data and save to DB',
    long_description="",
    long_description_content_type='text/markdown',
    author='Yifei Zuo',
    author_email='yfieizuo@gmail.com',
    url='TODO',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'website_checker': 'website_checker'},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
    ],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    project_urls={
        'Source': 'https://github.com/yifeizuo/website_checker',
    },
    scripts=[
        'bin/website_checker-produce',
        'bin/website_checker-consume'
    ],
)
