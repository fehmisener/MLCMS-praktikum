import numpy as np
import matplotlib.pyplot as plt
from skimage import transform
import imageio

# Load the image and convert it to grayscale
original_image = imageio.imread('raccoon.jpeg', pilmode='L')
# Rescale the image to have size (249 × 185)
rescaled_image = transform.resize(original_image, (185, 249))

# Flatten the image to treat columns as data points
flattened_image = rescaled_image.reshape((-1,))

# Center the data by subtracting the mean
mean_image = np.mean(flattened_image)
centered_image = flattened_image - mean_image

# Perform Singular Value Decomposition (SVD)
U, S, Vt = np.linalg.svd(centered_image.reshape(rescaled_image.shape), full_matrices=False)

# Visualization of reconstructions
num_components_to_visualize = [len(S), 120, 50, 10]

for num_components in num_components_to_visualize:
    # Truncate singular values
    S_truncated = np.copy(S)
    S_truncated[num_components:] = 0

    # Reconstruct the image
    reconstructed_image = np.dot(U, np.dot(np.diag(S_truncated), Vt))

    # Add back the mean
    reconstructed_image += mean_image

    # Display the reconstructed image
    plt.imshow(reconstructed_image, cmap='gray')
    plt.title(f'Reconstructed Image with {num_components} Principal Components')
    plt.show()

    # Calculate the energy loss
    energy_loss = 1 - np.sum(S_truncated**2) / np.sum(S**2)
    print(f'Energy loss with {num_components} principal components: {energy_loss * 100:.2f}%')

    # Check for energy loss smaller than 1%
    if energy_loss < 0.01:
        print(f'The energy loss with {num_components} principal components is smaller than 1%.')
