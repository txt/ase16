from setuptools import setup

def readme():
      with open('README.mt') as f:
                return f.read()

setup(name='package101',
      version='0.1',
      description='python package template',
      url='https://github.com/txt/ase16/tree/master/src/package101',
      author='Tim Menzies',
      author_email='tim@menzies.us',
      license='MIT',
      packages=[],
      install_requires=['markdown'],
      zip_safe=False)
