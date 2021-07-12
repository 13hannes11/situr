from setuptools import setup, find_namespace_packages

setup(name='situr',
      version='0.1',
      description='A package to register situ images',
      url='https://github.com/13hannes11/situr',
      author='Hannes F. Kuchelmeister',
      author_email='hannes@kuchelmeister.org',
      license='MIT',
      packages=find_namespace_packages(include=['situr.*']),
      zip_safe=False)
