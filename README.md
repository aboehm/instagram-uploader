# Instagram Media Uploader

Upload media file to instagram. Currently only pictures are supported.

## Help

```
usage: instagram-uploader.py [-h] [--comment [COMMENT]] [--media MEDIA]
                             [--force] [--username USERNAME]
                             [--password PASSWORD] [--save-userpass]
                             [--verbose]

Instagram Media Uploader

optional arguments:
  -h, --help            show this help message and exit
  --comment [COMMENT], -c [COMMENT]
                        Comment of picture
  --media MEDIA, -m MEDIA
                        Path to picture file to upload
  --force, -f           Don't ask for confirmation
  --username USERNAME, -u USERNAME
                        Username
  --password PASSWORD, -p PASSWORD
                        Password
  --save-userpass, -s   Store given user credentials and exit (username and
                        password needed)
  --verbose, -v         Say what's going on
```

## Upload media

Upload *MEDIAFILE* to account *ACCOUNT* with password *SECRET* with description "#tag1 #tag2 some words":

```
instagram-uploader.py
	--username ACCOUNT
	--password SECRET
	--media MEDIAFILE
	--comment '#tag1 #tag2 some words'
```

## Setting default credentials

Set default user-login for account *ACCOUT* with password *SECRET*:

```
instagram-uploader.py --username ACCOUNT --password SECRET --save-user-pass
```

**Warning**: The data will be saved in clear text and will be save in the home directory under *~/.instagram-uploader/settings*.

