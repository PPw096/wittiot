import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name="wittiot",
  version="1.0.11",
  author="PPw096",
  author_email="1225835565@qq.com",
  description="WSView Plus support",
  url='https://github.com/PPw096/wittiot',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)