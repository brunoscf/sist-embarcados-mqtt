import os
import shutil
import time

import paho.mqtt.client as mqtt
import psutil 

# Publisher Topics
TOPIC_TOTAL_RAM = "/emb/abe/total_ram"
TOPIC_RAM_IN_USE = "/emb/abe/ram_in_use"
TOPIC_CPU_USAGE = "/emb/abe/cpu_usage"
TOPIC_TOTAL_DISK_SPACE = "/emb/abe/total_disk_space"
TOPIC_USED_DISK_SPACE = "/emb/abe/used_disk_space"
TOPIC_FREE_DISK = "/emb/abe/free_disk"

# Subscriber Topics
TOPIC_DELAY_CONTROL = "/emb/abe/delay_control"
TOPIC_REBOOT = "/emb/abe/reboot"


DEFAULT_DELAY = 0  #segundos
delay = DEFAULT_DELAY


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_DELAY_CONTROL:
        global delay
        delay = int(msg.payload)
    
    elif msg.topic == TOPIC_REBOOT:
        os.system("reboot")
        #print("Rebooting")

def getInternalData():
    total_ram = round(psutil.virtual_memory().total/(1024**3), 2)
    ram_in_use = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(5)

    stat = shutil.disk_usage("/")
    total_disk_space = round(stat.total/(1024**3), 2)
    used_disk_space = round(stat.used/(1024**3), 2)
    free_disk_space = round(stat.free/(1024**3), 2)

    return (total_ram, ram_in_use, cpu_usage, 
            total_disk_space, used_disk_space, free_disk_space)


def main():
    print("\nInicializando script...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)
    
    client.subscribe(TOPIC_DELAY_CONTROL)
    client.subscribe(TOPIC_REBOOT)
    client.loop_start()

    while True:
        total_ram, ram_in_use, cpu_usage, total_disk_space, used_disk_space, free_disk_space = getInternalData()
        client.publish(TOPIC_TOTAL_RAM, total_ram)
        client.publish(TOPIC_RAM_IN_USE, ram_in_use)
        client.publish(TOPIC_CPU_USAGE, cpu_usage)
        client.publish(TOPIC_TOTAL_DISK_SPACE, total_disk_space)
        client.publish(TOPIC_USED_DISK_SPACE, used_disk_space)
        client.publish(TOPIC_FREE_DISK, free_disk_space)

        time.sleep(delay)

if __name__ == "__main__":
    main()