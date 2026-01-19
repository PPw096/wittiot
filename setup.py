import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name="wittiot",
  version="1.0.33",
  author="PPw096",
  author_email="1225835565@qq.com",
  description="WSView Plus support",
  url='https://github.com/PPw096/wittiot',
  long_description=long_description,
  long_description_content_type="text/markdown",
  python_requires=">=3.8",
  packages=setuptools.find_packages(),
  install_requires=[
    "aiohttp",
    "requests",
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
