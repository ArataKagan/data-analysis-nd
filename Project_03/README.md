<h1>Wrangle OpenStreetMap Data Project</h1>

In this project, I use data munging techniques, such as assessing the quality of the data for validity, 
accuracy, completeness, consistency and uniformity, to clean the OpenStreetMap data for 
San Francisco/Bay Area. 

Please refer to <a href='https://wiki.openstreetmap.org/wiki/About_OpenStreetMap'>this link</a> for more detail about the OpenStreetMap.

I have learnt the following points thoughout this project:

<ol>
<li>Assess the quality of the data for validity, accuracy, completeness, consistency and uniformity.</li>
<li>Parse and gather data from popular file formats such as .csv, .json, .xml, and .html</li>
<li>Process data from multiple files or very large files that can be cleaned programmatically.</li>
<li>Learn how to store, query, and aggregate data using SQL.</li>
</ol>

<h3>File directories</h3>

`SF_OpenStreetMap_project.pdf` : pdf file for going though the project rubric<br>
`database_preparation.py` : main python script to clean the dataset and store into SQL<br>
`get_city.py` : function for extracting city names<br>
`get_streetname.py` : function for extracting street names<br>
`get_tiger_county.py` : function for extracting tiger<br> 
`get_zipcode.py` : function for extracting zipcode<br>
`sf_osm_sample.osm` : San Francisco/Bay Area osm file (9.4M)<br>
