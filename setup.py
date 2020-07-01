import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djangorestframework_simplejwt_casng",
    version="0.0.1",
    author="Changsheng Yan",
    author_email="cs.yan@outlook.com",
    description="A JSON Web Token authentication plugin for the Django REST Framework, "
                "integrated with CAS Authentication.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChangshengYan/djangorestframework-simplejwt-casng",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'django>=3.0',
        'django-cas-ng',
        'djangorestframework',
        'djangorestframework-simplejwt',
    ]
)
