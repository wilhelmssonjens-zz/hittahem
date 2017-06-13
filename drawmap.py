import gmplot

#gmap = gmplot.GoogleMapPlotter(57.7, 11.9, 16)
#gmap.scatter(ADAM[0], ADAM[1], 'k', size=40, marker=True)
# lats = get_latitudes(apartment_list)
# longs = get_longitudes(apartment_list)
# print(longs[0])
# gmap.plot(lats, longs, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(lats, longs, 'k', marker=True)

#gmap.heatmap(ADAM[0], ADAM[1])
#gmap.draw("mymap.html")

def scatter_apts(gmap, apartment_list):

    for apt in apartment_list:
        long = apt.location.longitude
        lat = apt.location.latitude
        tmp = list(zip([int(float(lat)* 10**5)/(10**5), int(float(long)*10**5)/(10**5)]))
        gmap.scatter(tmp[0], tmp[1], 'k', size=40, marker=True)

    return gmap