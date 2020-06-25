# ISS Location Tracker

Keeps track of current International Space Station location using API from http://api.open-notify.org/, checks to see if it's above me in OKC or nearby, and displays the current distance away from the center of my sky. Also displays information about geographical locations the ISS is flying over, if they're in the US or in populated areas on the globe.

WIP features:

- Check current ISS coordinates and showing if it's flying over any and all global features, including ocean and underwater locations.. Assuming they're in these databases.
- Input current location to check distance from wherever, not just OKC.
- Interface, visual map representation.

Databases that I use for checking coordinates vs known locations (after converting to hdf5 format):

- US locations (National File): https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
- Global locations (separated by feature class): https://geonames.nga.mil/gns/html/namefiles.html
