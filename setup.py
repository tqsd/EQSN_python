import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='EQSN',
    version='0.0.6',
    packages=['eqsn', ],
    license='MIT',
    author='Benjamin Zanger',
    author_email='benjamin.zanger@tum.de',
    description="A quantum simulator made for networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tqsd/EQSN_python',
    download_url='https://github.com/tqsd/EQSN_python/releases/tag/v0.0.6',
    keywords=['quantum-simulator', 'quantum-internet', 'QuNetSim'],
    install_requires=[
        'numpy',
      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    python_requires='>=3.6',
)
