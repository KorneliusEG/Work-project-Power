import sys
import random
import threading
import time
from os.path import exists
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from timeit import default_timer as timer

timeout = 10
iteration_time = 200
url_open_fail = True
clicked = False
site_opening_started = False
work_done = False
no_address = False
work_stop = False
after_id = 0  # ID of work loop
error_count = 0
full_data = ""

tg1_p = 0.0
tg2_p = 0.0
tg3_p = 0.0
tg4_p = 0.0
tg5_p = 0.0
tg6_p = 0.0
tg_sum = 0.0

line110_1 = 0.0
line110_2 = 0.0
line110_3 = 0.0
line110_4 = 0.0
line110_5 = 0.0
line110_6 = 0.0
line110_7 = 0.0
line110_8 = 0.0
line110_9 = 0.0
line110_10 = 0.0
line110_11 = 0.0
line110_12 = 0.0
line110_sum = 0.0

line220_1 = 0.0
line220_1_minus = 0.0
line220_1_real = 0.0
line220_2 = 0.0
line220_2_minus = 0.0
line220_2_real = 0.0
line220_3 = 0.0
line220_4 = 0.0
line220_5 = 0.0
line220_sum = 0.0

u_110 = 0.0
u_220 = 0.0

all_lines_sum = 0.0
sn = 0.0


sec_arr = [] #Мгновенная мощность всех линий каждую секунду
min_arr = [] #Средняя мощность за каждую минуту внутри одного часа
period_arr = [] #Средняя мощность за каждый период внутри часа (сейчас - 15 минутки)
hour_arr = [] #Средняя мощность за каждый час
hour_plan = [] #План выдачи мощности на каждый час
energy_diff_sum = 0 #Суммарная перевыдача(+) или недовыдача(-) энергии в течение часа (накопитель)
energy_diff_hour_arr = [] #Массив данных о перевыдаче(+) или недовыдаче(-) энергии за каждый час
energy_diff_period_arr = [] #Массив данных о перевыдаче(+) или недовыдаче(-) энергии за каждый час
cur_energy_diff_sum = 0 #Текущая суммарная перевыдача(+) или недовыдача(-), вычисляемая каждую минуту
minute_counter = 0
second_counter = 0
last_min = 0
last_hour = 0
n = 0
cur_sec = 0
cur_min = 0
cur_hour = 0
first_start = True
average_calculations_allowed = False #Condition to start every minute average calculations
                                     #only after the first (cur_min%15 == 0) encounter
average_calculated = False #Защита от повторного вычисления средних значений в момент 0-ой секунды
data_restore_needed = False #Flag in time_func() to fulfill empty minutes with calculated average values if program was closed and opened again 
last_min_saved = 0
time_start = 0
request_minutes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
request_min = 60
request_value = 0


line110_1_secarr = []
line110_2_secarr = []
line110_5_secarr = []
line110_6_secarr = []

line110_1_minarr = []
line110_2_minarr = []
line110_5_minarr = []
line110_6_minarr = []

line110_1_periodarr = []
line110_2_periodarr = []
line110_5_periodarr = []
line110_6_periodarr = []

line110_1_hourarr = []
line110_2_hourarr = []
line110_5_hourarr = []
line110_6_hourarr = []

line220_1_secarr = []
line220_2_secarr = []
line220_3_secarr = []
line220_4_secarr = []

line220_1_minarr = []
line220_2_minarr = []
line220_3_minarr = []
line220_4_minarr = []

line220_1_periodarr = []
line220_2_periodarr = []
line220_3_periodarr = []
line220_4_periodarr = []

line220_1_hourarr = []
line220_2_hourarr = []
line220_3_hourarr = []
line220_4_hourarr = []

tgsum_secarr = []
tgsum_minarr = []
tgsum_periodarr = []
tgsum_hourarr = []
tg1_secarr = []
tg2_secarr = []
tg1_minarr = []
tg2_minarr = []
tg1_periodarr = []
tg2_periodarr = []
tg1_hourarr = []
tg2_hourarr = []

sn_secarr = []
sn_minarr = []
sn_periodarr = []
sn_hourarr = []

for i in range(60):
    sec_arr.append(0)
    min_arr.append(0)
    
    line110_1_secarr.append(0)
    line110_2_secarr.append(0)
    line110_5_secarr.append(0)
    line110_6_secarr.append(0)

    line220_1_secarr.append(0)
    line220_2_secarr.append(0)
    line220_3_secarr.append(0)
    line220_4_secarr.append(0)
    
    tg1_secarr.append(0)
    tg2_secarr.append(0)
    tgsum_secarr.append(0)

    line110_1_minarr.append(0)
    line110_2_minarr.append(0)
    line110_5_minarr.append(0)
    line110_6_minarr.append(0)

    line220_1_minarr.append(0)
    line220_2_minarr.append(0)
    line220_3_minarr.append(0)
    line220_4_minarr.append(0)
    
    tg1_minarr.append(0)
    tg2_minarr.append(0)
    tgsum_minarr.append(0)

    sn_secarr.append(0)
    sn_minarr.append(0)
    
    
for i in range(24):
    hour_arr.append(0)
    hour_plan.append(380.0)
    energy_diff_hour_arr.append(0)
    sn_hourarr.append(0)

for i in range(4):
    period_arr.append(0)
    energy_diff_period_arr.append(0)
    line110_1_periodarr.append(0)
    line110_2_periodarr.append(0)
    line110_5_periodarr.append(0)
    line110_6_periodarr.append(0)
    line220_1_periodarr.append(0)
    line220_2_periodarr.append(0)
    line220_3_periodarr.append(0)
    line220_4_periodarr.append(0)
    tg1_periodarr.append(0)
    tg2_periodarr.append(0)
    tgsum_periodarr.append(0)
    sn_periodarr.append(0)

CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
CHROME_PATH_ALT = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROMEDRIVER_PATH = 'chromedriver.exe'
#WINDOW_SIZE = "300,200"
options = webdriver.ChromeOptions()
#options.add_argument("--proxy-server='direct://'")
#options.add_argument("--proxy-bypass-list=*")
options.add_argument("--headless")
#options.add_argument("--window-size=%s" % WINDOW_SIZE)

service = ChromeService(executable_path = CHROMEDRIVER_PATH)
#service.creation_flags = 0x08000000

#Checking if Chrome is installed in different directories:
#'C:\Program Files\Google...' or 'C:\Program Files (x86)\Google...'

if (exists(CHROME_PATH)):
    options.binary_location = CHROME_PATH
    print(CHROME_PATH + " exists\n")
elif (exists(CHROME_PATH_ALT)):
    options.binary_location = CHROME_PATH_ALT
    print(CHROME_PATH_ALT + " exists\n")
else:
    print("Chrome not found!")
    sys.exit("Chrome not found!")

browser = webdriver.Chrome(service=service, options=options)
actions = ActionChains(browser)


def my_debug():
    print("Active threads: ", threading.activeCount())
    print("List of threads: ", threading.enumerate())
    after_id2 = root.after(2000, my_debug)

def on_closing():
    browser.quit()
    root.destroy()

def on_tab_change(event):
    tab = event.widget.tab('current')['text']
    if tab == "Выдача эл.энергии по периодам":
        hour_request_entry.select_clear()
    if tab == "Мощности по линиям и генераторам":
        site_entry.select_clear()

def stop_search():
    global after_id, work_stop, error_count
    #work_stop = True
    error_count = 0

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def string_cut(string):
    word = ""
    for c in string:
        if (c!=" " and c!="\n"):
            word += c
    return word

def string_to_array(string):
    words = []
    word = ""
    for c in string:
        if (c==" " or c=="\n"):
            if word!="":
                words.append(word)
                word = ""
        else:
            word += c
    if word:
        words.append(word)
    return words

def check_min_arr():
    global min_arr
    last_m = 0
    for i in range(60):
        if min_arr[i] > 0:
            last_m = i
    return last_m

def non_zero_minutes():
    global min_arr
    num = 0
    for i in range(60):
        if min_arr[i] > 0:
            num += 1
    return num

def check_comma(checking_string):
    new_string = list(checking_string)
    for i in range(len(new_string)):
        if new_string[i] == ",":
            new_string[i] = "."
    return "".join(new_string)

