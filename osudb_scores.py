from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os.path
import time
import json

with open('C:/Users/nimi/Documents/Scripts/osudb_scores/login.json') as f:
  data = json.load(f)

username = data["username"]
password = data["password"]

# Cookies

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

# Navigate to osu

dummy = "https://osu.ppy.sh/beatmapsets/"
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path="C:/WebDriver/bin/chromedriver", options=options)
cookie = "C:/WebDriver/cookies/osu.pkl"
driver.get("http://osu.ppy.sh")

if not os.path.exists(cookie):

    login = driver.find_element(By.XPATH, "/html/body/div[3]/nav/div[2]/div[2]/a").click()
    user_field = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/form/div[1]/input[1]").send_keys(username + Keys.ENTER)
    password_field = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/form/div[1]/input[2]").send_keys(password + Keys.ENTER)
    time.sleep(3) # Make sure cookie is saved properly
    save_cookie(driver, cookie)
    exit()

load_cookie(driver, cookie)
 
# Beatmap testing

b_sets = ["958476"]
b_ids = ["2006816"]
mod_container_path = "/html/body/div[7]/div/div/div[3]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div[2]/div[3]/div[6]/div[2]"
unselected_mod = "[@class='beatmap-scoreboard-mod']"
selected_mod = "[@class='beatmap-scoreboard-mod beatmap-scoreboard-mod--enabled']"
score_path = "/html/body/div[7]/div/div/div[3]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]"
acc_path = "/html/body/div[7]/div/div/div[3]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]"
pp_path = "/html/body/div[7]/div/div/div[3]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div[2]/div[3]/div[4]/div[2]/span"
NM = ["NM","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[1]"]
EZ = ["EZ","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[2]"]
NF = ["NF","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[3]"]
HT = ["HT","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[4]"]
HR = ["HR","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[5]"]
SD = ["SD","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[6]"]
PF = ["PF","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[7]"]
DT = ["DT","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[8]"]
NC = ["NC","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[9]"]
HD = ["HD","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[10]"]
FL = ["FL","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[11]"]
SO = ["SO","/html/body/div[7]/div/div/div[3]/div[1]/div/div[2]/button[12]"]
wait = WebDriverWait(driver, 2) 

def selected(path, status=True):
    if status is True:
        wait.until(EC.presence_of_element_located((By.XPATH, path+selected_mod)))
    else:
        wait.until(EC.presence_of_element_located((By.XPATH, path+unselected_mod)))

def score_data():
    SCORE = wait.until(EC.presence_of_element_located((By.XPATH, score_path))).text
    ACC = wait.until(EC.presence_of_element_located((By.XPATH, acc_path))).text
    PP = wait.until(EC.presence_of_element_located((By.XPATH, pp_path))).text
    print(SCORE, ACC, PP)

def mod(mod, single=True, override=False, disable=False):
    if disable is False:
        MOD = driver.find_element(By.XPATH, mod[1])
        MOD.click()
        try:
            if single is True:            
                selected(mod[1])
                score_data()   
                MOD.click()
                selected(mod[1], status=False)
            elif override is True:      
                selected(mod[1])
                score_data()
            elif override is True:
                selected(mod[1])
        except:
            print("--NO SCORE")
    else: 
        MOD = driver.find_element(By.XPATH, mod[1])
        MOD.click()
        selected(mod[1], status=False)

def multi_mod(*args):
    for arg in args[:-1]:
        mod(arg, single=False)
    mod(args[-1], single=False, override=True)
    for arg in args:
        mod(arg, disable=True)

def check_single(*args):
    for arg in args:
        print("echo--",arg[0])
        mod(arg)

def check_multi(*mods):
    for mod in mods:
        s = ""
        for name in mod:
            s += str(name[0])
        print("echo--",s)
        multi_mod(*mod)

for b_set in b_sets:
    driver.get(dummy+b_set)   
    for b_id in b_ids:
        # Switch difficulty
        driver.find_element(By.XPATH, '//a[@href="#taiko/'+b_id+'"]').click()
        # Wait for mod's objects
        wait.until(EC.presence_of_element_located((By.XPATH, NM[1])))
        # Single Mod
        check_single(NM,EZ,HR,SD,DT,HD,FL)
        # Multi Mod
        check_multi((HD,HR),(EZ,DT),(EZ,HD),(EZ,FL),(HD,FL),(HR,FL),(DT,FL),(DT,HR),(HD,DT),(EZ,HD,FL),(EZ,DT,HD),(EZ,DT,FL),(HD,DT,HR),(HD,DT,FL),(DT,HR,FL),(HD,HR,FL),(EZ,HD,DT,FL),(HR,HD,DT,FL))

x = input("close")