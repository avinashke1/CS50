#!/usr/bin/python
#Author: Avinash Kumar
#Also used in my Final Year College Project
#Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications
#Original Paper published by: Ion Stoica†, Robert Morris‡, David Liben-Nowell‡, David R. Karger‡, M. Frans Kaashoek‡, Frank Dabek‡,Hari Balakrishnan‡
#Link: https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf

import os
import random
import math
#import pandas

#Creating total nodes

def nodenetwork():
	global n
	n=input("Enter the number of nodes in network: ")
	global N
	N=[]
	for i in range(n):
		N.append(i)
		if (i>n):
			i=0
			break

	print "Total no. of nodes: "
	print N

#Creating Services

	S=[]
	for i in range(n):
		S.append(i)
		if (i>n):
			i=0
			break
	global x
	x=dict(zip(N,S))
	Z=input("\n\nEnter the number of nodes to participate in network: ")
	participatenode(Z)

#Logical Ring of participating nodes

def participatenode(Z):
	if (Z<=n):
		global z1
		global z
		z1=[]
		for i in range (Z+1):
			z1.append(random.choice(N))
		z=[]
		for i in z1:
			if i not in z:
				z.append(i)
	else:
		print "Participating nodes must be less than total number of nodes!"

	z.sort()

#Mapping

	target=open('Project/Participating_Nodes.txt','w')
	target.write(str(x))
	target.write(str(z))
	print z
	#print "\n"
	global m
	m=input("\nEnter the number of bits of Nodes(2^m): ")
	finger_generation(len(z))

#Generating Finger Table

def finger_write(finger,i):
			t=open("Project/node_"+`i`+".dat","w")
			t.write(str(finger))
			

def finger_generation(val):
	print "Finger Table:\n"
	for i in range(val):
		finger=[]
		finger_def(finger,val,z[i])
		print finger
		finger_write(finger,z[i])	

def finger_def(finger,val,n):
	for k in range(1,val+1):
		f=int((n+math.pow(2,k-1))%(math.pow(2,m)))
		finger.append(f)

#Search Operation

def searching():
	x=input("Enter the search key: ")
	y=input("Enter the starting search node: ")
	j=0
	counter=0
	flag=False
	while(j<=len(z) and flag==False):
		j=z.index(y)	
		i=z[j]
		t=open("Project/node_"+`i`+".dat","r")
		r=t.read()

		if (str(x) in r):
			print str(x) +" is in Node:",z[j]
			counter+=1
			break
		else:
			for j in range(0,len(z)):
				i=z[j]
				t=open("Project/node_"+`i`+".dat","r")
				r=t.read()
				if (str(x) in r):
					print str(x) +" is in Node:",z[j]
					j+=1
					counter+=1
				else:
					j=0
					while(flag==False):
						if(x<z[j]):
							print str(x)+" is in cache of Node: ",z[j]
							flag=True
							counter+=1
							break
						elif(x>z[j] and x<=z[j+1]):
							print str(x)+" is in cache of Node: ",z[j+1]
							flag=True
							counter+=1
							break
						elif(x<z[j] and x>z[len(z)-1]):
							print str(x)+" is in cache of Node: ",z[len(z)-1]
							flag=True
							counter+=1
							break
						elif(x>z[j+1] and x<z[len(z)-1]):
							print str(x)+" is in cache of Node: ",z[len(z)-1]
							flag=True
							counter+=1
							break
						else:	
							print str(x)+" is in cache of Node: ",z[0]
							flag=True
							counter+=1
							break
			
			break
		break
	print "Search Time: ",counter	

#Joining Operation

def joining():
	join=input("\nEnter the node to join: ")
	if (join not in z):
		for i in range(len(z),len(z)+1):
			z.append(join)	
			z.sort() 
		print("\nNew participating nodes: ")
		print z
		print "\nFinger table after adding node: ",join
		finger_generation(len(z))
	else:
		print "%d is already present!"%(join)

#Removing operation

def removing():
	remove=input("Enter the node to remove: ")
	k=remove
	z.remove(k)
	print k
	os.remove("Project/node_"+`remove`+".dat")
	print("\nNew participating nodes: \n")
	print z
	for j in range(len(z)):
		i=z[j]
		t=open("Project/node_"+`i`+".dat","r")
		r=t.read()
		r=r.replace(str(k),'')
		t=open("Project/node_"+`i`+".dat","w")
		t.write(r)	
	print "Finger table after removing node: ",k
	finger_generation(len(z))	

#Main Function

if __name__=='__main__':

	while(1):
		print "\n"
		print "0:Intialise Network\n1:Searching\n2:Joining\n3:Removing\nFor Exit: Ctrl+Z"
		options={0:nodenetwork,
				 1:searching,
				 2:joining,
				 3:removing,
		}
		op=input("\nGive option: ")
		options[op]()

		
