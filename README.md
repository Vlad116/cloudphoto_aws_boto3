# cloudphoto_aws_boto3

### Application commands 

* Upload photos to cloud storage: cloudphoto upload -p path -a album

Sends all photos (without recursion) from the path directory to the cloud storage and binds them to the album album. If the album does not exist, it creates a new album. If the directory does not exist, then it gives a corresponding error.

* Download photos to computer: cloudphoto download -p path -a album

Downloads from cloud storage all photos to path that are related to album. If the album or catalog does not exist, then it gives a corresponding error.

* View album list: cloudphoto list

Lists the albums that are present in the cloud storage.

* View a list of photos in an album: cloudphoto list -a album

Lists photos that belong to the album album.

For this application, a photograph is a file whose name, regardless of case, ends in:
· ".Jpg"
· ".Jpeg"
· ".Png"

### Before using

pip install click
pip install virtualenv --user
virtualenv env

$ . venv/bin/activate
If you are a Windows user, the following command is for you:
$ venv\scripts\activate
And if you want to go back to the real world, use the following command:
$ deactivate

- Set environment variables in the console open as administrator
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_BUCKET_NAME

in Windows:

* C:\> setx AWS_ACCESS_KEY_ID ACCES_KEY_ID
* C:\> setx AWS_SECRET_ACCESS_KEY SECRET
* C:\> setx AWS_DEFAULT_REGION eu-north-1
* C:\> setx AWS_BUCKET_NAME bucket_name (if the bucket was created)

in AWS cli:

* aws configure 

if the bucket was not created initially:

* aws s3api create-bucket --bucket bucket_name --region region

in the project directory:

* python setup.py develop

Run commands as in  "Application commands" readme section.
