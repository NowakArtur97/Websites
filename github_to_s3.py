
import os
import urllib.request
from urllib.parse import urlparse
import json
import boto3

print('Loading function')

s3 = boto3.resource('s3')

urls = [
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/index.html",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/about.html",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/contact.html",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/style.css",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/simple-house-logo.png",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/simple-house-01.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/about-01.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/about-02.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/about-03.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/about-04.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/about-05.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/about-06.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/dummy-img.png",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/img-01.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/gallery/01.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/gallery/02.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/gallery/03.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/gallery/04.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/gallery/05.jpg",
"https://raw.githubusercontent.com/NowakArtur97/Simple-House/master/img/gallery/06.jpg",
]

def resolve_content_type(extension):
    if extension == "html":
        return "text/html"
    elif extension == "css":
        return "text/css"
    elif extension == "png":
        return "image/png"
    else:
        return "image/jpeg"

def map_to_resource(url):
    extension = url.rsplit('.', 1)[1]
    return GithubResource(url, resolve_content_type(extension))

def save_to_local(resource):
    url = resource.url
    urlPath = urlparse(url).path
    fileName = os.path.basename(urlPath)
    filePath = '/tmp/' + fileName
    urllib.request.urlretrieve(url, filePath)
    return filePath

def resolve_key(url, fileName):
    if "/img/gallery/" in url:
        return "img/gallery/" + fileName
    elif "/img/" in url:
        return "img/" + fileName
    else:
        return fileName

def upload_to_s3(resource, filePath, bucket):
    fileName = os.path.basename(filePath)
    key = resolve_key(resource.url, fileName)
    s3.Object(bucket, key).put(Body=open(filePath, 'rb'), ContentType=resource.extension)

def copy_to_s3(resource, bucket):
    filePath = save_to_local(resource)
    upload_to_s3(resource, filePath, bucket)

def lambda_handler(event, context):
    bucket = "simple-house-687fffc0"
    resources = map(map_to_resource, urls)

    try:
        for resource in resources:
            copy_to_s3(resource, bucket)

    except Exception as e:
        print("Exception on copy")
        print(e)
        return

class GithubResource:
  def __init__(self, url, extension):
    self.url = url
    self.extension = extension