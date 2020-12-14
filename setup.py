from setuptools import setup, find_packages

setup(
      # mandatory
      name='cloudphoto',
      # mandatory
      version='0.1',
      description='cli script for download/upload photo album',
      # mandatory
      author='Vladislav Alekseev',
      author_email='vladalekseev9@yandex.ru',
      packages=['cloudphoto'],
      package_data={},
      install_requires=['boto3', 'botocore', 'redis-py-cluster', 'logging', 'requests', 'click'],
      entry_points={
        'console_scripts': ['cloudphoto = cloudphoto.cli:start']
      }
)