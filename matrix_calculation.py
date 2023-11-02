import numpy as np

# Function to add two matrices

def add_matrices(matrix1, matrix2):
    return np.add(matrix1, matrix2)

# Function to subtract two matrices

def subtract_matrices(matrix1, matrix2):
    return np.subtract(matrix1, matrix2)

# Function to multiply two matrices

def multiply_matrices(matrix1, matrix2):
    return np.dot(matrix1, matrix2)

# Example usage

matrix1 = np.array([[1, 2], [3, 4]])
matrix2 = np.array([[5, 6], [7, 8]])

print('Matrix 1:')
print(matrix1)

print('Matrix 2:')
print(matrix2)

print('Addition:')
print(add_matrices(matrix1, matrix2))

print('Subtraction:')
print(subtract_matrices(matrix1, matrix2))

print('Multiplication:')
print(multiply_matrices(matrix1, matrix2))
