import gmplot

gmap = gmplot.GoogleMapPlotter(57.7, 11.9, 16)

y = ['item1', 'item2']  # list of strings
xdata = [57.7, 11.9]  # list of numbers
ADAM = list(zip(xdata))

gmap.scatter(ADAM[0], ADAM[1], 'k', size=40, marker=True)
# lats = get_latitudes(apartment_list)
# longs = get_longitudes(apartment_list)
# print(longs[0])
# gmap.plot(lats, longs, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(lats, longs, 'k', marker=True)

gmap.heatmap(ADAM[0], ADAM[1])

gmap.draw("mymap.html")