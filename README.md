# Synopsis
CO-NCRN is the University of Colorado at Boulder branch of the [NSF-Census Research Network](https://www.ncrn.info/node/university-colorado-boulder-university-tennessee). The ACS Regionalization code is one project to emerge from our work, providing an algorithm that takes in small-area American Community Survey estimates and produces optimized regions that reduce high levels of uncertainty in the data. The results are maps and tables with new geographies that maintain granularity but improve data quality, thereby enhancing researchers' ability to ensure their results are not comprised by high uncertainty.

Please visit the main page of this repository, [co-ncrn.github.io](co-ncrn.github.io) to acess information about this project and obtain regionalization results for a selection of input data applied to all metropolitan statistical areas in the United States. To use your own input variables and geographies, you can access the regionalization algorithm at [this repository](https://github.com/geoss/ACS_Regionalization).

# Results 

Regionalization results are provided for four scenarios, housing, poverty, transportation, and a general scenario, and applied to 388 Metropolitan Statistical Areas as defined in 2013. The input data derives from the 2008-2012 American Community Survey.

Each result can be downloaded from the website as a zip file containing:
- A crosswalk between input tracts and output regions
- Input values for original and derived ACS variables for original tracts and computed regions
- Output values for the original and derived ACS variables for the computed regions
- Shapefiles for the input tracts and output regions
- A weights matrix for the output regions
- A data dictionary
- A metadata file

GeoJSON maps of the input tracts and output regions with associated data are displayed and available for download as well.



# Motivation

A short description of the motivation behind the creation and maintenance of the project. This should explain why the project exists.

# Tests

Describe and show how to run the tests with code examples.

# Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

# License
