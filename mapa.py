import folium

# Create a folium map centered on the given latitude and longitude
m = folium.Map(location=[19.048500, -98.216300], zoom_start=13)

# Add a marker to the map
folium.Marker([19.048500, -98.216300]).add_to(m)
folium.Marker([19.048700, -98.216300]).add_to(m)




# Save the map to an HTML file
m.save('map.html')