
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize as opt
import requests
import datetime
from bs4 import BeautifulSoup
dates = []
infected = []
#infected = [45, 62, 121, 198, 291, 440, 571, 830, 1287, 1975, 2744, 4515] on 28th Jan 2019
URL = "http://en.wikipedia.org/wiki/2019–20_Wuhan_coronavirus_outbreak"

#BeautifulSoup to get data from wikipedia 
res = requests.get(URL).text
soup = BeautifulSoup(res,'lxml')
#Because it is a table we find "td" tag
tags = soup.find_all(['td'], text=True)
#Hacky solution instead of using RegEx. 
#Incase someone changes the code unsymmetrically this code won't work
for i,e in enumerate(tags):
    if len(str(e))>64:
        if str(e)[64:69]=='2020-':
            dates.append(str(e)[64:74])
            infected.append(str(tags[i+2])[75:-5])
infected = [int(i.replace(",","")) for i in infected]
tot_days = len(infected) 

#Converting the dates as a datetime object
dates = [datetime.datetime.strptime(date,"%Y-%m-%d").date() for date in dates]
days = range(tot_days)
#fit exponential curve (exponential regression)

def func(x, a, b, c):
    return a * np.exp(b * x) + c
'''
#fit logistic curve, didn't work K=80 Billion which means the curve is almost exponential
p = infected[0]
def func(x,k,r):
    num = k*p*np.exp(r*x)
    den = k+p*(np.exp(r*x)-1)
    fin = num/den
    return fin
'''

popt, pcov = opt.curve_fit(func, days, infected)
'''
#logistic curve calculate
print("K=",popt[0])
def func2(x):
    num = popt[0]*p*np.exp(popt[1]*x)
    den = popt[0]+p*(np.exp(popt[1]*x)-1)
    fin = num/den
    return fin
'''
#exponential function fitted
def func2(x):
        return popt[0]*np.exp(popt[1]*x)+popt[2]

#days predicted
predict = 2
days_predict = range(tot_days+predict)
last_known = dates[-1]
for i in range(predict):
    dates.append(last_known+datetime.timedelta(days=1+i))
tick = dates.copy()
#apply function
x_predict = [func2(i) for i in days_predict]

#Plot
plt.title("Novel Corona Virus (2019 nCoV) spread")
plt.ylabel("Number of Confirmed Cases")
plt.plot(days,infected)
plt.plot(days_predict[tot_days-1:],x_predict[tot_days-1:],linestyle="--",color='C0')
plt.xticks(days_predict,tick, rotation = "45")
plt.tight_layout()
plt.savefig(str(last_known)+', '+ str(last_known+datetime.timedelta(days=predict))+".png")
