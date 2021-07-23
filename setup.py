from setuptools import setup, find_namespace_packages

setup(name='situr',
      version='0.1',
      description='A package to register situ images',
      url='https://github.com/13hannes11/situr',
      author='Hannes F. Kuchelmeister',
      author_email='hannes@kuchelmeister.org',
      license='MIT',
      packages=find_namespace_packages(include=['situr.*']),
      install_requires=[
          'numpy>=1.21.0',
          'open3d>=0.13.0',
          'Pillow>=8.3.1',
          'scikit-image>=0.18.2',
          'scikit-learn>=0.24.2',
          'scipy>=1.7.0'
      ],
      zip_safe=False)
