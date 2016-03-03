from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import csv
import os
import re
import time

class configgerer():

    def connect(self, configURL, ip):
        self.configURL = configURL
        self.ip = ip
        p = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(p)
        print("Now loading " + configURL)
        self.driver.get(self.configURL)
    
    def upgradeFirmware(self, firmware="/support/microhard/microhard_provision/1084-20.bin"):
        driver = self.driver
        print(firmware)
        #Move to Maintanence Page
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a" 
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        
    def uploadConfig(self,configurationFilePath):
        driver = self.driver
        
        #go to Maintanence window
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        
        #upload the path to the file 
        uploadConfigButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("configfile"))
        uploadConfigButtonEle.send_keys(configurationFilePath)
        
        #click the "Restore" button
        uploadConfigConfirmButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("chkconfig"))
        uploadConfigConfirmButtonEle.click()
    
        #Reconfirming the "Restore" button
        uploadConfigRestoreButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("instconfig"))
        uploadConfigRestoreButtonEle.click()    
    
    def setHostname(self, name, desc):
        driver = self.driver
        hostname=name
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = ".//*[@id='submenu']/li[2]/a" 
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        hostnameFieldXpath = "//input[@name='hostname']"
        hostanmeFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(hostnameFieldXpath))
        hostanmeFieldElement.clear()
        hostanmeFieldElement.send_keys(hostname)
        
        fieldXpath = "//input[@name='description']"
        fieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(fieldXpath))
        fieldElement.clear()
        fieldElement.send_keys(desc)

        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()
        
    def setRadiusID(self, name):
        driver = self.driver
        radiusID=name
        
        #Change to the Wireless tab
        wirelessButtonXpath = "Wireless"
        wirelessElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text(wirelessButtonXpath))
        wirelessElement.click()
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/coova-chilli.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        radiusIDFieldXpath = "coova_chilli_coova_nasid"
        radiusIDFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name(radiusIDFieldXpath))
        radiusIDFieldElement.clear()
        radiusIDFieldElement.send_keys(radiusID)
        
        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()
    
    def getFirmware(self):
        driver = self.driver
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a" 
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        return(self.driver.find_element_by_xpath("/html/body/div/form/div/div[1]/table[2]/tbody/tr[2]/td[3]").text) 
    
def main():
    ip = '192.168.168.1'
    configURL = 'http://admin:admin@' + ip + '/'
    device = configgerer()
    device.connect(configURL, ip)
    firmware = device.getFirmware()
    print(firmware)
    #device.uploadConfig("/Users/sambaruffi/Git/microhard_provision/VancouverTaxi")
    device.upgradeFirmware()
    device.setHostname("Provision", "ProvisionServerWorking")
    time.sleep(15)
    device.setRadiusID("YEAHHBB")


if __name__=='__main__':main() 