from setuptools import setup, Extension

evolvent_module = Extension("evolvent_c", sources=["evolvent.c"])

setup(
    name="evolvent_c",
    version="1.0",
    description="Evolvent c implementation",
    ext_modules=[evolvent_module],
)
