import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster

# Load the CSV data
try:
    data = pd.read_csv('lcsd_wd_en.csv')
except FileNotFoundError:
    print("Error: CSV file not found. Please check the file path.")
    exit()

# Print column names to check what's available
print("Available columns:")
print(data.columns)

# Check if required columns exist
required_columns = ['Latitude', 'Longitude']
if not all(col in data.columns for col in required_columns):
    print("Error: Required columns (Latitude, Longitude) not found in the CSV file.")
    exit()

# Extract latitude and longitude
latitudes = data['Latitude']
longitudes = data['Longitude']

# Create a scatter plot using matplotlib
plt.figure(figsize=(10, 8))
plt.scatter(longitudes, latitudes, c='blue', marker='o', alpha=0.5)
plt.title('Locations of Water Dispensers')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.tight_layout()
plt.savefig('water_dispenser_locations.png')
plt.close()

# Create a map using folium
m = folium.Map(location=[22.3527242, 114.1394], zoom_start=11)

# Add markers for each water dispenser
marker_cluster = MarkerCluster().add_to(m)

for idx, row in data.iterrows():
    popup_text = f"Location {idx+1}"
    tooltip_text = f"Location {idx+1}"
    
    # If 'Name' column exists, use it for popup
    if 'Name' in data.columns:
        popup_text = row['Name']
    
    # If 'District' column exists, use it for tooltip
    if 'District' in data.columns:
        tooltip_text = row['District']
    
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_text,
        tooltip=tooltip_text,
    ).add_to(marker_cluster)

# Add a marker for Saro
folium.Marker(
    location=[22.3050684, 114.1790019],
    tooltip="Click me!",
    popup="PolyU School of Design",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

# Save the map
m.save('water_dispenser_map.html')

print("Matplotlib plot saved as 'water_dispenser_locations.png'")
print("Folium map saved as 'water_dispenser_map.html'")