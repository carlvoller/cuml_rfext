from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext
from sysconfig import get_path, get_python_version
from glob import glob
import os

python_version = get_python_version()
cwd = os.getcwd()

platlib = get_path("platlib")
platlib_tmp_overlay = f"{cwd}/overlay/lib/python{python_version}/site-packages"

libcuml_path = f"{platlib}/libcuml" if os.path.isdir(f"{platlib}/libcuml") else f"{platlib_tmp_overlay}/libcuml"
libraft_path = f"{platlib}/libraft" if os.path.isdir(f"{platlib}/libraft") else f"{platlib_tmp_overlay}/libraft"



__version__ = "0.0.2"

ext_modules = [
    Pybind11Extension(
        "cuml_rfext._core",
        sorted(glob("src/*.cpp")),
        language="c++",
        extra_compile_args=["-O3", "-std=c++17", "-g"],
        include_dirs=[
          f"{libcuml_path}/include",
          f"{libraft_path}/include",
        ],
        libraries=["cuml++"],
        library_dirs=[f"{libcuml_path}/lib64"],
        runtime_library_dirs=[f"{libcuml_path}/lib64"],
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