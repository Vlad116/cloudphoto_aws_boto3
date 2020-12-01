import logging
import requests
import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import botocore

# Get environment variables
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_LOCATION = os.environ.get('AWS_DEFAULT_REGION')
BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

# create a resource instance
s3 = boto3.resource('s3')

s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

def init_db():
    key = 'db.json'

    try:
        s3.Object(BUCKET_NAME, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            return {}
        else:
            # Something else has gone wrong.
            raise
    else:
        obj = s3.Object(BUCKET_NAME,key)
        db = json.load(obj.get()['Body'])
        return db

def out_error(text):
    print("\033[31m {}" .format(text))

# cloudphoto upload -p C:\Users\vlada\Desktop\aws_test\first -a de
def upload_album(path, album_name):
    if os.path.exists(path):
        if os.path.isdir(path):
            print('uploading...')

            extensions = tuple(['.jpg', '.jpeg', '.png'])

            # res = []
            # res += [f for f in os.listdir(path) if f.endswith(extensions)]

            files_list = [
                x for x in os.listdir(path) if (
                        not x.startswith(".") and
                        os.path.isfile(os.path.join(path, x))
                        and x.endswith(extensions))
            ]

            objects_list = []

            for file in files_list:
                print(file.rsplit('.',1))
                object_name = file.rsplit('.',1)[0] + '_' + album_name + '.' + file.rsplit('.',1)[1]
                objects_list.append(object_name.lower())

            db = init_db()
            print(db)

            albumExist = album_name in db

            if (albumExist != True):
                db[album_name] = {}

            # loop through the desired source files
            for file in files_list:
                # get source file path
                src_path = os.path.join(path, file)
                object_name = objects_list[files_list.index(file)]

                if (object_name in db[album_name]) != True:
                    file_stats = os.stat(src_path)
                    print(f'File Size in KiloBytes is {file_stats.st_size / (1024)}')
                    db[album_name][object_name] = file_stats.st_size / (1024)

                    try:
                        s3_client.upload_file(src_path, BUCKET_NAME, object_name, ExtraArgs={'ACL': 'public-read'})
                    except ClientError as e:
                        logging.error(e)
                        return False
                    # return True
                    print('Uploaded', file, 'with URL:')

                    # get the url of the uploaded file. Prepare (Encode) it if necessary
                    #     BUCKET_LOCATION, BUCKET_NAME, dest_path)
                    object_url = "https://{0}.s3.{1}.amazonaws.com/{2}".format(
                        BUCKET_NAME, BUCKET_LOCATION, object_name)
                    print(object_url)
                    print(requests.Request('GET', object_url).prepare().url)
                    print('=' * 30)
                else:
                    print(object_name + ' уже был загружен в альбом')
                    print('=' * 30)

            with open('db.json', 'w') as json_file:
                json.dump(db, json_file)
            try:
                s3_client.upload_file('db.json', BUCKET_NAME, 'db.json', ExtraArgs={'ACL': 'public-read'})
            except ClientError as e:
                logging.error(e)
                return False
        else:
            print("Указанный параметр -p не является директорией")
    else:
        print("Обьекта файловой системы по указанному пути - не существует! Введите верный путь в директории")
    return

# cloudphoto download -p C:\Users\vlada\Desktop\aws_test -a de
def download_album(path, album_name):
    if os.path.exists(path):
        if os.path.isdir(path):
            db = init_db()

            if (album_name in db):
                print('Downloading ' + album_name + ' ...')
                s3_object_keys = db[album_name].keys()

                for KEY in s3_object_keys:
                    dest_path = os.path.join(path, KEY)
                    try:
                        s3.Bucket(BUCKET_NAME).download_file(KEY, dest_path)
                    except botocore.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == "404":
                            print("The object does not exist!.")
                        else:
                            raise
            else:
                print('Указанного альбома не существует')
        else:
            print("Указанный параметр -p не является директорией")
    else:
        print("Указанный параметр -p не является директорией")
    return

# cloudphoto list
def list_albums():
    print("List - all album's\n")

    db = init_db()
    isNotEmpty = any(db)

    if(isNotEmpty):
        albums = db.values()
        print(f'Количество загруженных альбомов: {len(albums)}\n')
        for album in albums:
            print(album)
    else:
        print("Нет загруженных альбомов!")
    return

#cloudphoto list -a album
def list_album(album_name):
    print("List - all photos in " + album_name +'\n')

    db = init_db()
    isNotEmpty = any(db)

    if (isNotEmpty):
        if(album_name in db):
            photos = db[album_name].keys()
            print(f'Количество фотографий в альбоме: {len(photos)}\n')
            for photo in photos:
                print(f'{photo} in {album_name} : {db[album_name][photo]}')
        else:
            print("Указанного альбома не существует!")
    else:
        print("Нет загруженны альбомов!")
    return