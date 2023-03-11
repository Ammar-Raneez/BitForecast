from setuptools import find_packages, setup

# Added into requirements.txt to trigger setup.py on pip install
AUTO_TRIGGER_TOKEN = '-e .'

def get_requirements(file_path):
  '''
  Read and return the requirements used by this project
  '''

  requirements = []
  with open(file_path, 'r') as f:
    requirements = f.readlines()
    requirements = [req.replace('\n', '') for req in requirements]

    if AUTO_TRIGGER_TOKEN in requirements:
      requirements.remove(AUTO_TRIGGER_TOKEN)

  return requirements

setup(
  name='BitForecast-deployment',
  version='1.0.0',
  author='Ammar',
  author_email='ammarraneez@gmail.com',
  packages=find_packages(),
  install_requires=get_requirements('requirements.txt'),
)