import paho.mqtt.client as mqtt
import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import datetime
import os


browser = None
Contact = []
message = None
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None

chrome_options = Options()
chrome_options.add_argument('--user-data-dir=./User_Data')
browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 1000)
browser.get(Link)
browser.maximize_window()

def send_message(target):
    global message, wait, browser
    print("Entro")
    try:
        
        x_arg = '//span[contains(@title,' + target + ')]'
        print("Entro1")
        ct = 0
        while ct != 10:
            print("Entro2")
            try:
                group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                print("dsdad")
                group_title.click()
                break
            except Exception as e:
                print(e)
                ct += 1
                time.sleep(3)
        print("Entro3")
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
        time.sleep(1)
    except NoSuchElementException as error:
        print(error)
        return

def sender():
    print("hola mundo")
    
    global Contact, choice, docChoice, unsaved_Contacts
    for i in Contact:
        print("Message sent to ", i)
        send_message(i)
        
    time.sleep(5)
    if len(unsaved_Contacts) > 0:
        for i in unsaved_Contacts:
            link = "https://wa.me/" + i
            #driver  = webdriver.Chrome()
            browser.get(link)
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="action-button"]').click()
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="fallback_block"]/div/div/a').click()
            time.sleep(4)
            print("Sending message to", i)
            send_unsaved_contact_message()
            if(choice == "yes"):
                try:
                    send_attachment()
                except:
                    print('Attachment not sent.')
            if(docChoice == "yes"):
                try:
                    send_files()
                except:
                    print('Files not sent')
            time.sleep(7)
            

def send_unsaved_contact_message():
    global message
    try:
        time.sleep(7)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
    except NoSuchElementException:
        print("Failed to send message")
        return




def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ejemplo/")


def on_message(client, userdata, msg):
    global Contact, unsaved_Contacts, message
    print(msg.topic+" "+str(msg.payload))
       
    texto=msg.payload.decode("utf-8")
    print(texto)
    texto=texto.split("*")
    print(texto)
    print(int(texto[2]))
    if int(texto[2])==1:
        print("Conocido")
        Contact = [texto[0]]
        print("Conocido2")
        
    else:
        print("No Conocido")
        unsaved_Contacts=[texto[0]]
    message = [texto[1]]
    done = False
    message = "\n".join(message)
    sender()
    Contact=[]
    unsaved_Contacts=[]
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker"", 1883, 60)
print("Estamos listos")
client.loop_forever()
