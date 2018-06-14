<h1>Wrangle OpenStreetMap Data Project</h1>

<ol>
<li>Assess the quality of the data for validity, accuracy, completeness, consistency and uniformity.</li>
<li>Parse and gather data from popular file formats such as .csv, .json, .xml, and .html</li>
<li>Process data from multiple files or very large files that can be cleaned programmatically.</li>
<li>Learn how to store, query, and aggregate data using MongoDB or SQL.</li>
</ol>

use data munging techniques, such as assessing the quality of the data for validity, 
accuracy, completeness, consistency and uniformity, to clean the OpenStreetMap data for 
San Francisco/Bay Area. 


<h3>File directories</h3>

`SF_OpenStreetMap_project.pdf` : pdf file for going though the project rubric 
`database_preparation.py` : main python script to clean the dataset and store into SQL
`get_city.py` : function for extracting city names 
`get_streetname.py` : function for extracting street names
`get_tiger_county.py` : function for extracting tiger 
`get_zipcode.py` : function for extracting zipcode
`sf_osm_sample.osm` : San Francisco/Bay Area osm file (9.4M)
