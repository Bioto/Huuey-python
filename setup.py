from setuptools import setup, find_packages

print find_packages()

setup(name='Huuey',
      version='0.1',
      description='Handles managing phillips hue lights',
      url='https://github.com/Bioto/Huuey-python',
      author='Nicholas Young',
      author_email='nick@coding.exposed',
      license='MIT',
      packages=find_packages())