(__import__("sys").path.append("D:\\K\\Coding\\projects\\Python-Lwp"),exec("_lwp=__import__(\"lwp\")"),exec(";".join([f"{k}=_lwp.__dict__[\"{k}\"]" for k in dir(_lwp) if k[:2]!="__"])),exec("del _lwp"))# from "D:\K\Coding\projects\Python-Lwp\lwp.py" import *
import time
import json as JSON
import random



class Valve(object):
	def __init__(self,ps,m):
		self.ps=ps
		self._m=m
		self._st=0



	def extend(self):
		if (self._st!=1):
			self._m.set_speed(100)
			self._st=1



	def retract(self):
		if (self._st!=-1):
			self._m.set_speed(-100)
			self._st=-1



	def stop(self):
		self._m.h._send([0x00,0x81,self._m.p,0x11,0x51,0,0])



class PlaneSimulator(object):
	def __init__(self,h1,h2):
		self._h1=h1
		self._h2=h2
		self.bl=Valve(self,self._h1.get_port(0)[0])
		self.br=Valve(self,self._h1.get_port(1)[0])
		self.fl=Valve(self,self._h1.get_port(2)[0])
		self.fr=Valve(self,self._h1.get_port(3)[0])
		self.s=Valve(self,self._h2.get_port(0)[0])
		self.bl.retract()
		self.br.retract()
		self.fl.retract()
		self.fr.retract()
		self.s.retract()
		time.sleep(0.3)



	def end(self):
		self.bl.retract()
		self.br.retract()
		self.fl.retract()
		self.fr.retract()
		self.s.retract()
		time.sleep(0.3)
		self._h1.disconnect()
		self._h2.disconnect()



	def run(self,fp,id_=None):
		with open(fp,"r") as f:
			dt=JSON.loads(f.read())
		dt=dt[(id_ if id_!=None else random.randint(0,len(dt)-1))]
		print(f"Running Flight Path: {dt['name']}")
		for k in dt["path"]:
			time.sleep((k["d"] if "d" in k.keys() else 0))
			for i in range(0,4):
				if (k["m"][i]!=0):
					getattr([self.br,self.bl,self.fr,self.fl][i],{-1:"retract",1:"extend"}[k["m"][i]])()
			print(f"BR: {(self.br._st+1)//2}, BL: {(self.bl._st+1)//2}, FR: {(self.fr._st+1)//2}, FL: {(self.fl._st+1)//2}")



def main():
	ps=PlaneSimulator(Hub.find([{0:LargeMotor,1:LargeMotor,2:LargeMotor,3:LargeMotor,50:RGBLed}],10,None,lambda h:h.get_port(50)[0].set_color("green"))[0][0],Hub.find([{0:XLMotor,50:RGBLed}],10,None,lambda h:h.get_port(50)[0].set_color("green"))[0][0])
	ps.s.extend()
	time.sleep(1)
	while (True):
		if (input("Load")!=""):
			break
		ps.s.retract()
		input("Start")
		ps.run("./flight.json",None)
		time.sleep(2)
		ps.br.retract()
		ps.bl.retract()
		ps.fr.retract()
		ps.fl.retract()
		time.sleep(2.5)
		ps.br.stop()
		ps.bl.stop()
		ps.fr.stop()
		ps.fl.stop()
		ps.s.extend()
		time.sleep(1)
		ps.s.stop()
	ps.end()



Hub.run(main)
