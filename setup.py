# encoding=utf8
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.md')

setup(
    name = "django-user-profiles",
    version = "0.1.0",
    url = 'http://github.com/philomat/django-user-profiles',
    license = 'BSD',
    description = "django-user-profiles is a flexible app that wires together Django's user authentication and user profile features, with customizable forms and models and user activation.",
    long_description = README,

    author = u'Samuel Luescher',
    author_email = 'philomat@popkultur.net',
    
    packages = find_packages(),
    include_package_data=True,

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

print find_packages()