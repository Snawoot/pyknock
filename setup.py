from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'rb') as f:
    long_description = f.read().decode('utf-8')

setup(name='pyknock',
      version='0.4.1',
      description='UDP port knocking suite with HMAC-PSK authentication',
      url='https://github.com/Snawoot/pyknock',
      author='Vladislav Yarmak',
      author_email='vladislav@vm-0.com',
      license='MIT',
      packages=['pyknock'],
      python_requires='>=2.6',
      setup_requires=[
          'wheel',
      ],
      scripts=[
          'pyknock-server',
          'pyknock-client',
      ],
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Development Status :: 5 - Production/Stable",
          "Environment :: No Input/Output (Daemon)",
          "Intended Audience :: System Administrators",
          "Natural Language :: English",
          "Topic :: Internet",
          "Topic :: System :: Networking :: Firewalls",
          "Topic :: Security",
          "Topic :: Utilities",
      ],
	  long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=True)
