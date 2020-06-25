# ISS Location Tracker

Keeps track of current International Space Station location using API from http://api.open-notify.org/, checks to see if it's above me in OKC or nearby, and displays the current distance away from the center of my sky.

WIP features:

- Check current ISS coordinates and return closest Earth feature, whether on land or at sea (uses local geographical databases on PC for now)
- Input current location to check distance from wherever, not just OKC.
- Interface, visual map representation.

Databases that I use for checking coordinates vs known locations (after converting to hdf5 format):

- US locations (National File): https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
- Global locations (separated by feature class): https://geonames.nga.mil/gns/html/namefiles.html