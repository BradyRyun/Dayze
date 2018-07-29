import datetime
from datetime import datetime
import tkinter as tk
from tkinter import *
from re import findall


us_holidays = {'Christmas': [12,25,datetime.now().year], 'Halloween': [10,31,datetime.now().year], 'Independence Day': [7,4,datetime.now().year],
'New Year': [1,1,datetime.now().year], 'MLK Day': [1,15,datetime.now().year], 'Memorial Day': [5,28,datetime.now().year],
'Labor Day': [9,3,datetime.now().year], 'Columbus Day': [10,8,datetime.now().year], "Veteran's Day": [11,12,datetime.now().year],
'Thanksgiving': [11,22,datetime.now().year]}

# These two functions clear their corresponding entry boxes.
def clearBox1(event):
    date1_entry.delete(0,'end')
    return None

def clearBox2(event):
    date2_entry.delete(0,'end')
    return None

# Deletes the textbox before entering in the difference in dates. Also used for reset button functionality.
def delete_textbox():
    t1.delete('1.0','end')
    return None

def reset_fields():
    date1_entry.delete(0,'end')
    date2_entry.delete(0,'end')
    date1_entry.insert(0,'MM-DD-YYYY')
    date2_entry.insert(0,'MM-DD-YYYY')
    delete_textbox()
    t1.insert(END, 'Please enter two dates you would like to see the day difference between or pick your favorite holiday to see how long until it comes! \nYou may also type in "today" to use the current date.')

# Changes the date input into a datetime object
def change_date1():
    global date1
    d1 = date1_entry_value.get()
    if d1.lower() == 'today':
        date1 = datetime.now()
    else:
        d1 = date1_entry_value.get()
        d1_list = re.findall(r"[\w']+", d1)
        d1_str = ''.join(str(i) for i in d1_list)
        date1 = datetime.strptime(d1_str, "%m%d%Y")

def change_date2():
    global date2
    d2 = date2_entry_value.get()
    if d2.lower() == 'today':
        date2 = datetime.now()
    else:
        d2 = re.findall(r"[\w']+", d2)
        d2_str = ''.join(str(i) for i in d2)
        date2 = datetime.strptime(d2_str, '%m%d%Y')
# Takes dictionary values and turns them into datetime objects
def transform_holiday(holiday):
    delete_textbox()
    holiday_date = us_holidays[dropdown_value.get()]
    holiday_str = ''.join(str(i) for i in holiday_date)
    global holiday_d
    holiday_d = datetime.strptime(holiday_str, '%m%d%Y')
    h_diff = datetime.now() - holiday_d
    if h_diff.days > 0:
        t1.insert(END,'We are ' + str(365-h_diff.days) + ' days from the next ' + str(dropdown_value.get()) + '.')
    else:
        t1.insert(END, 'We are ' + str(-h_diff.days) + ' days from ' + str(dropdown_value.get()) + '.')

# Mathematical brains
def diff():
    delete_textbox()
    while True:
        try:
            change_date1()
            change_date2()
            difference = date1 - date2
            if 365 > difference.days > 0:
                t1.insert(END,'These dates are ' + str(difference.days) + ' days apart.')
            elif difference.days > 365:
                t1.insert(END, 'These dates are ' + str(round(difference.days/365.25)) + ' years and ' +  str(round(difference.days%365.25+1)) + ' days apart.')
            elif -365 < difference.days < 0:
                t1.insert(END, 'These dates are ' + str(-difference.days) + ' days apart.')
            else:
                t1.insert(END, 'These dates are ' + str(round(-difference.days/365.25)) + ' years and ' + str(round(difference.days%365.25+1)) + ' days apart.')
        except ValueError:
            t1.insert(END, 'One of the values was entered improperly. Please try again.')
        break


# Boots up the window
root = tk.Tk()
master = tk.Frame()
root.iconbitmap("icon.ico")

b_execution = tk.Button(master, text = 'DAYS', fg = 'green',command=diff)
b_execution.grid(row=0,column=0,padx=20, sticky=NW+NE)
b_reset = tk.Button(master, text = 'RESET', fg = 'red', command=reset_fields)
b_reset.grid(row=1,column=0,padx=20, sticky=W+E)

Label(master, text='First Date:').grid(row=0,column=1)
Label(master, text='Second Date:').grid(row=1,column=1)

# Creating the entry locations for the dates.

date1_entry_value = StringVar()
date1_entry = Entry(master, textvariable = date1_entry_value)
date1_entry.insert(0,'MM-DD-YYYY')

date1_entry.bind('<Button-1>', clearBox1)

date2_entry_value = StringVar()
date2_entry = Entry(master, textvariable = date2_entry_value)
date2_entry.insert(0,'MM-DD-YYYY')

date2_entry.bind('<Button-1>', clearBox2)

# The two binds above will clear the boxes when clicked

date1_entry.grid(row=0,column=2)
date2_entry.grid(row=1,column=2)

t1 = Text(master, height = 5, width=50, wrap = WORD)
t1.configure(font=('Arial', 11))
t1.insert(END, 'Please enter two dates you would like to see the day difference between or pick your favorite holiday to see how long until it comes! \nYou may also type in "today" to use the current date.')
t1.grid(row=3,column=0,columnspan = 4)

dropdown_value = StringVar()
w = OptionMenu(master, dropdown_value, *us_holidays.keys(), command=transform_holiday).grid(row=6, column =0,columnspan=4,sticky=S,padx=10,)
dropdown_value.set('Holidays')


root.title('Dayze  1.0')
master.pack()
root.mainloop()
