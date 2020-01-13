from setuptools import find_packages, setup


setup(
    name='optimized-loop-utils',
    python_requires='>=2.6',
    version='0.1.0',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    packages=find_packages(),
    install_requires=[
        'futures; python_version=="2.7"',
        'enum34; python_version<"3.4"',
    ],
)