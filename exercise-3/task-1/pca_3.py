import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load trajectory data with space as delimiter
data = np.loadtxt('../data/data_DMAP_PCA_vadere.txt', delimiter=' ')

# Extract positions of the first two pedestrians
pedestrian1 = data[:, :2]
pedestrian2 = data[:, 2:4]

# Visualize trajectories of the first two pedestrians in the original 2D space
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(pedestrian1[:, 0], pedestrian1[:, 1], label='Pedestrian 1')
plt.plot(pedestrian2[:, 0], pedestrian2[:, 1], label='Pedestrian 2')
plt.title('Trajectories in Original 2D Space')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()

# Apply PCA to project the 30-dimensional data to the first two principal components
pca = PCA(n_components=2)
projected_data = pca.fit_transform(data)

# Visualize trajectories of the first two pedestrians in the 2D space defined by the first two principal components
plt.subplot(1, 2, 2)
plt.plot(projected_data[:, 0], projected_data[:, 1], label='Pedestrians')
plt.title('Trajectories in PCA Space')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()

plt.show()

# Analyze the energy captured by the first two principal components
explained_variance_ratio = pca.explained_variance_ratio_
total_energy = np.sum(explained_variance_ratio)
print(f'Total energy captured by the first two components: {total_energy * 100:.2f}%')

# Determine how many components are needed to capture most of the energy (>90%)
cumulative_energy = np.cumsum(explained_variance_ratio)
num_components_needed = np.argmax(cumulative_energy >= 0.9) + 1
print(f'Number of components needed to capture >90% energy: {num_components_needed}')
