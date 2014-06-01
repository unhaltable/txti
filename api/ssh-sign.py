#!/usr/bin/python

# A handy python script to use SSH host keys and known_host files to
# encrypt/decrypt or sign/verify files. The basic idea is to have a HTTP
# server without SSL, but you still can use it (internally) as package-distribution
# or update server if you just ever connected to it via SSH and ensured
# that the SSH key matches during SSH login.
#
# It works with DSA and RSA host keys (not ECC keys):
#
# linux:~ # ssh-sign -f /etc/passwd -s /etc/ssh/ssh_host_rsa_key -H 127.0.0.1
# Signing file for host '127.0.0.1' ...
# SHA256 hash of '/etc/passwd': 53ec[...]0fe2
# linux:~ # cat /etc/passwd.ssh-signed
# keytype ssh-rsa
# mode paramiko
# host 127.0.0.1
# hash sha256
# signature AAAAB3Nzai[...]Q7JwD6KhbgPg==
# linux:~ # ssh-sign -f /etc/passwd -k .ssh/known_hosts
# Verifying file '/etc/passwd' ...
# No valid RSA or DSA host key for '127.0.0.1'
# linux-czfh:~ # ssh 127.0.0.1
# The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
# RSA key fingerprint is cc:[...]74:3c.
# Are you sure you want to continue connecting (yes/no)? yes
# Warning: Permanently added '127.0.0.1' (RSA) to the list of known hosts.
# Password: <Ctrl-C>
# linux:~ # ssh-sign -f /etc/passwd -k .ssh/known_hosts
# Verifying file '/etc/passwd' ...
# Found Host: '127.0.0.1' and Keytype: 'ssh-rsa'.
# SHA256 hash of '/etc/passwd': 53ec2[...]09840fe2
# Signature OK for host '127.0.0.1'.
# linux:~ # echo $?
# 1
# linux:~ # ssh-sign -f /etc/passwd -k .ssh/known_hosts -H 1.2.3.4
# Verifying file '/etc/passwd' ...
# Given host does not match host from signature blob.
# linux:~ # echo $?
# 0
# linux:~ # ssh-sign -f /etc/passwd -e /etc/ssh/ssh_host_rsa_key.pub
# Encrypting file with '/etc/ssh/ssh_host_rsa_key.pub' to outfile '/etc/passwd.ssh-aescfb'.
# linux:~ # ls -l /etc/passwd.ssh-aescfb
# -rw------- 1 root root 2269 Mar 14 09:42 /etc/passwd.ssh-aescfb
# linux:~ # ssh-sign
# Need a file (-f) to operate on.
# Usage: ssh-sign <-f file> [-s signkey file] [-e privkey...] [-d pubkey...] [-k knownhosts...] [-o outfile] [-H host]
# linux:~ #

#
# (C) 2012 Sebastian Krahmer under the GPL
#
# You need to have PyCrypto and paramiko installed
#
# This is my first python script. If you find any bugs, in particular
# in the crypto part, please let me know: sebastian.krahmer [at] gmail [.] com

import os
import sys
import subprocess
from getopt import *
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, MD5
from base64 import b64encode, b64decode
from paramiko.util import load_host_keys
from Crypto.Random.random import StrongRandom
from paramiko import HostKeys, Message, RSAKey, DSSKey


def error(msg):
	raise Exception(msg)

def excl_open(path, mode):
	return os.fdopen(os.open(path, os.O_WRONLY|os.O_CREAT|os.O_EXCL, mode), 'w')


