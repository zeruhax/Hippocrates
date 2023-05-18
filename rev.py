import requests,json
from threading import Thread
from queue import Queue
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get("configuration","api_key")
class Worker(Thread):
  def __init__(self, tasks):
      Thread.__init__(self)
      self.tasks = tasks
      self.daemon = True
      self.start()

  def run(self):
      while True:
          func, args, kargs = self.tasks.get()
          try: func(*args, **kargs)
          except Exception as e: print(e)
          self.tasks.task_done()

class ThreadPool:
  def __init__(self, num_threads):
      self.tasks = Queue(num_threads)
      for _ in range(num_threads): Worker(self.tasks)

  def add_task(self, func, *args, **kargs):
      self.tasks.put((func, args, kargs))

  def wait_completion(self):
      self.tasks.join()
      
class Reverse:
        
    def __init__(self, iplist, server):
        self.endpoint = "http://api.zeru.ninja:8080/api/"
        self.api_key = api_key
        self.tmp_ip = []
        self.result = []
        self.ip = iplist
        self.server = server

    def reverse(self, ips):
        if ips not in self.tmp_ip:
            self.tmp_ip.append(ips)
            headers = {"X-API-KEY":self.api_key, 'Content-Type': 'application/x-www-form-urlencoded'}
            data = {"ip" : ips, "server" : self.server}
            req = requests.post(self.endpoint + "reverse", json=data, headers=headers)
            js = json.loads(req.text)
            if js["data"]["domain"] == None:
                print(f"Ip {ips} , have 0 domain")
            else:
                total = js["data"]["domain"]
                for x in js["data"]["domain"]:self.result.append(x);open(f"server-{self.server}.txt", "a+").write(x + "\n")
                print(f"Ip {ips} , have {len(total)} Domain")
        else:print("IP :" + ips + " SAME IP") 
        
    def execute(self, thread):
        pool = ThreadPool(int(thread))
        for url in self.ip:
            self.ip = url
            pool.add_task(self.reverse, self.ip)
        pool.wait_completion()
        print(f"Task Done , total : {len(self.result)} domain")
        
class Menu():

    def __init__(self):
        self.banner()
                
    def banner(self):
        print("""
                  __  ___                                   __           
   / / / (_)___  ____  ____  ______________ _/ /____  _____
  / /_/ / / __ \/ __ \/ __ \/ ___/ ___/ __ `/ __/ _ \/ ___/
 / __  / / /_/ / /_/ / /_/ / /__/ /  / /_/ / /_/  __(__  ) 
/_/ /_/_/ .___/ .___/\____/\___/_/   \__,_/\__/\___/____/  
       /_/   /_/                                           
              """)
    
    def input_list(self):
        ip = open(input("list : "), encoding="utf8" ).read().splitlines()
        server = input("Choose Server (one-eleven): ")
        return ip , server

try:
    menu = Menu()
    print("""Available Server : one,two,three,four,five,six,seven,eight,nine,ten,eleven \nCredit @Real_Zeru_nishimura""")
    ip , server = menu.input_list()
    thread = input("Thread: ")
    rev = Reverse(ip, server).execute(int(thread))
except KeyboardInterrupt:
    print("Bye")
    exit()
