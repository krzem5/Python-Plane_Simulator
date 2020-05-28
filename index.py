(__import__("sys").path.append("D:\\K\\Coding\\projects\\Python-Lwp"),exec("_lwp=__import__(\"lwp\")"),exec(";".join([f"{k}=_lwp.__dict__[\"{k}\"]" for k in dir(_lwp) if k[:2]!="__"])),exec("del _lwp"))
import time



VALVE_ANGLE=35



class Valve(object):
	def __init__(self,ps,m):
		self.ps=ps
		self._m=m
		self._st=0



	def extend(self):
		if (self._st!=1):
			if (self._st==0):
				self._m.rotate(VALVE_ANGLE,100,100,0)
			else:
				self._m.rotate(VALVE_ANGLE*2,100,100,0)
			self._st=1



	def retract(self):
		if (self._st!=-1):
			if (self._st==0):
				self._m.rotate(VALVE_ANGLE,-100,100,0)
			else:
				self._m.rotate(VALVE_ANGLE*2,-100,100,0)
			self._st=-1



	def hold(self):
		if (self._st!=0):
			self._m.rotate(VALVE_ANGLE,-100*self._st,100,0)
			self._st=0



class PlaneSimulator(object):
	def __init__(self,h):
		self._h=h
		self.bl=Valve(self,self._h.get_port(0)[0])
		self.br=Valve(self,self._h.get_port(1)[0])
		self.fl=Valve(self,self._h.get_port(2)[0])
		self.fr=Valve(self,self._h.get_port(3)[0])
		self.bl._m.set_speed(-100)
		self.br._m.set_speed(-100)
		self.fl._m.set_speed(-100)
		self.fr._m.set_speed(-100)
		time.sleep(0.1)
		self.bl._m.rotate(VALVE_ANGLE,100,100,0)
		self.br._m.rotate(VALVE_ANGLE,100,100,0)
		self.fl._m.rotate(VALVE_ANGLE,100,100,0)
		self.fr._m.rotate(VALVE_ANGLE,100,100,0)


	def end(self):
		self.bl.retract()
		self.br.retract()
		self.fl.retract()
		self.fr.retract()



def main():
	hl=Hub.find([{0:LargeMotor,1:LargeMotor,2:LargeMotor,3:LargeMotor}],i=2,t=CPlusHub)
	ps=PlaneSimulator(hl[0][0])
	input(">>>")
	ps.fr.extend()
	ps.fl.extend()
	time.sleep(2)
	ps.br.extend()
	ps.bl.extend()
	time.sleep(2)
	ps.fr.retract()
	ps.fl.retract()
	time.sleep(0.8)
	ps.fr.extend()
	ps.fl.extend()
	ps.br.retract()
	ps.bl.retract()
	time.sleep(1.2)
	ps.fl.retract()
	ps.br.extend()
	time.sleep(2.1)
	ps.fr.retract()
	ps.fl.extend()
	ps.br.retract()
	ps.bl.extend()
	time.sleep(2.1)
	ps.fr.extend()
	ps.br.extend()
	time.sleep(2)
	ps.fr.retract()
	ps.fl.retract()
	time.sleep(2)
	ps.end()



Hub.run(main)
