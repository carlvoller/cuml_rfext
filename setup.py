from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext
from sysconfig import get_path

platlib = get_path("platlib")

__version__ = "0.0.1"

ext_modules = [
    Pybind11Extension(
        "cuml_rfext._core",
        sources=["src/main.cpp"],
        language="c++",
        extra_compile_args=["-O3", "-std=c++17", "-g"],
        include_dirs=[
          f"{platlib}/libcuml/include",
          f"{platlib}/libraft/include",
        ],
        libraries=["cuml++"],
        library_dirs=[f"{platlib}/libcuml/lib64"],
        runtime_library_dirs=[f"{platlib}/libcuml/lib64"],
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name='cuml_rfext',
    version=__version__,
    author='Carl Voller',
    author_email='carl@carlvoller.is',
    description='Extension to add feature_importances_ to CUML\'s RandomForestClassifier and RandomForestRegressor',
    ext_modules=ext_modules,
    packages=find_packages(),
    cmdclass=dict(build_ext=build_ext),
    url="https://github.com/carlvoller/cuml_rfext",
    zip_safe=False,
    python_requires=">=3.10",
    build_requires=[
        'cuml-cu12',
        'cudf-cu12',
        'pylibraft-cu12',
        'setuptools',
        'pybind11[global]'
    ],
    install_requires=[
        'cuml-cu12',
        'cudf-cu12',
        'pylibraft-cu12',
    ],
    setup_requires=[
        'cuml-cu12',
        'cudf-cu12',
        'pylibraft-cu12',
    ],
    dependency_links=[
        'https://pypi.nvidia.com'
    ]
)