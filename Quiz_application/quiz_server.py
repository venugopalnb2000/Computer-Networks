from socket import *
import threading
# from thread import *
from time import *
# from os import *
from datetime import datetime
import os
host='127.0.0.1'
# port=int(input('enter port '))
port = 1111
s=socket(AF_INET,SOCK_STREAM)
s.bind((host,port))
s.listen(3)

t1=localtime(time())[5]

online=[]
def users():
	a=dict()
	file='./authentication.txt'
	f=open(file,'r')
	users=f.read().strip().splitlines()
	for user in users:
		name,pswd=user.split(',')
		a[name]=pswd
	f.close()
	return a

def append_ans(user,lopt,score):
	path='./ans_recorded.csv'
	file2=open(path,'r')
	init_content=file2.read()
	dt=datetime.now()
	file2.close()
	file=open(path,'w')
	k=''
	# k=",".join(lopt)
	for i in lopt:
		if i=='':
			i='-'
		k=k+i+","
	q=str(dt)+","+user+","+k+score
	# q=str(dt)+","+user+","+lopt[0]+","+lopt[1]+","+lopt[2]+","+lopt[3]+","+score
	answers=file.write(init_content+q+'\n')
	file.close()

def questions():
	q=[]
	i=1
	path='./question.txt'
	f=open(path,'r')
	lines=f.read().splitlines()
	for line in lines:
		l=line.split(',')
		q_o="Q."+str(i)+") "+l[0] + "\na) "+l[1]+"\nb) "+l[2]+"\nc) "+l[3]+"\nd) "+l[4]+"\n"
		q.append(q_o)
		i+=1
	f.close()
	return q



def return_results(list_opt,quest):
	correct='CORRECT ANSWERS \n\n\n'
	incorrect='INCORRECT ANS \n\n\n'
	unanswered='UNANSWERED \n\n\n'
	path='./correct_ans.txt'
	file=open(path,'r')
	corr_ans=file.read().strip().split(',')
	c=0
	t="\n\n-----------------------------------------------------------------------------------------\n\n"
	h="\n\n#################################################################################################\n\n"
	for i in range(len(corr_ans)):
		if list_opt[i]==corr_ans[i]:
			correct = correct + quest[i] + '\n\n' + 'correct answer ' + list_opt[i] + "\n\n"
			c+=1
		elif len(list_opt[i])==0:
			unanswered=unanswered + quest[i] + '\n\n' + 'Answer ' + corr_ans[i] + "\n\n"
		else:
			incorrect = incorrect + quest[i] + '\n\n' + 'correct answer ' + corr_ans[i] + '\nYour answer ' + list_opt[i] + "\n\n"

	total="total score = " + str(c) + t
	final=total + h + correct + h +incorrect + h + unanswered + h
	file.close()
	return final+"\t"+str(c)


def send_questions(c,u_name):
	q=questions()
	# print q
	i=0
	list_opt=['' for _ in range(len(q))]
	while(i<len(q)):
		if(list_opt[i]==''):
			c.send(q[i])
		else:
			p=q[i]+"\nPrevious choice "+list_opt[i]
			c.send(p)
		# print q[i]
		opt=c.recv(4096)
		if opt=='1':
			i+=1
		elif opt=='0' and i!=0:
			i-=1
		elif opt=='0' and i==0:
			i=0
		elif opt=='exit':
			c.send('sure')
			if(c.recv(4096) in ['y','Y','']):
				rs,score=return_results(list_opt,q).split('\t')
				append_ans(u_name,list_opt,score)
				c.send(rs)
				c.close()
			# break
		else:
			list_opt[i]=opt
			i+=1
		if(i==len(q)):
			rs,score=return_results(list_opt,q).split('\t')

			# print score
			c.send('end')
			x= c.recv(4096)
			if x in ['Y','y']:
				c.send(rs)
				k=append_ans(u_name,list_opt,score)
				# print k
				c.close()
			else:
				i=0
			


def listen_client(c,addr):
	# c.settimeout(10.0)
	try:
		c.send('####----- AUTHENTICATION --- ####')
		auth_det=c.recv(4096)
		if auth_det=='close':
			c.close()
		else:
			try:
				a=users()
				u_name,u_password=auth_det.split(',')
				# print u_name
				if(u_name in online):
					c.send('Cannot Login again')
					c.close()
				elif((u_name not in a) or (a[u_name]!=u_password)):
					c.send('Login Credentials Failed')
					c.close()
				else:
					# print online
					online.append(u_name)
					c.send('Success')
					if c.recv(4096)=='ack':
						try:
							send_questions(c,u_name)
						except :
							print ""
			except:
				print ""
	except KeyboardInterrupt as e:
		c.close()
		exit(0)

def main():
	# t1=localtime(time())[5]
	print("server...")
	try :
		while 1:
			c,addr=s.accept()
			# c.settimeout(10)
			threaded=threading.Thread(target=listen_client,args=(c,addr))
			threaded.start()
		# exit(0)
	except KeyboardInterrupt as k:
		os.system('clear')
		print "closing Server ........"
		sleep(2)
		# s.close()
		exit(0)
main()