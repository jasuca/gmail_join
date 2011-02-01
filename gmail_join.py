#!/opt/local/bin/python
# encoding: utf-8
"""
Gmail join conversations (threads)
"""

import sys
import os

import sys
import imaplib
import re

#RE expressions
subject_str = re.compile(r'Subject:.*?\r\n')
msgid_str = re.compile(r'Message-I.: <.*?>\r\n')
ref_str = re.compile(r'References: <.*?>\r\n')
rep_str = re.compile(r'In-Reply-To: <.*?>\r\n')
#end RE expressions


#VARS
imap_server = 'imap.gmail.com'
user = 'user@gmail.com'
pwd = 'your_password'


label_0 = '000_to_join'
label_1 = '001_joined'
msg_subject = "What are you doing this winter ?"
thr_number = 'In-Reply-To: <%s>\r\n'%'AAABB-some-hash@somemessage.com'
#end VARS


#Start M1
M=imaplib.IMAP4_SSL(imap_server, 993)
M.login(user,pwd)

#Start M2
M2=imaplib.IMAP4_SSL(imap_server, 993)
M2.login(user,pwd)


status, count = M.select(label_0)
status, count = M2.select(label_1)


print 'Fetching messages...'
typ, data = M.search(None, 'ALL')
msgs = data[0].split()

sys.stdout.write(" ".join(['Copying', str(len(msgs)), 'messages']))
print



counter = 0
for num in msgs:
	typ, data = M.fetch(num, '(RFC822)')
	sys.stdout.write('.')
	
	#same subject
	new_title = " ".join(["Re:"]*counter)+msg_subject
	new_data = subject_str.sub('Subject: %s\r\n'%new_title, data[0][1])
	
	
	#if replay-to
	if rep_str.search(new_data):
		new_data = rep_str.sub('%s'%thr_number, new_data)
	else:
		for f in msgid_str.findall(new_data):
			id_msg = f
			break
		new_data = msgid_str.sub('%s%s'%(id_msg,thr_number), new_data)
		

	#copy to new folder
	M2.append(label_1, None, None, new_data)
	
	counter+=1
	
#Close and logout
M.close()
M.logout()

M2.close()
M2.logout()
