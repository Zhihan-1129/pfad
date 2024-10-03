import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import dotenv
import os
from matplotlib.animation import FuncAnimation

# Load the Environment Variables
dotenv.load_dotenv('F:\SD5913 Creative Programming\Git_Code\pfad\Assignment_1_9.25\.env')

# Get URL
apikey = os.getenv('api_key') # This api is valid for 14 days from 2024.9.24
url =  os.getenv('URL')

# Access to Air Quality Data
response = requests.get(url)
airdata = json.loads(response.text)

# Extract Top 20 City Names and AQIs
cities = []
aqis = []
for citydata in airdata['results'][:20]: 
    cityname = citydata['location']['name']
    path = citydata['location'].get('path', '')
    splitpath = path.split(',')
    path = splitpath[2].strip() if len(splitpath) > 2 else '' 
    aqi = citydata['aqi']

    citylabel = f"{cityname}, {path}" if path else cityname
    
    cities.append(citylabel)
    aqis.append(float(aqi))  


# Change the Color
colors = []

# First 15 Cities Coloured Green
cmap_green = plt.get_cmap("Greens")
for i in range(15):
    colors.append(cmap_green(i / 15))

# Last 5 Cities Coloured Orange
cmap_orange = plt.get_cmap("Oranges")
for i in range(5):
    colors.append(cmap_orange(0.5 + i / 10)) 

assert len(colors) == len(cities)

# Change the Font
plt.rcParams['font.family'] = 'Calibri'

plt.figure(figsize=(12, 8))
bars = plt.barh(cities, aqis, color=colors, edgecolor='#405507')

# Change Border Colour
ax = plt.gca()
ax.spines['top'].set_color('#405507')
ax.spines['bottom'].set_color('#405507')
ax.spines['left'].set_color('#405507')
ax.spines['right'].set_color('#405507')

# Change Border Thickness
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)

# Change Background Color
ax.set_facecolor('#f8fff5')

# Label the Data
plt.xlabel('Air Quality Index (The AQI is higher, the worse the air quality is) ', weight='bold', fontsize=16, color='#37570d')
plt.title('Top 20 Cities in China Ranked by AQI ', fontsize=18, weight='bold', color='#37570d')
plt.gca().invert_yaxis()  # Invert the Y-axis so that the AQI is displayed from high to low

# Add gridlines to the Chart
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Change X-axis and Y-axis Label Colors and Font Sizes
plt.xticks(fontsize=13, color='#37570d')
plt.yticks(fontsize=13, color='#37570d')

# Define Animation Function
def update(frame):
    for i, bar in enumerate(bars):
        bar.set_width(aqis[i] * frame / 20)  

    # Display AQI Value at Last Frame
    if frame == 20:
        for index, value in enumerate(aqis):
            plt.text(value + 0.3, index, str(value), va='center', ha='left', fontsize=13, color='#37570d')

# Create an animation
ani = FuncAnimation(plt.gcf(), update, frames=np.arange(1, 21), interval=100, repeat=False)

# Show Chart
plt.tight_layout()
plt.show()