class SSHKey:
	def __init__(self, args):
		self.knownfile = ''
		self.keytype = ''
		self.pubfile = ''
		self.privfile = ''
		self.signfile = ''
		self.blob = ''
		self.host = ''
		self.hhost = ''
		self.privkey = ''
		self.pubkey = ''
		self.signkey = ''
		self.knownkey = ''

		if 'known' in args:
			self.knownfile = args['known']
		if 'pub' in args:
			self.pubfile = args['pub']
		if 'priv' in args:
			self.privfile = args['priv']
		if 'sign' in args:
			self.signfile = args['sign']
		if 'host' in args:
			self.host = args['host']
		if 'blob' in args:
			self.blob = args['blob']

		# for decryption
		if self.privfile != '':
			rsakey = ''
			try:
				f = open(self.privfile, 'r')
				for line in f:
					rsakey += line
			except:
				error('No private key file found.')
			f.close()
			try:
				self.privkey = RSA.importKey(rsakey)
			except:
				error('No valid private RSA key found.')

		# to sign files
		if self.signfile != '':
			try:
				f = open(self.signfile, 'r')
				line = f.readline()
				f.close()
				if line.find('RSA') != -1 or line.find('rsa') != -1:
					self.signkey = RSAKey.from_private_key_file(self.signfile)
				else:
					self.signkey = DSSKey.from_private_key_file(self.signfile)
			except:
				error('No valid signature key found.')

		# to encrypt files
		if self.pubfile != '':
			try:
				s = subprocess.check_output(['ssh-keygen', '-e', '-m', 'PKCS8', '-f',
				                            self.pubfile], shell = False)
				self.pubkey = RSA.importKey(s)
			except:
				error('No valid public RSA key found.')

	# load known hosts file for verifying
	def __load_hk(self):
		try:
			keys = load_host_keys(self.knownfile)
		except:
			error("No valid public keys found in '" + self.knownfile + "'")
		self.knownkey = ''
		for h in [self.host, self.hhost]:
			if h in keys:
				if self.keytype in keys[h]:
					self.knownkey = keys[h][self.keytype]
					break
		if self.knownkey == '':
			error("No valid RSA or DSA host key for '" + self.host + "'")

	def __sign(self, path):
		# hash file content
		digest = SHA256.new()
		try:
			f = open(path, 'rb')
			buf = ' '
			while buf != '':
				buf = f.read(4096)
				digest.update(buf)
			f.close()
		except:
			error('Unable to read source file for signing.')

		print "SHA256 hash of '" + path + "': " + digest.hexdigest()
		sig = self.signkey.sign_ssh_data(Random.new(), digest.hexdigest())

		try:
			f = excl_open(path + '.ssh-signed', 0644)
			f.write('keytype ' + self.signkey.get_name() + '\nmode paramiko\nhost ' +
			        self.host + '\nhash sha256\nsignature ' + b64encode(str(sig)) + '\n')
		except:
			error('Failed to open signature file for writing.')
		f.close()
		return True

	def sign(self, path):
		if self.signfile == '':
			error('No valid private key to sign file.')
		if self.host == '':
			error('No hostname given to sign as.')
		return self.__sign(path)

	def __verify(self, args):
		digest = SHA256.new()
		try:
			f = open(args['path'], 'rb')
			buf = ' '
			while buf != '':
				buf = f.read(4096)
				digest.update(buf)
			f.close()
		except:
			error('Not able to open data file for verifying.')

		print "SHA256 hash of '" + args['path'] + "': " + digest.hexdigest()
		m = Message(b64decode(args['signature']))
		return self.knownkey.verify_ssh_sig(digest.hexdigest(), m)

	def verify(self, path):
		if self.knownfile == '':
			error('No known_hosts file to check against.')

		args = {'path': path}
		try:
			f = open(path + '.ssh-signed', 'r')
			for line in f:
				[k, v] = line.replace('\n', '').split();
				args[k] = v
		except:
			error('Not able to open signature file for verifying.')
		f.close()
		if not 'signature' in args:
			error('Missing signature-tag in signature file.')
		if not 'host' in args:
			error('Missing host-tag in signature file.')
		if not 'keytype' in args:
			error('Missing keytype-tag in signature file.')

		if self.host != '' and self.host != args['host']:
			error('Given host does not match host from signature blob.')

		self.host = args['host']
		self.hhost = HostKeys.hash_host(self.host)
		self.keytype = args['keytype']
		self.__load_hk()
		print "Found Host: '" + self.host + "' and Keytype: '" + self.keytype + "'."
		return self.__verify(args)

	def encrypt(self, path):
		if self.pubfile == '':
			error('No valid RSA public keyfile for encryption.')

		r = StrongRandom()
		digest = MD5.new()
		digest.update(str(r.getrandbits(256)))
		aes = AES.new(digest.hexdigest(), AES.MODE_CFB)

		try:
			fin = open(path, 'rb')
			fout = excl_open(path + '.ssh-aescfb', 0600)

			fout.write(self.pubkey.encrypt(digest.hexdigest(), '')[0])
			buf = ' '
			while buf != '':
				buf = fin.read(4096)
				fout.write(aes.encrypt(buf))
		except:
			error('Unable to open source/target file for encryption.')

		fin.close()
		fout.close()
		return True

	def decrypt(self, inpath, opath):
		if self.privfile == '':
			error('No valid RSA private keyfile for decryption.')

		try:
			fin = open(inpath, 'rb')
			fout = excl_open(opath, 0600)

			# first 256 byte of file is RSA encrypted AES key
			buf = fin.read(256)
			aes = AES.new(self.privkey.decrypt(buf), AES.MODE_CFB)
			buf = ' '
			while buf != '':
				buf = fin.read(4096)
				fout.write(aes.decrypt(buf))
		except:
			error('Unable to open source/target file for decryption.')

		fin.close()
		fout.close()
		return True



