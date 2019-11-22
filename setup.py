from setuptools import setup,find_packages
assert setuptools.__version__>=36.2

# note: version is maintained inside nbdev/version.py
config = ConfigParser()
config.read(file)
cfg = config['DEFAULT']
readme = open('README.md').read()

requirements = """
    nbformat>=4.4.0 nbconvert pyyaml
""".split()

setup(
    name = cfg['lib_name'],
    version = cfg['version'],
    description = "Writing a library entirely in notebooks",
    keywords = 'jupyter notebook',
    author = "Sylvain Gugger and Jeremy Howard",
    author_email = 'info@fast.ai',
    license = "Apache Software License 2.0",

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    url = 'https://github.com/{}/{}'.format(cfg['user'],cfg['lib_name']),
    packages = find_packages(),
    include_package_data = True,
    install_requires = requirements,
    setup_requires   = setup_requirements,
    python_requires  = '>=3.6',
    long_description = readme,
    long_description_content_type = 'text/markdown',

    zip_safe = False,
)
