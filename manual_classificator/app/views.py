from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.conf import settings

from os.path import join
import os

def get_metadata(selected):
	label = []
	file_paths = []

	#Pegar pastas dentro de ./camera
	for folder in os.listdir(settings.PROJECT_PATH_MEDIA):
		if selected != folder:
			continue
		if os.path.isdir(join(settings.PROJECT_PATH_MEDIA, folder)):
			## Pegar todos arquivos da pasta
			for root, dirs, files in os.walk(os.path.abspath(join(settings.PROJECT_PATH_MEDIA, folder))):
				for file in files:
					file_paths.append(os.path.join(root, file).replace(settings.PROJECT_PATH_MEDIA, ""))
					label.append(str(folder))
	  
	return label, file_paths


class IdentClassifier:
	def __init__(self, user, path):
		self.count = 0
		self.classified = {}

		self.media = settings.PROJECT_PATH_MEDIA
		self.user = user
		self.path = path

		try:
			self.load_state()
		except:
			self.save_state()

		self.load_images()

	def load_images(self):
		_, self.files = get_metadata(self.path)
		
	def get_current(self):
		while self.files[self.count] in self.classified:
			self.count += 1


		file = self.files[self.count]
		return file

	def classify(self, classi, file):
		self.classified[file] = classi

	def save_state(self):
		file = open(join(self.media, self.user + '_class.txt'), 'w')
		for i in self.classified:
			file.write(f'{i} {self.classified[i]}\n')

		file.close()

	def load_state(self):
		file = open(join(self.media, self.user + '_class.txt'), 'r')
		for i in file.readlines():

			name = i.split(' ')[0]
			classi = i.split(' ')[1].replace("\n", "")

			self.classified[name] = classi

	def get_count(self):
		return self.count




users = {}


# Create your views here.
def home(request):
	return render(request, 'app/index.html')



@api_view(['POST'])
def start(request):
	print(request.data['path'], request.data['user'])
	user = request.data['user']

	users[user] = IdentClassifier(user, request.data['path'])
	cur = users[user].get_current()
	print(cur)

	return Response({'count': users[user].get_count(), 'cur': cur})


@api_view(['POST'])
def classify(request):
	user = request.data['user']

	cl = request.data['class']
	file = request.data['file']

	users[user].classify(cl, file)
	users[user].save_state()

	cur = users[user].get_current()
	return Response({'count': users[user].get_count(), 'cur': cur})
