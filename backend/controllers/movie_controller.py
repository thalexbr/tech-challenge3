from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from backend.config.security import get_current_user, TokenData
from fastapi.security import OAuth2PasswordBearer
import requests
import pandas as pd
import numpy as np
import os

router = APIRouter(prefix="/api/v1")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.get('/movies')
def getMovies(authorization: TokenData = Depends(get_current_user)):
    options = {'encoding':'UTF-8','sep':';', 'header':0, 'index_col':False, 'engine': 'python'}
    data = pd.read_csv('backend/data/data.csv',**options)
    for key in data.keys() :
        data[key] = np.where(pd.isna(data[key]),'',data[key])

    data_head = data.head(1000000)
    return data_head

@router.get('/movies/image')
def getMovies(movieId):

    file_path = f'backend/data/{movieId}.jpg'
    if(os.path.exists(file_path)):
        return FileResponse(file_path, media_type='image/jpeg', filename=os.path.basename(file_path))
    else:

        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

        url = f'https://www.imdb.com/title/{movieId}/'

        # Send a GET request to the webpage
        response = requests.get(url,headers=headers)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')
        for img in img_tags:
            if(img.get('width') == '190'):
                img_url = img.get('src')
                download_image(img_url,file_path)
                return FileResponse(file_path, media_type='image/jpeg', filename=os.path.basename(file_path))

    file_path = 'backend/data/notfound.jpg'

    return FileResponse(file_path, media_type='image/jpeg', filename=os.path.basename(file_path))

def download_image(url, file_path):
    """
    Downloads an image from the specified URL and saves it to the given file path.

    :param url: URL of the image
    :param file_path: Path to save the downloaded image file
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f'Image successfully downloaded: {file_path}')
    else:
        print(f'Failed to download image. HTTP Status code: {response.status_code}')



    