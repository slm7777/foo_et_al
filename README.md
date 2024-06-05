# Example package

This is a simple example package for slm7777's application to UCAR REQ-2024-114 Software Engineer I.
foo_et_al contains a base class foo that can be extended, and a sphere subclass. 

To install the package, type

    python -m pip install --index-url https://test.pypi.org/simple/ foo_slm7777

To test, open python and enter the following:

    >> from foo_slm7777 import foo
    >> s = foo.sphere()
    >> s.set(radius=10., units='meters')
    >> print(str(s))
    >> Vol, unitstr = s.get_volume()
    >> print(f'Sphere s has volume {Vol} {unitstr}')

The following should be displayed:

    The sphere has radius 10.0 meters
    Sphere s has volume 4188.790204786391 meters**3
