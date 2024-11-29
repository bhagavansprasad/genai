from setuptools import setup
import os

# Create folders
folders = ['vectDB', 'embeddings']
for folder in folders:
    os.makedirs(folder, exist_ok=True)

setup(
    name="VectorDB Operations",
    version="0.1",
    install_requires=open('requirements.txt').readlines(),
)

