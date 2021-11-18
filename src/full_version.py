import json
import os
import pandas as pd
import scraper
import webbrowser
import numpy as np

class full_version:
	def __init__(self):
		self.data={}
		self.name=""
		self.email=""
		self.user_data = os.path.join(
			os.path.dirname(
				os.path.dirname(
					os.path.abspath(__file__))),
			"json", 
			"user_data.json"
			)
		self.user_list = os.path.join(
			os.path.dirname(
				os.path.dirname(
					os.path.abspath(__file__))),
			"csvs", 
			"user_list.csv"
			)
		self.df=pd.DataFrame()
		self.currency=""
		pd.set_option('display.max_rows', None)
		pd.set_option('display.max_columns', None)
		pd.set_option('display.width', None)
		pd.set_option('display.max_colwidth', 40)


	def login(self):
		''' Used for User Login
		    Returns the username and email'''
		if not os.path.exists(self.user_data):
			print("Welcome to Slash!")
			print("Please enter the following information: ")
			name=input("Name: ")
			email=input("Email: ")
			self.data['name']=name
			self.data['email']=email
			with open(self.user_data, 'w') as outfile:
				json.dump(self.data, outfile)
			self.name=name
			self.email=email
		else:
			with open(self.user_data) as json_file:
				data = json.load(json_file)
				self.name=data['name']
				self.email=data['email']
		return self.name, self.email

	def search_fn(self):
		''' Functino searches for a given product and returns full list of products scraped. 
		It then gives the user and option to save an item or open an item in browser'''
		prod=input("Enter name of product to Search: ")
		self.scrape(prod)
		ch=int(input("\n\nEnter 1 to save product to list \n2 to open link in browser\nelse enter any other key to continue\n"))
		if ch==1:
			indx=int(input("Enter row number of product to save: "))
			if indx<len(self.df):
				if os.path.exists(self.user_list):
					old_data=pd.read_csv(self.user_list)
				else:
					old_data=pd.DataFrame()
				if self.df.title[indx] not in old_data:
					old_data=pd.concat([old_data,self.df.iloc[[indx]]])
					print(self.df.iloc[[indx]])
				old_data.to_csv(self.user_list, index=False,header=self.df.columns)
		if ch==2:
			indx=int(input("Enter row number of product to open: "))
			webbrowser.open_new(self.df.link[indx])

		pass

	def extract_list(self):
		'''This function helps user extract saved products and modify list or open product in browser'''
		if os.path.exists(self.user_list):
			old_data=pd.read_csv(self.user_list)
			print(old_data)
			choice=int(input("Select from the following:\n1. Delete item from list\n2. Open link in Chrome\n3. Continue\n"))
			if choice==1:
				indx=int(input("Enter row number to be removed: "))
				old_data=old_data.drop(index=indx)
				if old_data.shape[0]==0:
					os.remove(self.user_list)
					return
				
				old_data.to_csv(self.user_list, index=False,header=old_data.columns)
			if choice==2:

				indx=int(input("Enter row number to open in chrome: "))
				url=old_data.link[indx]
				
				webbrowser.open_new(url)


		else:
			print("No saved data found.")
		pass

	def scrape(self,prod):
		''' calls the scraper function from scraper.py'''
		results=scraper.driver(prod,df_flag=1,currency=self.currency)
		#esults = formatter.sortList(results, "ra" , True)
		self.df=pd.DataFrame.from_dict(results, orient='columns')
		print(self.df.replace("",np.nan).dropna())



	def driver(self):
		self.login()
		flag_loop=1
		print("Welcome ",self.name)
		while flag_loop==1:
			print("Select from following:")
			print("1. Search new product\n2. See exiting list\n3. See Currency Conversion\n4. Exit")
			choice=int(input())
			if choice==1:
				self.search_fn()
			elif choice==2:
				self.extract_list()
			elif choice==3:
				self.currency=input("Enter INR/EUR\n").lower()
			elif choice ==4:
				print("Thank You for Using Slash")
				flag_loop = 0
			else:
				print("Incorrect Option")
