from setuptools import setup

setup(name='chunkup',
      version='0.2',
      description='chunks up audio',
      url='https://github.com/JoFrhwld/chunkup',
      author='Josef Fruehwald',
      author_email='jofrhwld@gmail.com',
      license='MIT',
      packages=['chunkup'],
      install_requires = ['pysox'],
      scripts=['bin/chunkup'],
      zip_safe=False)