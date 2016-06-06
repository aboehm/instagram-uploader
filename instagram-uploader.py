#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: sts=4 ts=4 noet :

# The MIT License (MIT)
# 
# Copyright (c) 2016 Alexander Böhm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from instagram import InstagramSession
import sys, os, json, argparse, traceback

def get_user_dir():
	return os.path.join(os.environ['HOME'], '.instagram-uploader')

def get_settings_path():
	return os.path.join(get_user_dir(), 'settings')

def get_settings():
	try:
		f = open(get_settings_path())
		d = f.read()
		f.close()
		return json.loads(d)
	except:
		return None

def get_username():
	s = get_settings()
	if s == None:
		return None
	else:
		return get_settings()['username']

def get_password():
	s = get_settings()
	if s == None:
		return None
	else:
		return get_settings()['password']

def create_if_not_exists_user_dir():
	try:
		os.stat(get_user_dir())
	except:
		os.mkdir(get_user_dir())

def save_settings(username, password):
	cred = {
		"username": username,
		"password": password,
	}

	create_if_not_exists_user_dir()

	try:
		f = open(get_settings_path(), "w")
		f.write(json.dumps(cred))
		f.close()
		return cred
	except:
		return None

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Instagram Media Uploader')
	parser.add_argument(
		'--comment', '-c',
		help='Comment of picture',
		dest='comment',
		default = '',
		nargs='?',
	)
	parser.add_argument(
		'--media', '-m',
		help='Path to picture file to upload',
		dest='media',
	)
	parser.add_argument(
		'--force', '-f',
		action='store_true',
		help='Don\'t ask for confirmation',
		dest='force',
		default=False,
	)
	parser.add_argument(
		'--username', '-u',
		help='Username',
		dest='username',
		default=get_username(),
	)
	parser.add_argument(
		'--password', '-p',
		help='Password',
		dest='password',
		default=get_password(),
	)
	parser.add_argument(
		'--save-userpass', '-s',
		action='store_true',
		help='Store given user credentials and exit (username and password needed)',
		dest='save_userpass',
		default=False,
	)
	parser.add_argument(
		'--verbose', '-v',
		action='count',
		help='Say what\'s going on',
		dest='verbose',
		default=0,
	)
	args = parser.parse_args()

	if args.save_userpass == True:
		if args.username == None or args.password == None:
			print('No username and/or password given')
			sys.exit(1)
		else:
			save_settings(args.username, args.password)
			sys.exit(0)
	else:
		if args.media == None:
			print('Media file required!')
			parser.print_help()
			sys.exit(0)

		try:
			f = open(args.media, "rb")
			d = f.read(10)
			f.close()
		except Exception as e:
			print('Can\'t access media %s: %s' % (args.media, e))
			traceback.print_exc(file=sys.stderr)
			sys.exit(1)

	if (args.username == None or args.password == None) and (get_username() == None or get_password() == None):
		print('Username and/or password is not set, but required to run.')
		sys.exit(1)

	if (args.force == False):
		print("Account: %s" % (args.username))
		print("File   : %s" % (args.media))
		print("Comment: %s" % (args.comment))
		print("Press [Enter] to continue.")
		sys.stdin.read(1)

	instagram = InstagramSession(verbose=(args.verbose > 0))
	if (args.verbose >= 1):
		print('Log into instagram with username %s' % (args.username))

	try:
		rl = instagram.login(args.username, args.password)
		if rl["status"] == "ok":
			if (args.verbose >= 1):
				print('Uploading media %s' % (args.media))
			ru = instagram.upload_photo(args.media)
			if ru["status"] != "ok":
				print("Photo upload failed: %s" % (ru["message"]))
			else:
				media_id = ru["media_id"]

			if (args.verbose >= 1):
				print('Media ID is %s' % (media_id))
			
			if media_id is not None:
				if (args.verbose >= 1):
					print('Configuring media and setting comment')

				rc = instagram.configure_photo(media_id, args.comment)
				if rc["status"] != "ok":
					print("Photo configuration failed: %s" % (rc["message"]))

		else:
			print("Login failed: %s" % (rl["message"]))

	except Exception as e:
		print('Something wen\'t wrong while uploading: %s' % (e))
		traceback.print_exc(file=sys.stderr)
		sys.exit(1)

	sys.exit(0)
