import matplotlib.pyplot as plt
import json

word = "hola"

# open the data
with open('collectedData/allGraphs.json', 'r') as file:
    data = json.load(file)[word]

data = sorted(data, key=lambda point: point[0])

# Extract x and y values from the data
x_values = [point[0] for point in data]
y_values = [point[1] for point in data]

# Plot the data as a line plot
plt.plot(x_values, y_values)

# Add labels and title
plt.xlabel('Months after 1990')
plt.ylabel('Word Frequency')
plt.title('Usage of "' + word + '" over time in French rap lyrics')

# Display the plot
plt.show()
