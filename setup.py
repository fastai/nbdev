from setuptools import setup,find_packages

# note: version is maintained inside nbdev/version.py
exec(open('nbdev/version.py').read())
with open('README.md') as readme_file: readme = readme_file.read()

requirements = """
    nbformat>=4.4.0 nbconvert pyyaml
""".split()

setup_requirements = ['setuptools>=36.2']
    
setup(
    name = "nbdev",
    version = __version__,
    packages = find_packages(),
    include_package_data = True,

    install_requires = requirements,
    setup_requires   = setup_requirements,
    python_requires  = '>=3.6',
    
    description = "Writing a library entirely in notebooks",
    long_description = readme,
    long_description_content_type = 'text/markdown',
    
    keywords = 'jupyter notebook',
    license = "Apache Software License 2.0",
    url = 'https://github.com/fastai/nbdev',
    author = "Sylvain Gugger and Jeremy Howard",
    author_email = 'info@fast.ai',
    
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    
    zip_safe = False,
)
