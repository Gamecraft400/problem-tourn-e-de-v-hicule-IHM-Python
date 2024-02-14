from docplex.mp.model import Model
import numpy as np

# Read VRP instance data from file
file_path = 'c50.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()

num_customers, best_known_solution = map(int, [round(float(value)) for value in lines[0].split()])
capacity = int(float(lines[1]))
depot_location = tuple(map(int, lines[2].split()))

customer_data = [tuple(map(int, line.split())) for line in lines[3:]]

# Parsing demands from the file
customer_demands = [int(line.split()[3]) for line in lines[3:]]

# Save the customer demands to a file with proper formatting
output_demands_path = 'customer_demands.txt'

with open(output_demands_path, 'w') as output_file:
    output_file.write("[")
    output_file.write(", ".join(map(str, customer_demands)))
    output_file.write("]")

# Add the depot coordinates to the list of customers
depot_coords = (30, 40)
customer_coords = [depot_coords] + customer_data

# Calculate the distance matrix
num_points = len(customer_coords)
distance_matrix = np.zeros((num_points, num_points))

for i in range(num_points):
    for j in range(num_points):
        distance_matrix[i, j] = round(np.sqrt(
            (customer_coords[i][0] - customer_coords[j][0]) ** 2 +
            (customer_coords[i][1] - customer_coords[j][1]) ** 2
        ), 1)

# Print the distance matrix
print(distance_matrix)

# Specify the file path to save the distance matrix
output_file_path = 'distance_matrix.txt'

with open(output_file_path, 'w') as output_file:
    output_file.write("[")
    for row in distance_matrix:
        output_file.write("[")
        output_file.write(", ".join(map(str, row)))
        output_file.write("],\n")
    output_file.write("]")

print(f'Distance matrix saved to: {output_file_path}')

