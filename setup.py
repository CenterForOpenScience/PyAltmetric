from distutils.core import setup

setup(
    name='AltmetricLibrary',
    version='0.1.0',
    author='Lauren Revere',
    author_email='lauren.revere@gmail.com',
    packages=['altmetriclibrary', 'altmetriclibrary.test'],
    url='http://pypi.python.org/pypi/AltmetricLibrary/',
    license='LICENSE.txt',
    description='A python library for the Altmetric API.',
    long_description=open('README.txt').read(),
    install_requires=[open('requirements.txt').read()],
)
