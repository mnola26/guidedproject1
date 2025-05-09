The goal of this project was to convert the JSON file into a shapefile using Python so that it can be used in ArcGIS Pro. Since the JSON file included WKT, which cannot be directly imported into ArcGIS Pro, a custom code was needed to be able to process it and use it.

The code is included in this repository. There is the Jupyter Notebook as well as the Python toolbox for ArcGIS Pro.

**Code Development**
- I loaded the JSON file using Python's json module
- I extracted the geometry and attribute data
- I used arcpy.FromWKT() to convert valid WKT polygons into ArcGIS geometries
- I created a shapefile using arcpy.da.InsertCursor()
- I skipped records with invalid or empty WKT using try-except
- After verifying that the code worked, I put it into a Python Toolbox in ArcGIS Pro
- I used the JSON file as the input parameter and created an output for the shapefile path

**Using the Code**

- Open ArcGIS Pro
- Add json_to_shapefile.pyt to the Toolboxes folder
- Open the tool's interface
- Choose no_tax.json as the input and any .shp file path name for the output
- Run the tool and it will convert all the valid WKT polygons into a new shapefile
