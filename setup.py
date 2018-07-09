from setuptools import setup, find_packages

setup(
    name='Piton 2000',
    version='0.0.1',
    packages=find_packages(exclude=['examples', 'tests*']),
    url='https://github.com/MalumAtire832/P2000',
    license='GPL-3.0',
    author='Harjan Knapper',
    author_email='harjan@knapper-development.nl',
    description='Piton 2000 is a service that can connect to the Dutch P2000 network to monitor the messages send by alarm centers to the Fire Departments, Police stations, Ambulance services or the KNRM.'
)

# entry_points={
#     'console_scripts': [
#         'piton2000=p2000.cli.runner:main',
#     ],
# },
