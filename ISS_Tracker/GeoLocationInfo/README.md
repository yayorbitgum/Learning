# This is where you place your data files locally, ie 
  - NationalFile_20200501.txt containing all US-based geographical data, or
  - Countries_populatedplaces_p.txt containing all geographical data of populated locations on the entire planet, 
but they're way too large to upload to github!

In the future for a real application, I'd need to host these on a server and make requests.
But for my own personal use, let's just use my perfectly free-to-access local SSD.

If you want to follow along, you can always grab the files for yourself from:
  - https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
  - https://geonames.nga.mil/gns/html/namefiles.html
 
 Unzip them, and place them in this folder.
 For the hdf5 converter, the list names are based on "National File (all features in one file)",
 and "Entire country files dataset separated by feature class (Approximately 459MB compressed/2.37GB uncompressed) - Dated 2020-06-22".
