import pyproj
import numpy as np
from pandas import DataFrame

wsg84 = pyproj.CRS('EPSG:4326')
utm = pyproj.CRS('EPSG:32632')

lon = 12.352347
lat = 51.331455

transformer = pyproj.Transformer.from_crs(wsg84, utm)

eastings, northings = transformer.transform(lon, lat)

easting_pt2, northing2_pt2 = eastings+5, northings+5

lon_2, lat_2 = pyproj.Transformer.from_crs(utm, wsg84).transform(easting_pt2, northing2_pt2)

print('original lon, lat ', lon, lat)
print('eastings, northings pt 1 ', int(eastings), int(northings))
print('easting, northings pt 2 ', int(easting_pt2), int(northing2_pt2))
print('pt 2 lon, lat ', lon_2, lat_2)
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import pyproj
# from mpl_toolkits.basemap import Basemap

# fig, ax = plt.subplots(figsize=(6, 6))
# m = Basemap(projection='merc',
#               urcrnrlat=lat, llcrnrlat=lat_2,
#               urcrnrlon=lon, llcrnrlon=lon_2,
#               resolution='i',
#               suppress_ticks=False,
#               ax=ax)
# m.fillcontinents()
# m.drawcoastlines()
# m.ax = ax
# pt = m.plot(eastings, northings, 'ko', latlon=True)

# lons, lats, xs, ys = m.makegrid(200, 200, returnxy=True)

# gc = pyproj.Geod(a=m.rmajor, b=m.rminor)

# distances = np.zeros(lons.size)

# for k, (lo, la) in enumerate(zip(lons.flatten(), lats.flatten())):
#     _, _, distances[k] = gc.inv(eastings, northings, lo, la)
    
# distances = distances.reshape(200, 200)  # In km.

# # Plot perimeters of equal distance.
# levels = [1000]  # [50, 100, 150]
# cs = m.contour(xs, ys, distances, levels, colors='r')