def load_data():
    global sec_arr, min_arr, period_arr, hour_arr, hour_plan, sn_minarr
    global energy_diff_sum, cur_energy_diff_sum, energy_diff_hour_arr, energy_diff_period_arr
    global average_calculations_allowed, data_restore_needed, last_min_saved
    global request_value, request_min

    data_loaded = False
    min_arr_loaded = False
    hour_arr_loaded = False
    last_min_saved = 0
    file_content = []
    c_min = time.localtime().tm_min      
    cur_time = time.strftime("%d %m %Y %H:%M:%S", time.localtime())

    if exists("current_data.dbt"):
        current_data_file = open("current_data.dbt", "r")
        file_content = current_data_file.readlines()
        current_data_file.close()
        print("Number of lines in current_data_file = ", len(file_content))
    else:
        print("Current Data File not found") 

    if len(file_content) == 12:
        min_arr_saved = string_to_array(file_content[1])
        period_arr_saved = string_to_array(file_content[2])
        energy_diff_period_arr_saved = string_to_array(file_content[3])
        hour_arr_saved = string_to_array(file_content[4])
        hour_plan_saved = string_to_array(file_content[5])
        energy_diff_hour_arr_saved = string_to_array(file_content[6])
        sn_minarr_saved = string_to_array(file_content[7])
        energy_diff_sum_saved = string_cut(file_content[8])
        cur_energy_diff_sum_saved = string_cut(file_content[9])
        request_value_saved = string_cut(file_content[10])
        request_min_saved = string_cut(file_content[11])
        data_loaded = True
        print("Data loaded successfully")
        print("Date, time in file: ", file_content[0])
    else:
        print("File has wrong number of lines")


    # Checking if DAY and HOUR in the file is the same as current       
    if cur_time[:13]==file_content[0][:13] and data_loaded == True:
        for i in range(60):
            min_arr[i] = float(min_arr_saved[i])
            sn_minarr[i] = float(sn_minarr_saved[i])
        for i in range(4):
            period_arr[i] = float(period_arr_saved[i])
            energy_diff_period_arr[i] = float(energy_diff_period_arr_saved[i])
            period_fact_labels[i].config(text = str(round(period_arr[i], 1)) + " МВт")
            period_energy_labels[i].config(text = str(round(energy_diff_period_arr[i], 1)) + " кВт*ч")
        energy_diff_sum = float(energy_diff_sum_saved)
        cur_energy_diff_sum = float(cur_energy_diff_sum_saved)
        request_value = float(request_value_saved)
        request_min = int(request_min_saved)
        period_energy_labels[c_min//15].config(text = str(round(cur_energy_diff_sum, 0)) + " кВт*ч")
        print("min_arr, sn_minarr, period_arr, energy_diff_period_arr, cur_energy_diff_sum - loaded")
        min_arr_loaded = True
        average_calculations_allowed = True
    else:
        print("Current time (hour) is different than in the file")

    # Checking if DAY in the file is the same as current
    if cur_time[:10]==file_content[0][:10] and data_loaded == True:
        for i in range(len(hour_arr_saved)):
            hour_arr[i] = float(hour_arr_saved[i])
            day_hour_fact_labels[i].config(text = str(round(hour_arr[i], 1)) + " МВт")
            hour_plan[i] = float(hour_plan_saved[i])
            energy_diff_hour_arr[i] = float(energy_diff_hour_arr_saved[i])
        print("hour_arr, hour_plan, energy_diff_hour_arr - loaded")
        hour_arr_loaded = True
    else:
        print("Current date (day) is different than in the file")
    
        

    if min_arr_loaded:
        last_min_saved = check_min_arr()
        print("last_min_saved: ", last_min_saved)
        if (c_min-last_min_saved) < 30:
            data_restore_needed = True
            print("data_restore_needed = True")
    #Доделать: если пауза произошла между разными часами       

def save_data():
    global sec_arr, min_arr, period_arr, hour_arr, hour_plan, sn_minarr
    global energy_diff_sum, cur_energy_diff_sum, energy_diff_hour_arr, energy_diff_period_arr
    global request_value, request_min

    cur_time = time.strftime("%d %m %Y %H:%M:%S", time.localtime())

    try:
        current_data_file = open("current_data.dbt", "w")
        current_data_file.write(cur_time + "\n")        # index 0  Date and Time "01 02 2023 10:35:00"
        for value in min_arr:                           # index 1  min_arr
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        for value in period_arr:                        # index 2  period_arr
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        for value in energy_diff_period_arr:            # index 3  energy_diff_period_arr
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        for value in hour_arr:                          # index 4  hour_arr
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        for value in hour_plan:                         # index 5  hour_plan
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        for value in energy_diff_hour_arr:              # index 6  energy_diff_hour_arr
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        for value in sn_minarr:                         # index 7 sn_minarr
            current_data_file.write(str(value)+" ")
        current_data_file.write("\n")

        current_data_file.write(str(energy_diff_sum) + "\n")    # index 8  energy_diff_sum
        current_data_file.write(str(cur_energy_diff_sum) + "\n")# index 9  cur_energy_diff_sum
        current_data_file.write(str(request_value) + "\n")      # index 10  request_value
        current_data_file.write(str(request_min) + "\n")        # index 11  request_min
        
        current_data_file.close()
    except:
        pass
    
def show_plan():
    global hour_plan, cur_energy_diff_sum, sn_minarr, last_min, request_min, request_value
    
    c_hour = time.localtime().tm_hour
    c_min = time.localtime().tm_min
    hour_plan_label.config(text = str(hour_plan[c_hour]) + " МВт")
    period_label1.config(text = "Время\n\n{}:00-{}:00".format(c_hour, c_hour+1))
    
    for i in range(4):
        period_plan_labels[i].config(text = str(hour_plan[c_hour]) + " МВт")
    
    for i in range(24):
        day_hour_plan_entry[i].delete(0, END)
        day_hour_plan_entry[i].insert(0, str(hour_plan[i]))

    if c_min >= request_min:
        cur_energy_diff_sum -= request_value*1000
        request_value = 0
        request_min = c_min

    if request_min < 59:
        r_target = hour_plan[c_hour] - ((cur_energy_diff_sum - request_value*1000) / 1000 * 60 / (60 - request_min)) + sn_minarr[last_min]
        request_target_label.config(text = str(round(r_target, 1)) + " МВт", bg='#ffc')
        request_time_label.config(text = "{}:{}-{}:00".format(str(c_hour), str(request_min), str(c_hour+1)), bg='#ffc')
   
        
    p_target = hour_plan[c_hour] - (cur_energy_diff_sum / 1000 * 60 / (60 - c_min))
    power_target_label.config(text = str(round(p_target, 1)) + " МВт")

    g_target = p_target + sn_minarr[last_min]
    generation_target_label.config(text = str(round(g_target, 1)) + " МВт")

    for i in range(4):
        period_energy_labels[i].config(fg='#000', font=('Arial', 14), width=16, borderwidth=2)
        period_fact_labels[i].config(fg='#000', font=('Arial', 14), borderwidth=2)
    period_energy_labels[last_min//15].config(fg='#00a', font=('Arial', 16, 'bold'), width=14, borderwidth=4)
    period_fact_labels[last_min//15].config(fg='#00a', font=('Arial', 14, 'bold'), borderwidth=4)
    
   
def test_func():
    global tg1_p, tg2_p, tg3_p, tg4_p, tg5_p, tg6_p
    global line110_1, line110_2, line110_3, line110_4, line110_5, line110_6, line110_7, line110_8, line110_9, line110_10, line110_11, line110_12
    global line220_1, line220_2, line220_3, line220_4, line220_5, u_110, u_220
    global work_done, work_stop
      
    tg1_p = round(random.uniform(80, 100), 2)
    tg2_p = round(random.uniform(80, 100), 2)
    tg3_p = round(random.uniform(80, 100), 2)
    tg4_p = round(random.uniform(80, 100), 2)
    tg5_p = round(random.uniform(80, 100), 2)
    tg6_p = round(random.uniform(80, 100), 2)

    line110_1 = round(random.uniform(10, 30), 2)
    line110_2 = round(random.uniform(10, 30), 2)
    line110_3 = round(random.uniform(10, 30), 2)
    line110_4 = round(random.uniform(10, 30), 2)
    line110_5 = round(random.uniform(10, 30), 2)
    line110_6 = round(random.uniform(10, 30), 2)
    line110_7 = round(random.uniform(10, 30), 2)
    line110_8 = round(random.uniform(10, 30), 2)
    line110_9 = round(random.uniform(10, 30), 2)
    line110_10 = round(random.uniform(10, 30), 2)
    line110_11 = round(random.uniform(10, 30), 2)
    line110_12 = round(random.uniform(10, 30), 2)

    line220_1 = round(random.uniform(10, 30), 2)
    line220_2 = round(random.uniform(10, 30), 2)
    line220_3 = round(random.uniform(10, 30), 2)
    line220_4 = round(random.uniform(10, 30), 2)

    u_110 = round(random.uniform(105, 115), 4)
    u_220 = round(random.uniform(215, 230), 4)


    if not work_stop:
        work_done = True
    else:
        work_done = False
        
    #calculations()
    #after_id = root.after(iteration_time, test_func)

def time_func():
    global cur_sec, cur_min, cur_hour, last_min, last_hour, time_start, average_calculated, average_calculations_allowed
    global sec_arr, min_arr, period_arr, hour_arr, hour_plan, minute_counter, second_counter, data_restore_needed, last_min_saved
    global all_lines_sum, energy_diff_sum, cur_energy_diff_sum, energy_diff_hour_arr, energy_diff_period_arr, request_value
    global line110_1, line110_1_secarr, line110_1_minarr, line110_1_periodarr, line110_1_hourarr
    global line110_2, line110_2_secarr, line110_2_minarr, line110_2_periodarr, line110_2_hourarr
    global line110_5, line110_5_secarr, line110_5_minarr, line110_5_periodarr, line110_5_hourarr
    global line110_6, line110_6_secarr, line110_6_minarr, line110_6_periodarr, line110_6_hourarr
    global line220_3, line220_3_secarr, line220_3_minarr, line220_3_periodarr, line220_3_hourarr
    global line220_4, line220_4_secarr, line220_4_minarr, line220_4_periodarr, line220_4_hourarr
    global line220_1_real, line220_1_secarr, line220_1_minarr, line220_1_periodarr, line220_1_hourarr
    global line220_2_real, line220_2_secarr, line220_2_minarr, line220_2_periodarr, line220_2_hourarr
    global tg1_p, tg1_secarr, tg1_minarr, tg1_periodarr, tg1_hourarr
    global tg2_p, tg2_secarr, tg2_minarr, tg2_periodarr, tg2_hourarr
    global tg_sum, tgsum_secarr, tgsum_minarr, tgsum_periodarr, tgsum_hourarr
    global sn, sn_secarr, sn_minarr, sn_periodarr, sn_hourarr
    

    t1 = timer()
    #Данные о текущем РЕАЛЬНОМ времени на основе которых будут браться соответствующие
    #индексы массивов секунд, минут и часов
    now_time = time.localtime()
    cur_sec = now_time.tm_sec
    cur_min = now_time.tm_min
    cur_hour = now_time.tm_hour
    time_dif = time.time() - time_start

    
       
    # Вычисляем средние значения за минуту/период/час если:
    # 1) Сейчас момент нулевой секунды;
    # 2) С момента старта программы прошла одна полная минута;
    # 3) Средние значения еще не были вычислены и записаны в массивы (для предотвращения
    #    повторного вычисления)
    if cur_sec == 0 and time_dif >= 60 and not average_calculated:
        #print("Time_dif = ", time_dif)
        k1 = timer()
        ##########for testing only
        #cur_min += 1
        #minute_counter += 1
        #if cur_min == 60:
        #    cur_min = 0
        ##########for testing only


        if cur_min%15 == 1:
            average_calculations_allowed = True
        
        #Clear data from the past hour
        if cur_min == 1:
            hour_fact_label.config(text = "0.0 МВт")
            hour_energy_label.config(text = "0.0 кВт*ч")
            for i in range(4):
                period_fact_labels[i].config(text = "0.0 МВт")
                period_energy_labels[i].config(text = "0.0 кВт*ч")
                
        #calculate average power for last minute
        min_arr[last_min] = sum(sec_arr) / 60
        
        line110_1_minarr[last_min] = sum(line110_1_secarr) / 60
        line110_2_minarr[last_min] = sum(line110_2_secarr) / 60
        line110_5_minarr[last_min] = sum(line110_5_secarr) / 60
        line110_6_minarr[last_min] = sum(line110_6_secarr) / 60
        line220_1_minarr[last_min] = sum(line220_1_secarr) / 60
        line220_2_minarr[last_min] = sum(line220_2_secarr) / 60
        line220_3_minarr[last_min] = sum(line220_3_secarr) / 60
        line220_4_minarr[last_min] = sum(line220_4_secarr) / 60
        tg1_minarr[last_min] = sum(tg1_secarr) / 60
        tg2_minarr[last_min] = sum(tg2_secarr) / 60
        tgsum_minarr[last_min] = sum(tgsum_secarr) / 60
        sn_minarr[last_min] = sum(sn_secarr) / 60

        #If program was stopped (or closed) and started again and less than 30 minutes passed we fill lost minutes
        #with calculated average values
        if data_restore_needed:
            print("min_arr[{}] = {}".format(str(last_min_saved), str(min_arr[last_min_saved])))
            print("cur_energy_diff_sum = {}".format(str(cur_energy_diff_sum)))
            for i in range(last_min_saved+1, last_min):
                min_arr[i] = (min_arr[last_min_saved] + min_arr[last_min])/2
                cur_energy_diff_sum += (min_arr[i] - hour_plan[last_hour])*1000/60
                print("min_arr[{}] = {}".format(str(i), str(min_arr[i])))
                print("cur_energy_diff_sum = {}".format(str(cur_energy_diff_sum)))
            time_start = 0
            time_dif = 1000
            data_restore_needed = False

        #Current energy_diff_sum and current average power output, calculating and refreshing labels every minute
        if average_calculations_allowed:
            cur_energy_diff_sum += (min_arr[last_min] - hour_plan[last_hour])*1000/60
            print("\ncur_energy_diff_sum = ", cur_energy_diff_sum)
            period_energy_labels[last_min//15].config(text = str(round(cur_energy_diff_sum, 0)) + " кВт*ч")
            cur_average_power = sum(min_arr[(last_min//15)*15:]) / (last_min + 1 - (last_min//15)*15)
            print("cur_average_power = ", cur_average_power)
            period_fact_labels[last_min//15].config(text = str(round(cur_average_power, 1)) + " МВт")
        
        #for i in range(60):
        #    print(sec_arr[i])
        print("min: {} min_avg: {}".format(str(last_min), min_arr[last_min]))
        print(line110_1_minarr[last_min])
        print(line110_2_minarr[last_min])
        print(line110_5_minarr[last_min])
        print(line110_6_minarr[last_min])
        print(line220_1_minarr[last_min])
        print(line220_2_minarr[last_min])
        print(line220_3_minarr[last_min])
        print(line220_4_minarr[last_min])
        print(tg1_minarr[last_min])
        print(tg2_minarr[last_min])
        print(tgsum_minarr[last_min])
        print(sn_minarr[last_min])
        show_plan()
           

        #calculate average power for last 15 minutes        
        if (cur_min%15 == 0) and (time_dif >= 900):
                        
            if cur_min != 0:
                period_arr[last_min//15] = sum(min_arr[cur_min-15:cur_min]) / 15
                
                line110_1_periodarr[last_min//15] = sum(line110_1_minarr[cur_min-15:cur_min]) / 15
                line110_2_periodarr[last_min//15] = sum(line110_2_minarr[cur_min-15:cur_min]) / 15
                line110_5_periodarr[last_min//15] = sum(line110_5_minarr[cur_min-15:cur_min]) / 15
                line110_6_periodarr[last_min//15] = sum(line110_6_minarr[cur_min-15:cur_min]) / 15
                line220_1_periodarr[last_min//15] = sum(line220_1_minarr[cur_min-15:cur_min]) / 15
                line220_2_periodarr[last_min//15] = sum(line220_2_minarr[cur_min-15:cur_min]) / 15
                line220_3_periodarr[last_min//15] = sum(line220_3_minarr[cur_min-15:cur_min]) / 15
                line220_4_periodarr[last_min//15] = sum(line220_4_minarr[cur_min-15:cur_min]) / 15
                tg1_periodarr[last_min//15] = sum(tg1_minarr[cur_min-15:cur_min]) / 15
                tg2_periodarr[last_min//15] = sum(tg2_minarr[cur_min-15:cur_min]) / 15
                tgsum_periodarr[last_min//15] = sum(tgsum_minarr[cur_min-15:cur_min]) / 15
                sn_periodarr[last_min//15] = sum(sn_minarr[cur_min-15:cur_min]) / 15

                print(" ")
                print(time.strftime("%d %m %Y %H:%M:%S", time.localtime()))
                print("period: {} period_avg: {}".format(str(last_min//15), period_arr[last_min//15]))
                period_fact_labels[last_min//15].config(text = str(round(period_arr[last_min//15], 1)) + " МВт")

                print(line110_1_periodarr[last_min//15])
                print(line110_2_periodarr[last_min//15])
                print(line110_5_periodarr[last_min//15])
                print(line110_6_periodarr[last_min//15])
                print(line220_1_periodarr[last_min//15])
                print(line220_2_periodarr[last_min//15])
                print(line220_3_periodarr[last_min//15])
                print(line220_4_periodarr[last_min//15])
                print(tg1_periodarr[last_min//15])
                print(tg2_periodarr[last_min//15])
                print(tgsum_periodarr[last_min//15])
                print(sn_periodarr[last_min//15])


                #Calculating energy surplus(+) or deficit(-) relative to the plan. Cumulative value
                energy_diff_sum += ((period_arr[last_min//15] - hour_plan[cur_hour])*1000/4)
                energy_diff_period_arr[last_min//15] = cur_energy_diff_sum
                #period_energy_labels[last_min//15].config(text = str(round(cur_energy_diff_sum, 0)) + " кВт*ч")


                #TARGET POWER OUTPUT
                power_target = hour_plan[cur_hour] - (cur_energy_diff_sum / 1000 * 60 / (60 - cur_min))
                power_target_label.config(text = str(round(power_target, 1)) + " МВт")

                generation_target = power_target + sn_minarr[last_min]
                generation_target_label.config(text = str(round(generation_target, 1)) + " МВт")
                
            elif cur_min == 0:
                ##############FOR TESTING PURPOSES ONLY
                #cur_hour += 1
                #if cur_hour == 24:
                #    cur_hour = 0
                ##############FOR TESTING PURPOSES ONLY
                 
                period_arr[3] = sum(min_arr[45:60]) / 15
                
                line110_1_periodarr[3] = sum(line110_1_minarr[45:60]) / 15
                line110_2_periodarr[3] = sum(line110_2_minarr[45:60]) / 15
                line110_5_periodarr[3] = sum(line110_5_minarr[45:60]) / 15
                line110_6_periodarr[3] = sum(line110_6_minarr[45:60]) / 15
                
                line220_1_periodarr[3] = sum(line220_1_minarr[45:60]) / 15
                line220_2_periodarr[3] = sum(line220_2_minarr[45:60]) / 15
                line220_3_periodarr[3] = sum(line220_3_minarr[45:60]) / 15
                line220_4_periodarr[3] = sum(line220_4_minarr[45:60]) / 15
                tg1_periodarr[3] = sum(tg1_minarr[45:60]) / 15
                tg2_periodarr[3] = sum(tg2_minarr[45:60]) / 15
                tgsum_periodarr[3] = sum(tgsum_minarr[45:60]) / 15
                sn_periodarr[3] = sum(sn_minarr[45:60]) / 15

                print(" ")
                print(time.strftime("%d %m %Y %H:%M:%S", time.localtime()))
                print("period: {} period_avg: {}".format(3, period_arr[3]))
                print("period_arr:")
                print(period_arr)
                period_fact_labels[3].config(text = str(round(period_arr[3], 1)) + " МВт")

                print(line110_1_periodarr[3])
                print(line110_2_periodarr[3])
                print(line110_5_periodarr[3])
                print(line110_6_periodarr[3])
                print(line220_1_periodarr[3])
                print(line220_2_periodarr[3])
                print(line220_3_periodarr[3])
                print(line220_4_periodarr[3])
                print(tg1_periodarr[3])
                print(tg2_periodarr[3])
                print(tgsum_periodarr[3])
                print(sn_periodarr[3])

                
                # Calculate average power for last hour
                hour_average = sum(min_arr)/non_zero_minutes()
                print("Hour average by sum(min_arr): ", hour_average)
                hour_arr[last_hour] = hour_average
                hour_fact_label.config(text = str(round(hour_average, 1)) + " МВт")
                day_hour_fact_labels[last_hour].config(text = str(round(hour_average, 1)) + " МВт")

                #Calculating energy surplus(+) or deficit(-) relative to the plan. Cumulative value
                energy_diff_sum += ((period_arr[3] - hour_plan[last_hour])*1000/4)
                energy_diff_period_arr[3] = cur_energy_diff_sum
                #period_energy_labels[3].config(text = str(round(energy_diff_sum, 0)) + " кВт*ч")
                hour_energy_label.config(text = str(round(cur_energy_diff_sum, 0)) + " кВт*ч")
                print("Hour cur_energy_diff_sum: ", cur_energy_diff_sum)
                print("Energy_diff_period_arr[]: ", energy_diff_period_arr)

                #TARGET POWER OUTPUT for the new hour (previous hour deficit is ignored)
                power_target_label.config(text = str(round(hour_plan[cur_hour], 1)) + " МВт")

                generation_target = hour_plan[cur_hour] + sn_minarr[last_min]
                generation_target_label.config(text = str(round(generation_target, 1)) + " МВт")
                
                #Saving the data about energy surplus(+) or deficit(-) for an hour and then deleting it,
                #because new hour has started
                energy_diff_hour_arr[last_hour] = cur_energy_diff_sum
                                
                print("Hour_arr: ")
                print(hour_arr)

        if cur_min == 0:
            #Deleting data in minute array, period array, energy_diff_sum, cur_energy_diff_sum because new hour has started
            energy_diff_sum = 0
            cur_energy_diff_sum = 0
            request_value = 0
            request_min = 60
            request_target_label.config(text = " ", bg='white')
            request_time_label.config(text = " ", bg='white')
            for i in range(60):
                min_arr[i] = 0
            for i in range(4):
                period_arr[i] = 0
                energy_diff_period_arr[i] = 0
            if cur_hour == 1:
                for i in range(1, 24):
                    hour_arr[i] = 0
                    day_hour_fact_labels[i].config(text = " ")
                    
        average_calculated = True
        save_data()
        print("Time: ", timer()-k1)
        
    elif cur_sec != 0:
        last_min = cur_min
        last_hour = cur_hour
        average_calculated = False

    sec_arr[cur_sec] = all_lines_sum
    line110_1_secarr[cur_sec] = float(line110_1)
    line110_2_secarr[cur_sec] = float(line110_2)
    line110_5_secarr[cur_sec] = float(line110_5)
    line110_6_secarr[cur_sec] = float(line110_6)
    line220_1_secarr[cur_sec] = line220_1_real
    line220_2_secarr[cur_sec] = line220_2_real
    line220_3_secarr[cur_sec] = float(line220_3)
    line220_4_secarr[cur_sec] = float(line220_4)
    tg1_secarr[cur_sec] = float(tg1_p)
    tg2_secarr[cur_sec] = float(tg2_p)
    tgsum_secarr[cur_sec] = tg_sum
    sn_secarr[cur_sec] = sn
    #print("sec: {} value: {}".format(str(cur_sec), sec_arr[cur_sec]))
    

def calculations():
    global tg1_p, tg2_p, tg3_p, tg4_p, tg5_p, tg6_p, tg_sum
    global line110_1, line110_2, line110_3, line110_4, line110_5, line110_6, line110_7, line110_8, line110_9, line110_10, line110_11, line110_12, line110_sum
    global line220_1, line220_1_minus, line220_2, line220_2_minus, line220_3, line220_4, line220_5, line220_sum, u_110, u_220
    global line220_1_real, line220_2_real, sn
    global all_lines_sum, error_count, after_id, site_opening_started
    global full_data

    a1 = timer()

    # Processing of received string with full table of data

    words = []
    word = ""
    if len(full_data) > 420:    # Adjust this condition to actual length of full_data
        for c in full_data:
            if (c==" " or c=="\n"):
                if word!="":
                    words.append(word)
                    word = ""
            else:
                word += c
        words.append(word)

##    for i in range(len(words)):
##        print(i, words[i])
##
##    print("len(words) = ", len(words))
##    print("len(full_data) = ", len(full_data))
        
    if len(words) == 62:
        tg1_p = float(words[7])/5
        tg2_p = float(words[8])/5
        tg3_p = float(words[13])
        tg4_p = float(words[14])
        tg5_p = float(words[19])/5
        tg6_p = float(words[20])/5

        line110_1 = float(words[25])/20
        line110_2 = float(words[26])/20
        line110_3 = float(words[31])/50
        line110_4 = float(words[32])/50
        line110_5 = float(words[37])/100
        line110_6 = float(words[38])/100
        line110_7 = float(words[43])/300
        line110_8 = float(words[44])/300
        #line110_9 = words[50]
        #line110_10 = words[51]
        #line110_11 = words[44]
                
        line220_1 = float(words[50])
        line220_2 = float(words[51])
        line220_3 = float(words[57])
        line220_4 = float(words[58])
        #line220_5 = words[150]

        #u_110 = words[194]
        #u_220 = words[176]
    
    tg1_value_label.config(text = str(round(tg1_p,4)) + " МВт")
    tg2_value_label.config(text = str(round(tg2_p,4)) + " МВт")
    tg3_value_label.config(text = str(round(tg3_p,4)) + " МВт")
    tg4_value_label.config(text = str(round(tg4_p,4)) + " МВт")
    tg5_value_label.config(text = str(round(tg5_p,4)) + " МВт")
    tg6_value_label.config(text = str(round(tg6_p,4)) + " МВт")
    tg_sum = tg1_p + tg2_p + tg3_p + tg4_p + tg5_p + tg6_p
    tg_sum_value_label.config(text = str(round(tg_sum, 4)) + " МВт")
    generation_current_label.config(text = str(round(tg_sum, 2)) + " МВт")
    

    line110_1_value_label.config(text = str(round(line110_1,4)) + " МВт")
    line110_2_value_label.config(text = str(round(line110_2,4)) + " МВт")
    line110_3_value_label.config(text = str(round(line110_3,4)) + " МВт")
    line110_4_value_label.config(text = str(round(line110_4,4)) + " МВт")
    line110_5_value_label.config(text = str(round(line110_5,4)) + " МВт")
    line110_6_value_label.config(text = str(round(line110_6,4)) + " МВт")
    line110_7_value_label.config(text = str(round(line110_7,4)) + " МВт")
    line110_8_value_label.config(text = str(round(line110_8,4)) + " МВт")
    line110_9_value_label.config(text = str(round(line110_9,4)) + " МВт")
    line110_10_value_label.config(text = str(round(line110_10,4)) + " МВт")
    line110_11_value_label.config(text = str(round(line110_11,4)) + " МВт")
    line110_12_value_label.config(text = str(round(float(line110_12),2)) + " МВт")

    #110kV LINES SUM   
    line110_sum = (line110_1 + line110_2 + line110_3 + line110_4 + line110_5
                          + line110_6 + line110_7 + line110_8 + line110_9
                          + line110_10 + line110_11 + float(line110_12))
    line110_sum_value_label.config(text = str(round(line110_sum, 4)) + " МВт")

    line220_1_real = line220_1 - line220_1_minus * 7612
    line220_1_value_label.config(text = str(round(line220_1_real,4)) + " МВт")

    line220_2_real = line220_2 - line220_2_minus * 7612
    line220_2_value_label.config(text = str(round(line220_2_real,4)) + " МВт")
    
    line220_3_value_label.config(text = str(round(float(line220_3),4)) + " МВт")
    line220_4_value_label.config(text = str(round(float(line220_4),4)) + " МВт")
    line220_5_value_label.config(text = str(round(float(line220_5),4)) + " МВт")

    #220kV LINES SUM 
    line220_sum = line220_1_real + line220_2_real + line220_3 + line220_4 + line220_5
    line220_sum_value_label.config(text = str(round(line220_sum, 4)) + " МВт")

    #ALL LINES SUM
    all_lines_sum = line110_sum + line220_sum
    all_lines_sum_value_label.config(text = str(round(all_lines_sum, 4)) + " МВт")
    power_current_label.config(text = str(round(all_lines_sum, 2)) + " МВт")

    #СОБСТВЕННЫЕ НУЖДЫ + ПОТРЕБИТЕЛИ 6кВ + ПОТЕРИ
    sn = tg_sum - all_lines_sum
    sn_value_label.config(text = str(round(sn, 4)) + " МВт")
    
    #VOLTAGE 110kV, 220kV
    u_110_value_label.config(text = str(round(float(u_110),2)) + " кВ")
    u_220_value_label.config(text = str(round(float(u_220),2)) + " кВ")

    time_func()

    a2 = timer()
    a3 = a2 - a1
    
    #print("Calculations() took: ", a3)
    #mystr = (str(after_id) + "\nError count: " + str(error_count) + "\nThreads count: "
    #          + str(threading.active_count()) + "\nSite opening started: " + str(site_opening_started))
    #t.insert(END, mystr)
      

def get_start():
    global after_id, site_opening_started, error_count, no_address, work_stop
    error_count = 0
    work_stop = True
    site_name = site_entry.get()
    
    if not site_opening_started:
        if site_name:
            no_address = False
            site_opening_started = True
            print("site_opening_started")
            site_opening_thread = threading.Thread(target=start, args=(site_name,)) #Separate thread for site opening
            site_opening_thread.start()
        else:
            no_address = True
    else:
        print("Site opening already started! Wait please.")
        
    
def start(target_site):
    global url_open_fail, site_opening_started, clicked, work_stop, first_start, time_start, last_min
    
    print("Target site: " + target_site)
    clicked = False
    url_open_fail = True
    try:
        browser.get(target_site)
        url_open_fail = False
        
    except:

        t.insert(END, "Can't open URL\n")
        url_open_fail = True
        site_opening_started = False
        clicked = True
    print(url_open_fail)
   
# Waiting for the page to be loaded and checking conditions

    #try:
        #WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "tabs__content")))
    #except (TimeoutException, WebDriverException):
        #print("Can't open the page")
        #news.append("Can't open the page")
        #browser.quit()
        #sys.exit()

# Clicking on a needed tab
    if not clicked:
        try:
            target_tab = browser.find_element(By.ID, "ui-id-5")
            actions.move_to_element(target_tab)
            actions.click(target_tab)
            actions.perform()
            clicked = True
                        
        except:
            pass

    try:
        browser.switch_to.frame(browser.find_element(By.XPATH, "//*[@id='main_frame']"))
        browser.switch_to.frame(browser.find_element(By.XPATH, "/html/body/table/tbody/tr/td/iframe"))
        print("Frame found!")
    except:
        print("Frame NOT found!")
        
    time.sleep(1)
    load_data()    
    work_stop = False

    if first_start:
        last_min = time.localtime().tm_min
        time_start = time.time()
        first_start = False
            
    #if not url_open_fail:
    work_thread_start()
    print(time.strftime("%d %m %Y %H:%M:%S", time.localtime()))
    show_plan()
    site_opening_started = False
    
    #test_func()


# Function that will collect needed data every %iteration_time% seconds
def work():
    global tg1_p, tg2_p, tg3_p, tg4_p, tg5_p, tg6_p
    global line110_1, line110_2, line110_3, line110_4, line110_5, line110_6, line110_7, line110_8, line110_9, line110_10, line110_11, line110_12
    global line220_1, line220_2, line220_3, line220_4, line220_5, u_110, u_220
    global error_count, iteration_time, after_id, work_done, work_stop
    global full_data
    global cur_sec
    t1 = 0
    t2 = 0
    full_data = ''
    
    #print("Work started...")
    try:
        t1 = timer()
        full_data = browser.find_element(By.XPATH, "//*[@id='mainDiv']/table/tbody/tr/td[1]/table/tbody/tr[6]/td/table").text

    except:
        error_count += 1
        pass
    
    #print("Work() took: ", (timer()-t1))
    #print("Work finished.")
    if not work_stop:
        work_done = True
    else:
        work_done = False

def get_hour_request():
    global cur_energy_diff_sum, request_value, request_min
    selected_min = hour_request_combobox.get()
    request_string = check_comma(hour_request_entry.get())

    if not is_integer(selected_min):
        showinfo(
            title="Сообщение",
            message="Вы ввели не целое число секунд\nлибо нечисловое значение: {}".format(selected_min),
        )
        return
    
    if not is_float(request_string):
        showinfo(
            title="Сообщение",
            message="Вы ввели нечисловое значение заявки: {}".format(request_string)
        )
        return

    if float(request_string) >= 1000:
        showinfo(
            title="Сообщение",
            message="Введите значение без нулей. Например:\nЕсли заявка 30 000 кВт*ч, то введите 30"
        )
        return
    
    request_min = int(selected_min)
    print(request_min)
    request_value = float(request_string)
    print(request_value)
    
    
        
    #Два варианта:
    #1) Заявка в форме кВт*ч сразу прибавляется к текущему избытку/недостатку и сразу влияет на задание по выдаче и генерации
    #cur_energy_diff_sum -= request_value*1000
    hour_request_entry.delete(0, END)
    
    #2) Заявка вступает в силу только в заданную минуту и только тогда изменяется задание по выдаче и генерации
    c_hour = time.localtime().tm_hour
    c_min = time.localtime().tm_min
    show_plan()
        #Recalculate energy_diff_sum IF NEEDED ! If new plan is only for the REST of the hour, then DO NOT recalculate
##        if energy_diff_sum != 0 and c_period >= 1:
##            end_min = c_period*15
##            new_average = sum(min_arr[:end_min]) / end_min
##            energy_diff_sum = (new_average - hour_plan[c_hour])*1000*c_period/4
##            period_arr[c_period-1] = energy_diff_sum
##            period_energy_labels[c_period-1].config(text=str(round(energy_diff_sum),0))

def get_day_plan():
    global hour_plan
    for i in range(24):
        p = day_hour_plan_entry[i].get()
        if is_float(p):
            hour_plan[i] = float(p)
    show_plan()
        
    
def work_thread_start():
    global work_done, work_stop
    work_done = False
    work_thread = threading.Thread(target=work, args=())
    work_thread.start()

def work_loop():
    global work_done, after_id, iteration_time, site_opening_started, url_open_fail, no_address, work_stop
    t.delete(1.0, END)
    t.config(fg='#000')
    if no_address:
        mystr = "Введите адрес сервера: http://192.168.1.2\n"
        t.insert(END, mystr)
    if site_opening_started:
        mystr = "Идёт подключение к серверу...\n"
        t.insert(END, mystr)
    if url_open_fail:
        mystr = "Нет связи с сервером Телеметрии\n"
        t.config(fg='#f00')
        t.insert(END, mystr)
    else:
        t.config(fg='#00f')
        mystr = "Связь с сервером Телеметрии установлена\n"
        t.insert(END, mystr)
    mystr = (str(after_id) + " | Error count: " + str(error_count) + "\nThreads count: "
              + str(threading.active_count()) + " | Site opening started: " + str(site_opening_started))
    t.insert(END, mystr)
    if work_done and not work_stop:
        calculations()
        work_thread_start()

    #mystr = "\n! Не закрывайте браузер Chrome и служебное \nокно программы!"
    #t.insert(END, mystr)

#Данная функция будет выполняться в бесконечном цикле с временем итерации %iteration_time%
#By storing the unique identifiers returned by the after() method, you can have fine-grained control
#over each scheduled event. You can use these identifiers to cancel or modify specific events using
#the after_cancel() or after() methods.
    after_id = root.after(iteration_time, work_loop)
    


# Creating a window for our program
root = Tk()
root.title("Программа отображения мощности по генераторам и линиям")
root.config(padx=10, pady=10)
root.geometry('+%d+%d'%(0,0))
root.maxsize(2000, 1200)

s = ttk.Style()
s.configure('TNotebook.Tab', font=('Times New Roman', '14'))

tab_root = ttk.Notebook(root)

tab1 = Frame(tab_root)
tab2 = Frame(tab_root)

tab2.rowconfigure(1, weight=5)

tab_root.add(tab1, text="Мощности по линиям и генераторам")
tab_root.add(tab2, text="Выдача эл.энергии по периодам")

form_frame = LabelFrame(tab1, text="Данные для загрузки")
form_frame.grid(row=0, column=0, columnspan=2, sticky="nw", padx=5, pady=5)

site_label = Label(form_frame, text="Введите адрес сервера: ")
site_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

site_entry = Entry(form_frame, width=25)
site_entry.grid(row=0, column=1, sticky="w", padx=(0,10))
site_entry.insert(0, "https://www.profinance.ru/quote_show.php")

#ГЕНЕРАТОРЫ
generators_frame = LabelFrame(tab1, text="Генераторы", font=('Times New Roman', 12))
generators_frame.grid(row=1, rowspan=2, column=0, sticky="nw", padx = 5, pady = 2)

tg1_label = Label(generators_frame, text="ТГ-1: ", font=('Arial', 13))
tg1_label.grid(row=0, column=0, sticky = "w", padx = 5, pady = 2)
tg1_value_label = Label(generators_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
tg1_value_label.grid(row=0, column=1, sticky = "w", padx = 5, pady = 2)

tg2_label = Label(generators_frame, text="ТГ-2: ", font=('Arial', 13))
tg2_label.grid(row=1, column=0, sticky = "w", padx = 5, pady = 2)
tg2_value_label = Label(generators_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
tg2_value_label.grid(row=1, column=1, sticky = "w", padx = 5, pady = 2)

tg3_label = Label(generators_frame, text="ТГ-3: ", font=('Arial', 13))
tg3_label.grid(row=2, column=0, sticky = "w", padx = 5, pady = 2)
tg3_value_label = Label(generators_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
tg3_value_label.grid(row=2, column=1, sticky = "w", padx = 5, pady = 2)

tg4_label = Label(generators_frame, text="ТГ-4: ", font=('Arial', 13))
tg4_label.grid(row=3, column=0, sticky = "w", padx = 5, pady = 2)
tg4_value_label = Label(generators_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
tg4_value_label.grid(row=3, column=1, sticky = "w", padx = 5, pady = 2)

tg5_label = Label(generators_frame, text="ТГ-5: ", font=('Arial', 13))
tg5_label.grid(row=4, column=0, sticky = "w", padx = 5, pady = 2)
tg5_value_label = Label(generators_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
tg5_value_label.grid(row=4, column=1, sticky = "w", padx = 5, pady = 2)

tg6_label = Label(generators_frame, text="ТГ-6: ", font=('Arial', 13))
tg6_label.grid(row=5, column=0, sticky = "w", padx = 5, pady = 2)
tg6_value_label = Label(generators_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
tg6_value_label.grid(row=5, column=1, sticky = "w", padx = 5, pady = 2)

tg_sum_label = Label(generators_frame, text="Суммарная \nP генераторов: ", font=('Arial', 14), justify = LEFT)
tg_sum_label.grid(row=6, column=0, sticky = "w", padx = 5, pady = 5)
tg_sum_value_label = Label(generators_frame, text="0.0", font=('Arial', 14), width = 10, anchor="w")
tg_sum_value_label.grid(row=6, column=1, sticky = "w", padx = 5, pady = 5)

# ЛИНИИ 110 кВ
lines110_frame = LabelFrame(tab1, text="Линии 110кВ", font=('Times New Roman', 12))
lines110_frame.grid(row=1, rowspan=2, column=1, sticky="nw", padx = 5, pady = 2)

line110_1_label = Label(lines110_frame, text="ВЛ Караганда - 1: ", font=('Arial', 13))
line110_1_label.grid(row=0, column=0, sticky = "w", padx = 5, pady = 2)
line110_1_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_1_value_label.grid(row=0, column=1, sticky = "w", padx = 5, pady = 2)

line110_2_label = Label(lines110_frame, text="ВЛ Караганда - 2: ", font=('Arial', 13))
line110_2_label.grid(row=1, column=0, sticky = "w", padx = 5, pady = 2)
line110_2_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_2_value_label.grid(row=1, column=1, sticky = "w", padx = 5, pady = 2)

line110_3_label = Label(lines110_frame, text="ВЛ Жана-Жарык - 1: ", font=('Arial', 13))
line110_3_label.grid(row=2, column=0, sticky = "w", padx = 5, pady = 2)
line110_3_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_3_value_label.grid(row=2, column=1, sticky = "w", padx = 5, pady = 2)

line110_4_label = Label(lines110_frame, text="ВЛ Жана-Жарык - 2: ", font=('Arial', 13))
line110_4_label.grid(row=3, column=0, sticky = "w", padx = 5, pady = 2)
line110_4_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_4_value_label.grid(row=3, column=1, sticky = "w", padx = 5, pady = 2)

line110_5_label = Label(lines110_frame, text="ВЛ Сантехническая - 1: ", font=('Arial', 13))
line110_5_label.grid(row=4, column=0, sticky = "w", padx = 5, pady = 2)
line110_5_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_5_value_label.grid(row=4, column=1, sticky = "w", padx = 5, pady = 2)

line110_6_label = Label(lines110_frame, text="ВЛ Сантехническая - 2: ", font=('Arial', 13))
line110_6_label.grid(row=5, column=0, sticky = "w", padx = 5, pady = 2)
line110_6_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_6_value_label.grid(row=5, column=1, sticky = "w", padx = 5, pady = 2)

line110_7_label = Label(lines110_frame, text="ВЛ Сталь: ", font=('Arial', 13))
line110_7_label.grid(row=6, column=0, sticky = "w", padx = 5, pady = 2)
line110_7_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_7_value_label.grid(row=6, column=1, sticky = "w", padx = 5, pady = 2)

line110_8_label = Label(lines110_frame, text="ВЛ Каз Карбон: ", font=('Arial', 13))
line110_8_label.grid(row=7, column=0, sticky = "w", padx = 5, pady = 2)
line110_8_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_8_value_label.grid(row=7, column=1, sticky = "w", padx = 5, pady = 2)

line110_9_label = Label(lines110_frame, text="ВЛ КЗФ - 1: ", font=('Arial', 13))
line110_9_label.grid(row=8, column=0, sticky = "w", padx = 5, pady = 2)
line110_9_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_9_value_label.grid(row=8, column=1, sticky = "w", padx = 5, pady = 2)

line110_10_label = Label(lines110_frame, text="ВЛ КЗФ - 2: ", font=('Arial', 13))
line110_10_label.grid(row=9, column=0, sticky = "w", padx = 5, pady = 2)
line110_10_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_10_value_label.grid(row=9, column=1, sticky = "w", padx = 5, pady = 2)

line110_11_label = Label(lines110_frame, text="ВЛ Насосная: ", font=('Arial', 13))
line110_11_label.grid(row=10, column=0, sticky = "w", padx = 5, pady = 2)
line110_11_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_11_value_label.grid(row=10, column=1, sticky = "w", padx = 5, pady = 2)

line110_12_label = Label(lines110_frame, text="ВЛ ОВМ-110: ", font=('Arial', 13))
line110_12_label.grid(row=11, column=0, sticky = "w", padx = 5, pady = 2)
line110_12_value_label = Label(lines110_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line110_12_value_label.grid(row=11, column=1, sticky = "w", padx = 5, pady = 2)

line110_sum_label = Label(lines110_frame, text="Сумма P по линиям 110кВ: ", font=('Arial', 14))
line110_sum_label.grid(row=12, column=0, sticky = "w", padx = 5, pady = 5)
line110_sum_value_label = Label(lines110_frame, text="0.0", font=('Arial', 14), width = 10, anchor="w")
line110_sum_value_label.grid(row=12, column=1, sticky = "w", padx = 5, pady = 5)

#ЛИНИИ 220 кВ
lines220_frame = LabelFrame(tab1, text="Линии 220кВ", font=('Times New Roman', 12))
lines220_frame.grid(row=1, rowspan=2, column=2, sticky="nw", padx = 5, pady = 2)

line220_1_label = Label(lines220_frame, text="ВЛ Л-2278: ", font=('Arial', 13))
line220_1_label.grid(row=0, column=0, sticky = "w", padx = 5, pady = 2)
line220_1_value_label = Label(lines220_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line220_1_value_label.grid(row=0, column=1, sticky = "w", padx = 5, pady = 2)

line220_2_label = Label(lines220_frame, text="ВЛ Л-2288: ", font=('Arial', 13))
line220_2_label.grid(row=1, column=0, sticky = "w", padx = 5, pady = 2)
line220_2_value_label = Label(lines220_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line220_2_value_label.grid(row=1, column=1, sticky = "w", padx = 5, pady = 2)

line220_3_label = Label(lines220_frame, text="ВЛ Л-2058: ", font=('Arial', 13))
line220_3_label.grid(row=2, column=0, sticky = "w", padx = 5, pady = 2)
line220_3_value_label = Label(lines220_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line220_3_value_label.grid(row=2, column=1, sticky = "w", padx = 5, pady = 2)

line220_4_label = Label(lines220_frame, text="ВЛ Л-2068: ", font=('Arial', 13))
line220_4_label.grid(row=3, column=0, sticky = "w", padx = 5, pady = 2)
line220_4_value_label = Label(lines220_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line220_4_value_label.grid(row=3, column=1, sticky = "w", padx = 5, pady = 2)

line220_5_label = Label(lines220_frame, text="ОВМ-220: ", font=('Arial', 13))
line220_5_label.grid(row=4, column=0, sticky = "w", padx = 5, pady = 2)
line220_5_value_label = Label(lines220_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
line220_5_value_label.grid(row=4, column=1, sticky = "w", padx = 5, pady = 2)

line220_sum_label = Label(lines220_frame, text="Сумма P по линиям 220кВ: ", font=('Arial', 14))
line220_sum_label.grid(row=5, column=0, sticky = "w", padx = 5, pady = 5)
line220_sum_value_label = Label(lines220_frame, text="0.0", font=('Arial', 14), width = 10, anchor="w")
line220_sum_value_label.grid(row=5, column=1, sticky = "w", padx = 5, pady = 5)

#НАПРЯЖЕНИЯ НА ШИНАХ 110кВ и 220кВ
u_frame = LabelFrame(tab1, text="Напряжение на шинах", font=('Times New Roman', 12))
u_frame.grid(row=2, column=2, sticky = "w", padx=5, pady=5)

u_110_label = Label(u_frame, text="Напряжение 2СШ 110кВ: ", font=('Arial', 13))
u_110_label.grid(row=0, column=0, sticky = "w", padx = 5, pady = 2)
u_110_value_label = Label(u_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
u_110_value_label.grid(row=0, column=1, sticky = "w", padx = 5, pady = 2)

u_220_label = Label(u_frame, text="Напряжение 2СШ 220кВ: ", font=('Arial', 13))
u_220_label.grid(row=1, column=0, sticky = "w", padx = 5, pady = 2)
u_220_value_label = Label(u_frame, text="0.0", font=('Arial', 13), width = 10, anchor="w")
u_220_value_label.grid(row=1, column=1, sticky = "w", padx = 5, pady = 2)

#СУММА МОЩНОСТИ ПО ВСЕМ ЛИНИЯМ (110кВ + 220кВ)
all_lines_sum_frame = LabelFrame(tab1, text="Сумма P по всем линиям", font=('Times New Roman', 12))
all_lines_sum_frame.grid(row=3, column=0, columnspan=2, sticky="nw", padx = 5, pady = 2)

all_lines_sum_label = Label(all_lines_sum_frame, text="Сумма P по линиям 110кВ + 220кВ: ", font=('Arial', 14))
all_lines_sum_label.grid(row=0, column=0, sticky="w", padx = 5, pady = 5)
all_lines_sum_value_label = Label(all_lines_sum_frame, text="0.0", font=('Arial', 16), width = 15, bg='white', borderwidth=2, relief='ridge')
all_lines_sum_value_label.grid(row=0, column=1, sticky="w", padx = 5, pady = 5)

#СОБСТВЕННЫЕ НУЖДЫ (с потребителями по 6кВ)
sn_frame = LabelFrame(tab1, text="Собственные нужды и потребители по 6кВ", font=('Times New Roman', 12))
sn_frame.grid(row=4, column=0, columnspan=2, sticky="nw", padx = 5, pady = 5)

sn_label = Label(sn_frame, text="Сумма P СН + потребители 6кВ + потери", font=('Arial', 14))
sn_label.grid(row=0, column=0, sticky="w", padx = 5, pady = 5)
sn_value_label = Label(sn_frame, text="0.0", font=('Arial', 14), width = 15, bg='white', borderwidth=2, relief='ridge')
sn_value_label.grid(row=0, column=1, sticky="w", padx = 5, pady = 5)


#ВКЛАДКА ВЫДАЧИ ЭЛЕКТРОЭНЕРГИИ И РАСЧЁТОВ

period_fact_labels = []
period_plan_labels = []
period_head_labels = []
period_energy_labels = []


#Средняя мощность по 15-минуткам. Факт | План
period_output_frame = LabelFrame(tab2, text="Суммарная выдача мощности с шин 110 и 220кВ по периодам одного часа", font=('Arial', 12))
period_output_frame.grid(row=0, rowspan=2, column=0, sticky="nw", padx = 10, pady = 12)
period_label1 = Label(period_output_frame, text="Время\n\n13:00-14:00", font=('Arial', 14), justify=LEFT)
period_label1.grid(row=0, rowspan=2, column=0, sticky="w", padx=5, pady=5)
for i in range(4):
    period_head_labels.append(Label(period_output_frame, text = "{} мин\nФакт    |    График".format(str((i+1)*15)), font=('Arial', 14), width = 18, justify=CENTER))
    period_head_labels[i].grid(row=0, column=1+(i*2), columnspan=2, padx=(25, 1), pady=0)
    
    period_fact_labels.append(Label(period_output_frame, text = "0.0", font=('Arial', 14), width = 9, anchor="center", bg='white', borderwidth=2, relief='ridge'))
    period_fact_labels[i].grid(row=1, column=1+(i*2), sticky="e", padx=2, pady=10)

    period_plan_labels.append(Label(period_output_frame, text = "0.0", font=('Arial', 14), width = 9, anchor="center", bg='white', borderwidth=2, relief='ridge'))
    period_plan_labels[i].grid(row=1, column=1+(i*2+1), sticky="w", padx=2, pady=10)


#Суммарная перевыдача или недовыдача эл.энергии по 15-минуткам
    
period_label2 = Label(period_output_frame, text="Суммарный\nнедостаток(-)\nизбыток(+)", font=('Arial', 14), width=10, justify=LEFT)
period_label2.grid(row=2, column=0, sticky="w", padx=5, pady=5)
for i in range(4):
    period_energy_labels.append(Label(period_output_frame, text = "0.0 кВт*ч", font=('Arial', 14), width = 16, anchor="center", bg='white', borderwidth=2, relief='ridge'))
    period_energy_labels[i].grid(row=2, column=1+(i*2), columnspan=2, padx=14, pady=10)


#Текущая необходимая величина выдачи мощности для выполнения плана

period_label3 = Label(period_output_frame, text='Необходимая величина выдачи\nмощности для выполнения графика:', font=('Arial', 14), width=28, justify=LEFT, anchor='w')
period_label3.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)
period_label4 = Label(period_output_frame, text='Необходимая величина суммарной\nгенерации:', font=('Arial', 14), width=28, justify=LEFT, anchor='w')
period_label4.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=15)
period_label5 = Label(period_output_frame, text='Выдача:', font=('Arial', 16), width=9, justify=LEFT, anchor='e')
period_label5.grid(row=3, column=6, sticky="w", padx=2, pady=5)
period_label6 = Label(period_output_frame, text='Генерация:', font=('Arial', 16), width=9, justify=LEFT, anchor='e')
period_label6.grid(row=4, column=6, sticky="w", padx=2, pady=15)
period_label7 = Label(period_output_frame, text = 'Величина генерации, которая потребуется\nдля выполнения заявки:', font=('Arial', 14), width=34, justify=LEFT, anchor='w')
period_label7.grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=(25, 5))
period_label8 = Label(period_output_frame, text='Время исполнения заявки:', font=('Arial', 14), width=22, justify=LEFT, anchor='e')
period_label8.grid(row=5, column=5, columnspan=2, sticky="w", padx=2, pady=(25, 5))


power_target_label = Label(period_output_frame, text='0.0 МВт', font=('Arial', 28), width = 14, anchor='center', bg='white', borderwidth=2, relief='ridge')
power_target_label.grid(row=3, column=3, columnspan=3, padx=8, pady=10)

generation_target_label = Label(period_output_frame, text='0.0 МВт', font=('Arial', 28), width = 14, anchor='center', bg='white', borderwidth=2, relief='ridge')
generation_target_label.grid(row=4, column=3, columnspan=3, padx=8, pady=15)

power_current_label = Label(period_output_frame, text='0.0 МВт', font=('Arial', 26), width = 10, anchor='center', bg='white', borderwidth=2, relief='ridge')
power_current_label.grid(row=3, column=7, columnspan=2, padx=1, pady=10)

generation_current_label = Label(period_output_frame, text='0.0 МВт', font=('Arial', 26), width = 10, anchor='center', bg='white', borderwidth=2, relief='ridge')
generation_current_label.grid(row=4, column=7, columnspan=2, padx=1, pady=15)

request_target_label = Label(period_output_frame, text=' ', font=('Arial', 24), width = 10, anchor='center', bg='white', borderwidth=2, relief='ridge')
request_target_label.grid(row=5, column=3, columnspan=2, padx=2, pady=(25, 5))

request_time_label = Label(period_output_frame, text=' ', font=('Arial', 24), width = 10, anchor='center', bg='white', borderwidth=2, relief='ridge')
request_time_label.grid(row=5, column=7, columnspan=2, padx=2, pady=(25, 5))

#Часовой итог

hour_frame = LabelFrame(tab2, text="Итог за час", font=('Arial', 12))
hour_frame.grid(row=0, column=1, sticky="nw", padx = 20, pady = 12)    

hour_head_label = Label(hour_frame, text = "1 час\nФакт    |    График", font=('Arial', 14), width = 18, justify=CENTER)
hour_head_label.grid(row=0, column=0, columnspan=2, padx=(25, 1), pady=0)
hour_fact_label = Label(hour_frame, text = "0.0 МВт", font=('Arial', 14), width = 9, anchor="center", bg='white', borderwidth=2, relief='ridge')
hour_fact_label.grid(row=1, column=0, sticky="e", padx=2, pady=10)
hour_plan_label = Label(hour_frame, text = "0.0 МВт", font=('Arial', 14), width = 9, anchor="center", bg='white', borderwidth=2, relief='ridge')
hour_plan_label.grid(row=1, column=1, sticky="w", padx=2, pady=10)
hour_energy_label = Label(hour_frame, text = "0.0 кВт*ч", font=('Arial', 14), width = 12, anchor="center", bg='white', borderwidth=2, relief='ridge')
hour_energy_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=28)



# ЗАЯВКА НА ТЕКУЩИЙ ЧАС

hour_request_frame = LabelFrame(tab2, text="Окно заявки", font=('Arial', 12))
hour_request_frame.grid(row=1, rowspan=2, column=1, sticky="n", padx = 20, pady = 5)

hour_request_label1 = Label(hour_request_frame, text = 'Введите заявку на\nтекущий час (в тысячах кВт*ч):\nЗаявка на понижение\nвводится со знаком "-",\nна повышение: без знака', font=('Arial', 12), justify=LEFT)
hour_request_label1.grid(row=0, column=0, sticky="n", padx=5, pady=5)

hour_request_entry = Entry(hour_request_frame, font=('Arial', 14), justify=CENTER, width=18)
hour_request_entry.grid(row=1, column=0, sticky="w", padx=5, pady=5)
hour_request_entry.insert(0, "")

hour_request_label2 = Label(hour_request_frame, text = 'Введите минуту начала\nисполнения заявки', font=('Arial', 12), justify=LEFT)
hour_request_label2.grid(row=2, column=0, sticky="w", padx=5, pady=2)

hour_request_combobox = ttk.Combobox(hour_request_frame, values = request_minutes, font=('Arial', 12))
hour_request_combobox.grid(row=3, column=0, sticky="w", padx=5, pady=2)
hour_request_combobox.current(0)

hour_request_btn = Button(hour_request_frame, text="Ввести заявку", font=('Arial', 14), anchor=CENTER, command=get_hour_request)
hour_request_btn.grid(row=4, column=0, sticky="ew", padx=5, pady=5)


#ЧАСОВЫЕ ПЛАНЫ НА 24 ЧАСА

day_plan_frame = LabelFrame(tab2, text="Почасовой график выдачи мощности, МВт", font=('Arial', 12))
day_plan_frame.grid(row=2, rowspan=2, column=0, sticky="nw", padx = 10, pady=10)

day_plan_label1 = Label(day_plan_frame, text = "Факт        |    График", font=('Arial', 12), width = 22)
day_plan_label1.grid(row=0, column=1, columnspan=2, sticky="w", padx=(9, 2), pady=2)
day_plan_label2 = Label(day_plan_frame, text = "Факт        |    График", font=('Arial', 12), width = 22)
day_plan_label2.grid(row=0, column=4, columnspan=2, sticky="w", padx=(9, 2), pady=2)
day_plan_label3 = Label(day_plan_frame, text = "Факт        |    График", font=('Arial', 12), width = 22)
day_plan_label3.grid(row=0, column=7, columnspan=2, sticky="w", padx=(9, 2), pady=2)

day_hour_fact_labels = []
day_hour_plan_entry = []
day_hour_time_labels = []
for i in range(24):
    day_hour_time_labels.append(Label(day_plan_frame, text = "{}:00-{}:00".format(i, i+1), font=('Arial', 11), width = 10, anchor="e"))
    day_hour_time_labels[i].grid(row=(1+i-8*(i//8)), column=(i//8)*3, sticky="e", padx=2, pady=0)
    
    day_hour_fact_labels.append(Label(day_plan_frame, font=('Arial', 11), width = 11, anchor="center", bg='white', borderwidth=2, relief='ridge'))
    day_hour_fact_labels[i].grid(row=(1+i-8*(i//8)), column=(i//8)*3+1, sticky="e", padx=2, pady=0)

    day_hour_plan_entry.append(Entry(day_plan_frame, font=('Arial', 11), width = 11, justify=CENTER))
    day_hour_plan_entry[i].grid(row=(1+i-8*(i//8)), column=(i//8)*3+2, sticky="w", padx=(2,22), pady=0)
    
day_plan_btn = Button(tab2, text="Ввести данные\nпочасового графика\nвыдачи мощности", font=('Arial', 14), width=20, justify=CENTER, anchor=CENTER, command=get_day_plan)
day_plan_btn.grid(row=3, column=1, sticky="w", padx=5, pady=5)    




#ОКНО ОТЛАДКИ
text_frame = LabelFrame(tab1, text="Окно отладки", padx=2, pady=4)
text_frame.grid(row=3, rowspan=2, column=2, sticky=E+W+N+S)

t = Text(text_frame, height=4, width=40, font=('Arial',14), padx=4, pady=4)
t.grid(row=0, column=0, sticky=E+W+N+S)

#scroll = Scrollbar(text_frame, orient="vertical")
#scroll.grid(row=0, column=1, sticky="ns")
#scroll.config(command=t.yview)
#t.config(yscrollcommand=scroll.set)

btn_start = Button(tab1, text="Загрузить данные", font=16, anchor=CENTER, command=get_start)
btn_start.grid(row=0, column=1, pady=5)
btn_stop = Button(tab1, text="Остановить загрузку", font=16, command=stop_search)
btn_stop.grid(row=0, column=2, pady=5, sticky=W)


#root.columnconfigure(0, weight=1)
text_frame.columnconfigure(0, weight=1)

tab_root.grid(column=0, row=0)
tab_root.bind('<<NotebookTabChanged>>', on_tab_change)

root.protocol("WM_DELETE_WINDOW", on_closing)

#my_debug()
work_loop()
mainloop()



