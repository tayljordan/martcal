martcal
=======

Current release: 0.1.0


Description
-----------

Martcal is a Python package for calculating the distance from any point
at sea to a port, accounting for land masses. The method used
is based on spherical trigonometry, where the system will locate:
1. nearest port from sea using mercator distance 
2. distance from nearest port to destination port using static tables

The outcome will be the at-sea leg of resultant triangle.


Installation
------------

Requirements:

 - Python 3.5+

Installing using `poetry`:

    poetry add martcal --git https://github.com/tayljordan/martcal.git

Installing using `pip`:

    pip install https://github.com/tayljordan/martcal/archive/master.zip


Documentation
-------------

Short example is located in the `doc` directory.


Contributing
------------

Open an issue or send a pull request on the Github
(https://github.com/tayljordan/martcal).


Authors
-------

 - Jordan Taylor
 - Miodrag Tokić


Copyright
---------

Copyright (C) 2019 Jordan Taylor.

Released under the MIT License. See the LICENSE file for details.
