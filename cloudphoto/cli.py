import click
from cloudphoto.functions import upload_album, download_album, list_albums, list_album

# cloudphoto [OPTIONS] (env, заранее добавить в переменн. окр. os) COMMAND [ARGS] (-p - path, -a - album_name)
@click.group()
def main():
    print("======================================================")

@main.command()
@click.option('-p', help='path to dir, from which the photos will be uploaded')
@click.option('-a', help='album name')
def upload(p, a):
    if (p is not None) & (a is not None):
        upload_album(p,a.lower())
    else:
        click.echo("ERROR",color='red')
        click.echo("You need input -a TEXT && -p TEXT option's")
        click.echo("Input -a album_name and -p path , and try again!")

@main.command()
@click.option('-p', help='path to dir, from which the photos (with album name) will be downloaded')
@click.option('-a', help='album name')
def download(p, a):
    if (p is not None) & (a is not None):
        download_album(p,a.lower())
    else:
        click.echo("ERROR",color='red')
        click.echo("You need input -a TEXT && -p TEXT option's")
        click.echo("Input -a album_name and -p path , and try again!")

@main.command()
@click.option('-a', help='album name, if call with album name option, show all photo in album')
def list(a):
    if a is not None:
        # выводим фотографии в альбоме
        list_album(a.lower())
    else:
        # выводим список альбомов
        list_albums()

def start():
    main()

if __name__ == "__main__":
    start()