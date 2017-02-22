from setuptools import setup, find_packages
from codecs import open


version = open('packaging/VERSION').read().strip()
requirements = open('packaging/requirements.txt').read().split("\n")
test_requirements = open('packaging/requirements-test.txt').read().split("\n")
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ncrawl',
    version=version,
    author='Workonline Communications',
    author_email='communications@workonkonline.co.za',
    description='A network topology crawler and mapper',
    long_description=long_description,
    license='LICENSE',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(
        include=[
            'ncrawl',
            'ncrawl.*'
        ],
        exclude=[]
    ),
    include_package_data=True,

    url='https://github.com/wolcomm/ncrawl',
    download_url='https://github.com/wolcomm/ncrawl/%s' % version,

    install_requires=requirements,
    test_requires=test_requirements,
    #test_suite='test.exec'
)
