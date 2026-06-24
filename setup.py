from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

import numpy as np
from Cython.Build import cythonize


class OptionalBuildExt(build_ext):
    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except (Exception, SystemExit):
            if not getattr(ext, "optional", False):
                raise
            self.warn(
                f"Skipping optional extension {ext.name!r}. "
                "Install Python development headers to enable Cython/OpenMP."
            )


extensions = [
    Extension(
        "core.solver_accel",
        ["core/solver_accel.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3", "-fopenmp"],
        extra_link_args=["-fopenmp"],
        optional=True,
    )
]

cythonized_extensions = cythonize(
    extensions,
    compiler_directives={
        "boundscheck": False,
        "wraparound": False,
        "initializedcheck": False,
        "language_level": "3",
    },
)
for extension in cythonized_extensions:
    extension.optional = True


setup(
    cmdclass={"build_ext": OptionalBuildExt},
    ext_modules=cythonized_extensions,
)