def usage():
	 print('Usage: ssh-sign <-f file> [-s signkey file] [-e privkey...] [-d pubkey...] [-k knownhosts...] [-o outfile] [-H host]')
	 exit()

host = ''
priv = ''
known = ''
sign = ''
blob = ''
pub = ''
outfile = ''
infile = ''

try:
	[opts, args] = getopt(sys.argv[1:], 'f:s:e:d:k:o:H:')
except:
	usage()

for o in opts:
	if o[0] == '-s':
		sign = o[1]
	if o[0] == '-e':
		pub = o[1]
	if o[0] == '-d':
		priv = o[1]
	if o[0] == '-k':
		known = o[1]
	if o[0] == '-o':
		outfile = o[1]
	if o[0] == '-f':
		infile = o[1]
	if o[0] == '-H':
		host = o[1]

if infile == '':
	print 'Need a file (-f) to operate on.'
	usage()

if sign != '':
	if priv != '':
		print 'Either sign (-s) or encrypt (-e) a file.\n'
		usage()
	if known != '':
		print 'Either sign (-s) or verify (-k) a file.\n'
		usage()
	if pub != '':
		print 'Either sign (-s) or decrypt (-d) a file.\n'
		usage()
	if host == '':
		print 'Need a hostname or IP (-H) to sign as (must match entry in targets known_hosts file.\n'
		usage()

if priv != '':
	if known != '':
		print 'Either decrypt (-d) or verify (-k) a file.\n'
		usage()
	if pub != '':
		print 'Either decrypt (-d) or encrypt (-e) a file.\n'
		usage()
	if outfile == '':
		if infile.endswith('.ssh-aescfb'):
			outfile = infile.replace('.ssh-aescfb', '')
		else:
			print 'Need output file (-o) to decrypt to.\n'
			usage()

if pub != '':
	if known != '':
		print 'Either encrypt (-e) or verify (-k) a file.\n'
		usage()


args = {'known': known, 'sign': sign, 'priv': priv, 'host': host, 'blob': infile + '.ssh-sign', 'pub': pub}

r = False

try:

	s = SSHKey(args)

	if sign != '':
		print "Signing file for host '" + host + "' ..."
		r = s.sign(infile)
	elif known != '':
		print "Verifying file '" + infile + "' ..."
		r = s.verify(infile)
		if r:
			print "Signature OK for host '" + s.host + "'."
		else:
			print "Signature NOT ok for host '" + s.host + "'."
	elif pub != '':
		print "Encrypting file with '" + pub + "' to outfile '" + infile + ".ssh-aescfb'."
		r = s.encrypt(infile)
	elif priv != '':
		print "Decrypting file with '" + priv + "' to outfile '" + outfile + "'."
		r = s.decrypt(infile, outfile)
	else:
		print 'You did not specify any operation (-e, -d, ...) on file.\n'
		usage()

except Exception as e:
	print(e)

exit(r)

