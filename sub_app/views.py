from django.shortcuts import render
from .models import image_classification
from django.http import HttpResponseRedirect
from .py_templates.my_model import image_pred
from PIL import Image
import requests
import numpy as np

dis={0:'Basal Cell Carcinoma (BCC)',1:'Actinic Keratosis (ACK)',2:'Nevus (NEV)',
3:'Seborrheic Keratosis (SEK)',4:'Squamous Cell Carcinoma (SCC)	',5:'Melanoma (MEL)'}



def home(request):
	
	print('here u go')
	images=image_classification.objects.all()
	try:
		url=images[len(images)-1].pic.url
		print('url is',url)
		out=image_pred(url)
		out=dis[int(out)]
		return render(request,'home.html',{'pred':out,'url':url})
	except FileNotFoundError:
		return render(request,'home.html',{'pred':'no image'})





def uploadImage(request):
	print('image handling')
	img=request.FILES['image']
	image=image_classification(pic=img)
	image.save()
	return HttpResponseRedirect('/')
	#return render(request,'home.html')

def uploadURL(request):
	#file_name='image{}.jpg'.format(np.random.randint())
	print('image is uploaded using url')
	url=request.POST.get('imgurls')
	print(url)
	# img=Image.open(urllib2.urlopen(url))
	# img=Image.open(requests.get(url, stream=True).raw)
	imgurl=requests.get(url, stream=True).raw
	print('new url',imgurl)
	out=image_pred(imgurl)
	print(out)
	out=dis[int(out)]
	#img.save(file_name)
	return render(request,'home.html',{'pred':out,'url':url})
