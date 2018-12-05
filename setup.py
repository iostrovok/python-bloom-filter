from setuptools import setup, find_packages
from bloomfilter import __version__ as version


if __name__ == '__main__':
    setup(
        name='bloomfilter',
        version=version,
        description="",
        long_description="",
        classifiers=['MIT License'],
        url='https://github.com/iostrovok/python-bloom-filter',
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        provides=find_packages(include=['bloomfilter']),
        setup_requires=(
            'wheel',
        ),
        install_requires=(
            'couchbase==2.3.2',
        )
    )
