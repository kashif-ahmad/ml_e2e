# this file is central to create the application as a package and deploy it using pipelines

from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name='ml_e2e',
    version='1.0.0',
    author='Kashif',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)
       
