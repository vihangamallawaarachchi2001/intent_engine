from setuptools import setup

package_name = 'intent_engine'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    maintainer='vihanga mallawaarachchi',
    maintainer_email='vihanganethusara00@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'intent_engine_node = intent_engine.intent_node:main',
            'intent_cli = intent_engine.cli:main',
        ],
    },
)