import os
from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext
from sysconfig import get_path, get_python_version
from glob import glob

is_ci_env = os.environ.get('IS_CI_ENV')

platlib = get_path("platlib")
libcuml_path = f"{platlib}/libcuml" 
libraft_path = f"{platlib}/libraft"

if not is_ci_env and not os.path.isdir(libcuml_path):
    raise ModuleNotFoundError("Module cuml-cu12 not found. Please install cuml-cu12 from https://docs.rapids.ai/install/ first before installing cuml_rfext.")

if not is_ci_env and not os.path.isdir(libraft_path):
    raise ModuleNotFoundError("Module pylibraft-cu12 not found. Please install pylibraft-cu12 from https://docs.rapids.ai/install/ first before installing cuml_rfext.")

__version__ = "0.0.6"

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
    install_requires=[
        'cuml-cu12',
        'pylibraft-cu12',
    ],
    dependency_links=[
        'https://pypi.nvidia.com'
    ]
)