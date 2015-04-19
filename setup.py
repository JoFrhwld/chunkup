from setuptools import setup

setup(name='chunkup',
      version='0.1',
      description='chunks up audio',
      url='https://github.com/JoFrhwld/chunkup',
      author='Josef Fruehwald',
      author_email='jofrhwld@gmail.com',
      license='MIT',
      packages=['chunkup'],
      install_requires = ['pysox'],
      zip_safe=False)