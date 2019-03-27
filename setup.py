from setuptools import setup

setup(
    name='autoitpy',
    version='0.1',
    description='AutoItX wrapper for python',
    url='http://github.com/',
    author='Abdullah Husein',
    author_email='abdullah.husein9192@gmail.com',
    license='MIT',
    packages=['autoitpy'],
    package_data={'autoitpy': ['AutoItX/*.dll']},
    zip_safe=False
)
