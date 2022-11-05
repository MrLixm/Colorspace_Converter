# ColorSpace Converter

> **Warning** This application is archived and not maintained anymore.
>
> You can still browse the code but it is not production-quality and I do not recommend to even use it as learning material.


This application was intended to be use for cgi production and especially when working with [ACES](https://acescentral.com/) 

The application provide an interface and functions to convert 2d image inputs to a target RGB colorspace.

## Documentation

You can find the documentation here: <https://mrlixm.github.io/PYCO/standalone/ColorspaceConvert/home/>

## Development 

OS: Windows 10
Python version 3.6.8

VirtualEnvironment:
```
$ pip install PySide2==5.13.1
$ pip install colour-science==0.3.15
$ pip install 'colour-science[optional]'
$ pip install fbs==0.8.6
$ pip install "..\oiio-2.0.5-cp36-none-win_amd64.whl"
```
The oiio Python wheel can be downloaded here: <https://github.com/fredrikaverpil/oiio-python/releases>

**Shared under CC BY-SA 4.0 license.**
BY – Credit must be given to the creator
SA – Adaptations must be shared under the same terms
https://creativecommons.org/licenses/by-sa/4.0/
