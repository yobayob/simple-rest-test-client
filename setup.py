from setuptools import setup, find_packages

setup(
    name='simple_rest_test_client',
    version='0.0.3',
    description='Micro framework for testing REST API',
    author='yobayob',
    namespace_packages=['simple_rest_test_client'],
    packages=find_packages(),
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    install_requires=['jsonschema', 'validator.py==1.2.5', 'requests'],
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
        ],
    )