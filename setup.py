from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='chunkup',
      version='0.2.1',
      description='chunks up audio',
      long_description = readme(),
      url='https://github.com/JoFrhwld/chunkup',
      author='Josef Fruehwald',
      author_email='jofrhwld@gmail.com',
      license='MIT',
      packages=['chunkup'],
      install_requires = ['pysox'],
      scripts=['bin/chunkup'],
      zip_safe=False)