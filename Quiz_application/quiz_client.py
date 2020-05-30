from socket import *
from os import *
from time import *

host='127.0.0.1'
# port=int(input('enter port '))
port = 1111

def recv_quest(s):
	li_o=['a','b','c','d','0','1','exit']
	while 1:
		flag=0
		system('clear')
		print("0 for back \n1 for front \nexit to end\n\n")
		q=s.recv(4096)
		if not q:
			break
		print q
		if(q=='end'):
			choice=raw_input('Are you sure you want to exit (Y/N) ')
			while choice=='':
				choice=raw_input('Are you sure you want to exit (Y/N) ')
			s.send(choice)
			if choice in ['Y','y','\n']:
				system('clear')
				print s.recv(4096)
				s.close()
				exit(0)
			else:
				continue
			# continue
		opt=raw_input("Enter Options ")
		while opt not in li_o:
			opt=raw_input("invalid\nenter choice   ")
		if opt=='exit':
			s.send('exit')
			print s.recv(4096)
			choice=raw_input('Are you sure you want to exit (Y/N) ')
			while choice=='':
				choice=raw_input('Are you sure you want to exit (Y/N) ')
			s.send(choice)
			if choice in ['Y','y']:
				system('clear')
				print s.recv(4096)
				s.close()
				exit(0)	
			flag=1
		if flag!=1:	
			s.send(opt)





def main():
	s=socket(AF_INET,SOCK_STREAM)
	s.connect((host,port))

	print("connection acheived ...")

	system('clear')
	print(s.recv(4096)+"\n\n")
	print "-------------------------------------------------------\n"
	u_name=raw_input('Enter u_name ').strip()
	print "\n"

	u_password=raw_input('Enter u_password ').strip()
	print "\n"
	print "----------------------------------------------------------\n"
		# print(str(len(u_name))+" "+u_password)
	i=4
	while((u_name=='' or u_password=='') and i>0):
			# print(len(u_name),len(u_password))
		system('clear')
		print "-------------------------------------------------------------\n"
		print("Empty username or password\n\nEnter Again ... \n\n")
			
		print'Attempts remaining %s \n\n'%i
		i-=1
		u_name=raw_input('Enter u_name ')
		print "\n"

		u_password=raw_input('Enter u_password ')
		print "\n"

		print "-------------------------------------------------------------\n"
	if(i==0):
		s.send('close')
		print "\n\nClosing ......."
		sleep(3)
		exit(0)
	s.send(u_name+","+u_password)

	message=s.recv(4096)
	if(message!='Success'):
		print(message)
		s.close()
		exit(0)
	# else:
	else:
		system('clear')
		print message+"........\nEnjoy the test !!!\n"
		sleep(4)
		s.send('ack')
		# while 1:
		recv_quest(s)
	s.close()
try:
	main()
except KeyboardInterrupt as e:
	exit(0)
