import arcpy
import json
import os

class Toolbox(object):
    def __init__(self):
        self.label = "JSON to Shapefile Toolbox"
        self.alias = "json2shp"
        self.tools = [JSONToShapefile]

class JSONToShapefile(object):
    def __init__(self):
        self.label = "JSON to Shapefile Tool"
        self.description = "Converts a JSON file with WKT geometries to a shapefile"
        self.canRunInBackground = False

    def getParameterInfo(self):
        in_json = arcpy.Parameter(
            displayName="Input JSON File",
            name="in_json",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        out_fc = arcpy.Parameter(
            displayName="Output Shapefile",
            name="out_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        return [in_json, out_fc]

    def execute(self, parameters, messages):
        in_json = parameters[0].valueAsText
        out_fc = parameters[1].valueAsText
        sr = arcpy.SpatialReference(4326)

        with open(in_json, "r") as file:
            data = json.load(file)

        records = data["data"]
        folder, name = os.path.split(out_fc)
        arcpy.env.workspace = folder
        arcpy.env.overwriteOutput = True
        arcpy.management.CreateFeatureclass(folder, name, "POLYGON", spatial_reference=sr)

        fields = [("OBJECTID", "LONG"), ("GEOID", "TEXT"), ("Cluster", "TEXT"),
                  ("Area", "DOUBLE"), ("Length", "DOUBLE")]
        for fname, ftype in fields:
            arcpy.management.AddField(out_fc, fname, ftype)

        skipped = 0
        with arcpy.da.InsertCursor(out_fc, ["SHAPE@"] + [f[0] for f in fields]) as cursor:
            for row in records:
                wkt = row[8].strip()
                if not wkt or wkt in ['{}', 'None', None]:
                    skipped += 1
                    continue
                try:
                    geom = arcpy.FromWKT(wkt, sr)
                    attr = [int(row[9]), row[10], row[11], float(row[12]), float(row[13])]
                    cursor.insertRow([geom] + attr)
                except:
                    skipped += 1
                    continue

        arcpy.AddMessage(f"{len(records) - skipped} features inserted.")
        arcpy.AddMessage(f"{skipped} records skipped due to invalid geometry.")
