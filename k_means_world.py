import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing

#PLOT 3D GRAPH
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for index in range(len(df)):
# 	ax.scatter(df['lat'][index], df['lng'][index], df['population'][index], marker='o')
# plt.show()

class K_Means:
	def __init__(self, k=20, max_iterations=10, tolerance=0.001):
		self.k = k
		self.max_iterations = max_iterations
		self.tolerance = tolerance

	def fit(self, data_set):
		self.centroids = {}
		for i in range(self.k):
			#set first k data sets cordinates as initial centroids
			self.centroids[i] = data_set[i]

		current_iteration = 1
		for i in range(self.max_iterations):
			print("Iteration {} of {} ".format(current_iteration, self.max_iterations))
			current_iteration = current_iteration+1
			self.classifications = {}
			#classifications[centroid] = data_set[cordinate_x, cordinate_y]
			#classifications of data_set(x,y) is some centroid

			for j in range(self.k):
				self.classifications[j] = []

			for cordinates in data_set:
				distances = []
				for centroid in self.centroids:
					#get distances of all cordinates from the current centroids
					distances.append(np.linalg.norm(cordinates-self.centroids[centroid]))

				#get minimum distance from the centroid and assign it to that centroid classification
				classification = distances.index(min(distances))
				self.classifications[classification].append(cordinates)

			prev_centroid = dict(self.centroids)
			# print(self.centroids)
			for classification in self.classifications:
				#get average of the cordinates (dataset) in current classification to determine centroid movement
				self.centroids[classification] = np.average(self.classifications[classification], axis=0)
			optimized = True

			for c in self.centroids:
				orginal_centroid = prev_centroid[c]
				current_centroid = self.centroids[c]

				#find if centroid has moved or not, if not it is optimized
				if sum((current_centroid- orginal_centroid)/orginal_centroid*100.0) > self.tolerance:
					optimized = False
			if optimized:
				# print("Final centroids")
				# print(self.centroids)
				break
		# print(self.classifications)
		# print(self.centroids)

	def predict(self, predict_set):
		predictions = {}
		predictions[0] = []
		predictions[1] = []
		for cordinates in predict_set:
			distances = []
			for centroid in self.centroids:
				distances.append(np.linalg.norm(cordinates-self.centroids[centroid]))
			classification = distances.index(min(distances))
			predictions[classification].append(cordinates)
		return predictions

	def plot(self):
		i = 1
		colors = ['r','g','b','c','k','y','m','r','g','b','c','k','y','m','r','g','b','c','k','y','m','r','g','b','c','k','y','m']
		for key, value in self.classifications.items():
			for cordinates in value:
				print('plotting point no. : {} '.format(i))
				i = i+1
				plt.scatter(cordinates[0], cordinates[1], c=colors[key])

		for i in range(self.k):
			plt.scatter(self.centroids[i][0], self.centroids[i][1], c=colors[i], marker='*')
			plt.text(self.centroids[i][0], self.centroids[i][1], 'centroid')
		# for key, value in predicted_cluster.items():
		# 	for cordinates in value:
		# 		plt.scatter(cordinates[0], cordinates[1], c=colors[key], marker='*')
		# 		plt.text(cordinates[0], cordinates[1], 'predicted cluster')
		plt.show()

	def plot3D(self):
		i = 1
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		colors = ['r','g','b','c','k','y','m']
		for key, value in self.classifications.items():
			for cordinates in value:
				print('plotting point no. : {}'.format(i))
				i = i+1
				ax.scatter(cordinates[0], cordinates[1], cordinates[2], c=colors[key])
		print('Plot completed.')

		for i in range(self.k):
			ax.scatter(self.centroids[i][0], self.centroids[i][1], self.centroids[i][2], c=colors[i], marker='*')
			ax.text(self.centroids[i][0], self.centroids[i][1], self.centroids[i][2], 'centroid')
		# for key, value in predicted_cluster.items():
		# 	for cordinates in value:
		# 		plt.scatter(cordinates[0], cordinates[1], c=colors[key], marker='*')
		# 		plt.text(cordinates[0], cordinates[1], 'predicted cluster')
		plt.show()


df = pd.read_excel('worldcities.xlsx')
df.drop(['city','city_ascii','country','iso2','iso3','admin_name','capital','id'], 1, inplace=True)
print(len(df)) #Print total rows
print(df.isnull().sum(axis = 0)) #print out total empty values in each column
df.dropna(subset = ['population'] ,inplace=True) #drop rows where population is 0
df = df[['lng','lat']]
X = np.array(df)

km = K_Means()
print('fit started')
km.fit(X)
print('fit done')
print('Plotting started ...')
# km.plot3D()
km.plot()