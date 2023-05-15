### Table of Contents
***[Documentation](#documentation)***<br>
*[IfcMapConversion](#ifcmapconversion)*<br>
*[IfcMapConversionScaled](#ifcmapconversionscaled)*<br>
*[IfcRigidOperation](#ifcrigidoperation)*<br>
*[North](#north)*<br>
*[Epoch](#epoch)*<br>

***[Software](#software)***<br>
*[SketchUp](#sketchup)*<br>
*[ArcGIS](#arcgis)*<br>
*[Revit](#revit)*<br>
*[Blender](#blenderblenderbim)*<br>

***[Testfiles](#testfiles)***<br>

***[Experiments](#experiments)***<br>

***[Rules & Validation](#rules--validation)***<br>
*[Checks](#checks)*<br>
*[Best Practices](#best-practices)*<br>
*[Ideas](#ideas-related-to-georeferencing)*<br>
Ideas related to georeferencing


**Georeferencing**
Here are some notes I made after my initial review of the georeferencing-related terms in the documentation, attending a meeting with the implementers forum, using various georeferencing-related features of the software, and manually creating and modifying IFC files. 
The notes contains some remarks, questions, potential additions and ideas for rules or additions for the validation service. 
Please note that these observations are with limited knowledge. 

# Documentation
An overview of notes from georeferencing-related terms.
## IfcProjectedCRS
https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcProjectedCRS.htm
- What are the expected names for Geodetic Datum and Vertical Datum? When reading the documentation, one would expect the name of the Coordinate Reference System (CRS), such as ED50 and DHHN92, respectively. However, upon examining example files, it is more common to find an EPSG code being used instead. For example, https://github.com/buildingSMART/IFC4.x-IF/blob/aaef3f02ff003bf64048f8d54ac11c93d20d8524/IFC-files/Georeferencing/Georeferencing_COMPDCS(WKT)-RO.ifc#LL912C11-L912C11 . This expectation or requirements is very clear however in the 'Name' attribute (of the supertype 'IfcCoordinateReferenceSystem'). 
- In case the input at the attribute geodetic datum or vertical datum is different from the datums referred to in the name of the provided ESPG code, which is the case in some example files, which one has preference?
- A possible solution would be to specify the type of CRS, such as a Compound CRS, that consists of a geographic or projected CRS as the horizontal component, and a vertical CRS, such as "NAD83 + NAVD88 height". This information can then be inherited from 'IfcCoordinateReferenceSystem' (similar as 'IfcGeographicCRS') , with 'Geodetic Datum' and 'Vertical Datum' values being made non-optional. This would also address the previous question. https://proj.org/operations/operations_computation.html#compound-crs-to-a-geographic-crs

## IfcMapConversion
https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcMapConversion.htm
A proposal draft for the description :

> The map conversion is a process of transforming a local engineering coordinate system, also known as a world coordinate system, into the coordinate reference system of the underlying map. This involves mapping the local origin of the coordinate system, which defines the (0,0,0) point in the system, to its corresponding position in the map's coordinate system. The map conversion also allows for the rotation of the x-axis of the local engineering coordinate system within the horizontal plane of the map, which helps to align the coordinate system with the map's orientation.
**NOTE** the map conversion does not handle the projection of a map from the geodetic coordinate reference system. Geodetic projection is the process of representing a three-dimensional surface of the Earth onto a two-dimensional map, which is different from the map conversion process.
In the map conversion process, the z-axis of the local engineering coordinate system is always parallel to the z-axis of the map coordinate system. This means that the vertical height in the local engineering coordinate system can be converted to the height in the map's coordinate system, without any distortion.
**NOTE** the scale factor can be used in the map conversion process when the length unit for the three axes of the map coordinate system is different from the length unit established for the project. The scale factor is used to convert the units from one system to the other, and if it is omitted, a scale factor of 1.0 is assumed.'*

- Orthogonal Height, 'relative to the vertical datum specified'. Where is this specified? There could be a vertical datum specified in (the subtypes of) 'IfcCoordinateReferenceSystem', but not in IfcMapConversion. And if this is not specified, what should be filled in here?
- XAxisAbscissa, XAxisOrdinate could be described as the variables that determine where east is. These attributes are optional, but what are the consequences if they are not given? Is the MapConversion still accurate? Should they perhaps be not optional when the area of a given project is bigger than a certain value (e.g. 10km squared), see also the remarks under 'Rules & Validation'. They are also determined differently in different softwares. In Revit, it is the angle to True North / Derive North. In ArchiCAD, it is simply ordinate & absicca and a synonym in BlenderBIM is 'Derived Angle'. An idea would be to verify these differences among software and include it in the documentation.
- For 'Scale', the same as above. 

## IfcMapConversionScaled
https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcMapConversionScaled.htm

When is this entity used instead of IfcMapConversion, and, if clearly defined, would it be a hard requirement? This question came up in the meeting of the Implementers Forum on 20-4-2023. 

## IfcRigidOperation
https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRigidOperation.htm
- Definition is not very clear, a proposal draft:
- IfcRigidOperation is used to define a transformation that moves every point in a coordinate system by the same distance and in the same direction. 
It is a type of geometric transformation that preserves the distances and angles between any points or objects in the coordinate system, only specyfing a translation of the coordinate system. 
In constrast to map conersion, which involves changing the coordinate system, a rigid operation does not involve any conversion or distortion of the coordinate system. 

## North
Determining North seems to be one of the most important attributes of georeferencing. True North is not a constant, but a curve based on Northings and Eastings. On True North in IfcGeometricalRepresentationContext: 
> f not present, it defaults to 0. 1., meaning that the positive Y axis of the project coordinate system equals the geographic northing direction.

Isn't it dangerous to say: if True North is not available, True North == Grid North?

## Epoch
During the meeting with the Implementers Forum, it was mentioned that using an epoch is important. This refers to a specific point in time to which the coordinate system of a dataset is referenced. This reference is also mentioned in the EPSG database. To be added in the subtypes of IfcCoordinateReferenceSystem? 

# Software

## SketchUp
I've used the SketchUp IFC plugin (SketchUp-IFC-Manager) by Jan Brouwer: https://github.com/BIM-Tools/SketchUp-IFC-Manager. In SketchUp itself, longitude and langitude can be used and there are some external tools that can be used to transform between coordinate systems. However, when exporting to IFC I didn't encounter a possibility to also export georeferencing-related values. 

## ArcGIS
There is a tool to import the contents of one ore more IFC files into a geodatabase feature set. Additionally, there is a merge tool which seems to work only with files that are congruent with eacher other (for example, merging a map from Germany and the Netherlands) or maps from different years. The ability to merge maps of countries as large as the US, Canada and Mexico points to the possibilty to work with different coordinate systems. Until now, I haven't found how this works 'under the hood' and whether it can be used for IFC models. 
-> Each object has its own georeferencing. Additionaly, there is a project CRS has well
-> Has inbuild supported CRS systems
-> Georeferencing to IFC doesn't always seem to work (e.g., using Data Interoperability extension of ArcGIS Pro)


## Revit
- Moult: 'Revit is for vertical construction, to bringing coordinates back will lead to problems'. 
- Revit 2020 contains a bug: MapUnit is not used consistently (for example, sometimes foot are used instead of meters). This is fixed from 2021 onwards. 
- XAxisAbssicca and XaxisOrdinate are defined as the angle to True North / Derive North. 

## Blender(BlenderBIM)
- Sometimes, a model may mix Map Coordinates and Local engineering coordinates. For example, a surveyed pipe may have its placement use Map Coordinates with large Eastings and Northings. However, the placement of the site object may be still set at 0, 0, 0. Since this range of coordinates exceed the default 1km distance limit, this creates a problem. Blender needs to choose between displaying the pipe accurately and sacrificing precision at the site placement, or vice versa, but it is impossible to satisfy both simultaneously in the same Blender session.
- Used to create and merge IFC files with different coordinate systems, seems to work well (see 'Experiments')

# Testfiles
https://github.com/buildingSMART/IFC4.x-IF/tree/main/IFC-files/Georeferencing

- **COMPDCS(WKT) **-> https://github.com/buildingSMART/IFC4.x-IF/blob/main/IFC-files/Georeferencing/Georeferencing_COMPDCS(WKT)-RO.ifc 
- EPSG6174 is replaced by 5974. https://epsg.org/crs_6174/ETRS89-UTM-zone-34N-NN54-height.html?sessionkey=epgipcbfih Since it's a coordinate system from Norway, maybe Artur has more recent example files? -> Validate whether coordinate system used is up to date?
- EPSG6258 is a geodetic datum from Colombia (?)
- EPSG5776 -< NN54 height is replaced by NN2000 height (EPSG:5941)

- Is there any preference of using a WKT over ESPG codes?
- Would it be worth it or helpful to make a better differentiation between types of CRS (compound, projected, geogaphic)

# Experiments
Created two files with BlenderBIM. Both files contain a small UV sphere as a reference point
## File 1
- EPSG5678 -> DHPN / 3-degree Gauss-Krueger zone 4
- Geodetic Datum -> EPSG:6314 -> Deutsches Hauptdreiecksnetz (DHDN)
- Vertical Datum -> EPSG:1170 -> Deutsches Haupthoehenetz 2016 (DHHN2016) with Revision Date March 2023
- Based on Gauss-Kreuger Zone 4

Not sure whether correct, but I'm using UTM zone 33N for Leipzig:
- Scale factor for this zone is 0.9996
- False easting for zone 33N is 500000 meters 

### Convert
Based on this zone, northings and eastings are calculated with the pyproj module https://github.com/Ghesselink/georeferencing/blob/17ecb26bdbf6a294f957a04e80c2a7b7785576c4/convert_coordinates.py#L17
- Northings : 1828806
- Eastings : 5534444

## File 2
- ESPG: 5556 -> ESTR89
- Datums are again DHDN & DHHN2016
- Northings : 1828811 (+5 meters)
- Eastings : 5534449 (+ 5 meters)
- Back to lang-long(WSG84) would be 51.331496 - 12.352374


### Combine

The two files were combined with the blenderBIM 'IfcPatch'. https://blenderbim.org/docs-python/autoapi/ifcpatch/index.html
Afterwards, they were opened in BIMviewer software (e.g. Solibri, BIMviewer, blenderBIM).
In all programs, the two UV spheres of both files were visible, but georeferencing was not merged and still contained two instances MapConversions and two IFCProjectedCRS. In BlenderBIM, the georeferencing system of the first file was taken and used as references for the whole patched project.
There were no transformations of local coordinates from one coordinate reference system to another.
Is this expected behavior?

# Rules & Validation
## Checks
- In an area under 1km square, the same map converion can be used and the scale should remain the same (?)
- GlobalID should the the same for the same project across IFC files
- A check for correct use of coordinate reference systems. For example, in de EPSG documentation one can lookup whether a EPSG code refers to for a ProjectedCRS, CompoundCRS, VerticalDatumCRS etc. If this is incorrect, it could lead to incorrect coordinate transformations or related problems.
- Use the same unit for length or distance in the whole georeferencing system (e.g. millimeters, metres or inches). 
## Best Practices
- Check for incorrect coordinate use. A first option is to check for values that numerically don't make sense. A more elegant option would be to (1) make a list of 'very unlikely' points, for example by coordinates that are in located entirely in the ocean, or (2) check for coordinates that don't make sense within a certain coordinate systems. This last two options would require a small database. 
- Check whether coordinate system has a recent version
- A name of a CRS (such as 'MGA56' or 'GDA/MGA56') is used instead of a EPSG number. 
- Check for georeferencing in IFC2x3, for example in propertySets (is this possible?)
- EPSG code found only on epsg.io, not in official epsg.org

## Ideas related to georeferencing
### Tracking georeferencing history
Performing spatial analysis, such as identifying boundaries which require surface level queries, is impossible as a result. Additionally, tracking histories is challenging because accessibility can only be controlled at the file level and not at the object-level.

However, history is crucial once the physical construction of the building has already commenced, and objects must be accurately located. Georeferencing could be a useful tool for this purpose. One possible solution could be to include an optional field for **'Last date of conversion,'** which must have a value that is more recent than the current value.
