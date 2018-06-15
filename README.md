CreateDS-uploadfile.py:<br>
-create dataset (using an atom.xml and sword api)<br>
-get returned dataset_id<br>
-upload file to dataset (using returned dataset_id) and passed description (uses native api)<br>
</p>

<p>
Pull-dataset-metadata.py:<br>
Script example for extracting metadata from dataverse<br>
-function getID lists all returned objects under top dataverse_id<br>
-then if 'type' == dataset, parses out dataset_id<br>
-then runs function getMetadata which shows the dataset whose ID is passed<br>
-output of getMetadata could be dumped in file for future work<br>
                                                                


