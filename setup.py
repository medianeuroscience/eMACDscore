from setuptools import setup, find_packages

setup(name='emacscore',
      version='0.0.1',
      description='Extended Morality as Cooperation Dictionary for Python',
      url='https://github.com/medianeuroscience/emacscore',
      author='Anonymized.',
      author_email='musamalik@ucsb.edu',
      license='MIT',
      packages=['emacscore'],
      scripts=['bin/emacscore'],
      include_package_data=True, 
      install_requires=[
          'pandas',
          'progressbar2',
          'sklearn',
          'nltk',
          'numpy',
          'pickle5' 
      ],
      zip_safe=False)
