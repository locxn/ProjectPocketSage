from tkinter import *
from twilio.rest import Client
from datetime import date
from datetime import datetime
from tools import Person, DailyCalories, sendDailyText
from lobe import ImageModel
from TakePic import takePic
from PIL import Image
import re


def delete_widgets(*event):
    for widget in root.winfo_children():
        widget.destroy()



def weight(*event):
    weight_label = Label(root, bg = bg2_color, text= " Weight (kg): ",font =("Arial", 12), fg = "white")
    weight_label.place(x=100, y=325)

    weight_entry = Entry(root,bg = "white", fg = "black")
    weight_entry.place(x=200, y=330, width=50, height=20)

    reps_label = Label(root, bg = bg2_color, text= " Reps: ",font =("Arial", 12), fg = "white")
    reps_label.place(x=100, y=360)

    reps_entry = Entry(root,bg = "white", fg = "black")
    reps_entry.place(x=200, y=365, width=50, height=20)

    sets_label = Label(root, bg = bg2_color, text= " Sets: ",font =("Arial", 12), fg = "white")
    sets_label.place(x=100, y=400)

    sets_entry = Entry(root,bg = "white", fg = "black")
    sets_entry.place(x=200, y=405, width=50, height=20)

    calories_burned_label = Label(root, bg = bg2_color, text= " Calories Burned: ",font =("Arial", 12), fg = "white")
    calories_burned_label.place(x=100, y=500)
    

def cardio(*event):
    time_label = Label(root, bg = bg2_color, text= " Time (sec): ",font =("Arial", 12), fg = "white")
    time_label.place(x=100, y=325)

    time_entry = Entry(root,bg = "white", fg = "black")
    time_entry.place(x=200, y=330, width=50, height=20)

    distance_label = Label(root, bg = bg2_color, text= " Distance (m): ",font =("Arial", 12), fg = "white")
    distance_label.place(x=100, y=360)

    distance_entry = Entry(root,bg = "white", fg = "black")
    distance_entry.place(x=220, y=365, width=50, height=20)

    intensity_label = Label(root, bg = bg2_color, text= " Intensity: ",font =("Arial", 12), fg = "white")
    intensity_label.place(x=100, y=400)

    activity_sedentary_checkButt = Checkbutton(root,text="sedentary", onvalue= 1, offvalue= 0, fg="black",bg = "#89a6ff",selectcolor="white",activebackground="#89a6ff")
    activity_sedentary_checkButt.place(x=200, y=405, width=75, height=20)

    activity_moderate_checkButt = Checkbutton(root,text="moderate", onvalue= 1, offvalue= 0, fg="black",bg = "#89a6ff",selectcolor="white",activebackground="#89a6ff")
    activity_moderate_checkButt.place(x=275, y=405, width=75, height=20)

    activity_active_checkButt = Checkbutton(root,text="active", onvalue= 1, offvalue= 0, fg="black",bg = "#89a6ff",selectcolor="white",activebackground="#89a6ff")
    activity_active_checkButt.place(x=350, y=405, width=75, height=20)

def progress(*event):
    delete_widgets()
    global root
    box = Canvas(root,bg=bg2_color, width=500, height=400)
    box.place(x=25, y=75, width=500, height=600)
    
    weight_button = Button(root, text= "Weight",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    weight_button.place(x=85, y=100, width=175, height=125)
    weight_button.bind("<Button-1>",weight)

    cardio_button = Button(root, text= "Cardio",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    cardio_button.place(x=300, y=100, width=175, height=125)
    cardio_button.bind("<Button-1>",cardio)

    home_button = Button(root, text= "Home",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    home_button.place(x=25, y=25, width=90, height=30)
    home_button.bind("<Button-1>",home)


def editTotalCal(*event):
    global caloriesLeft
    global result
    result = result.prediction
    numbers_only = re.sub('[^0-9]', '',result)  # removes all non-numeric characters
    my_int = int(numbers_only)

    print(my_int, type(my_int))
    caloriesLeft -= my_int
    calorie()


def scan(*event):
    global result
    model = ImageModel.load("hoohacksTensorFlow")
    takePic()

    img = Image.open("saved_img.png")

    result = model.predict(img)
    print(result.prediction)

    scan_result = Label(root, bg = "grey", text= f"Result: {result.prediction}",font =("Arial", 12), fg = "white")
    scan_result.place(x=75, y=700, width=200, height=30)

    edit_button = Button(root, text= "Edit",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    edit_button.place(x=275, y=700, width=90, height=30)
    edit_button.bind("<Button-1>",editTotalCal)

    # Print all classes
    for label, confidence in result.labels:
        print(f"{label}: {confidence*100}%")

def demoTwilio(*event):
    global Phone
    sendDailyText(Phone)

def calorie(*event):
    delete_widgets()
    global caloriesLeft
    print(name, Age, Height, Weight, Gender, HomeIntensity, Phone)
    person = Person(name, Age, Height, Weight, Gender, HomeIntensity, Phone)
    print(person)
    dailyCal = DailyCalories(person)

    if caloriesLeft == 0:
        caloriesLeft = dailyCal.calculateDailyCalories()
        print(True)
    caloriesPerDay = dailyCal.calculateDailyCalories()


    global root

    box = Canvas(root,bg=bg2_color, width=500, height=400)
    box.place(x=200, y=25, width=300, height=500)

    box2 = Canvas(root,bg="grey", width=500, height=400)
    box2.place(x=75, y=100, width=400, height=100)

    fixed_calorie_label = Label(root, bg = "grey", text= "Total Calorie Per Day: ",font =("Arial", 12), fg = "white")
    fixed_calorie_label.place(x=75, y=100, width=400, height=100)

    sub_box = Canvas(root,bg="light gray", width=100, height=100)
    sub_box.place(x=300, y=175, width=150, height=75)

    fixed_calorieResult_label = Label(root, bg = "light gray", text= caloriesPerDay,font =("Arial", 12), fg = "black")
    fixed_calorieResult_label.place(x=305, y=200, width=140, height=20)

    box3 = Canvas(root,bg="grey", width=500, height=400)
    box3.place(x=75, y=300, width=400, height=100)

    left_calorie_label = Label(root, bg = "grey", text= "Calories Left To Intake: ",font =("Arial", 12), fg = "white")
    left_calorie_label.place(x=75, y=300, width=400, height=100)

    sub_box2 = Canvas(root,bg="#c8f8e8", width=100, height=100)
    sub_box2.place(x=300, y=375, width=150, height=75)

    fixed_calorieResult_label = Label(root, bg = "#c8f8e8", text= caloriesLeft,font =("Arial", 12), fg = "black")
    fixed_calorieResult_label.place(x=305, y=400, width=140, height=20)

    scan_button = Button(root, text= "Scan for Calories [◉\"]",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 24))
    scan_button.place(x=75, y=550, width=400, height=125)
    scan_button.bind("<Button-1>",scan)




    home_button = Button(root, text= "Home",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    home_button.place(x=25, y=25, width=90, height=30)

    home_button.bind("<Button-1>",home)

    demo_button = Button(root, text= "Demo",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    demo_button.place(x=450, y=700, width=90, height=30)

    demo_button.bind("<Button-1>",demoTwilio)

    root.mainloop()


def getName(*event):
    global name
    name = name_entry.get()
    name_entry.configure(fg = "grey")

def getAge(*event):
    global Age
    Age = int(age_entry.get())
    age_entry.configure(fg = "grey")

def getHeight(*event):
    global Height
    Height = int(height_entry.get())
    height_entry.configure(fg = "grey")
    print(Height)

def getWeight(*event):
    global Weight
    Weight = int(weight_entry.get())
    weight_entry.configure(fg = "grey")
    print(Weight)

def getPhone(*event):
    global Phone
    Phone = phone_entry.get()
    phone_entry.configure(fg = "grey")


def setSedintary(*event):
    global HomeIntensity
    HomeIntensity = "sedintary"
    # activity_sedentary_checkButt
    activity_moderate_checkButt.configure(fg = "grey")
    activity_active_checkButt.configure(fg = "grey")
def setModerate(*event):
    global HomeIntensity
    HomeIntensity = "moderate"
    activity_sedentary_checkButt.configure(fg = "grey")
    activity_active_checkButt.configure(fg = "grey")
def setActive(*event):
    global HomeIntensity
    HomeIntensity = "active"
    activity_moderate_checkButt.configure(fg = "grey")
    activity_sedentary_checkButt.configure(fg = "grey")

def setFemale(*event):
    global Gender
    Gender = "female"
    gender_boy_checkButt.configure(fg = "grey")

def setMale(*event):
    global Gender
    Gender = "male"
    gender_girl_checkButt.configure(fg = "grey")
    


def home(*event):
    delete_widgets()
    global root
    global bg_color
    global bg2_color

    global name
    global Age
    global Gender
    global Height
    global Weight
    global HomeIntensity
    global Phone

    global name_entry
    global age_entry 
    global height_entry 
    global weight_entry 
    global phone_entry 

    global gender_girl_checkButt
    global gender_boy_checkButt


    global activity_sedentary_checkButt
    global activity_moderate_checkButt 
    global activity_active_checkButt 

    global caloriesLeft

    root.wm_attributes('-transparentcolor', '#ab23ff')
    root.title("Pocket Trainer")
    root.configure(background=bg_color)

    box = Canvas(root,bg=bg2_color, width=500, height=400)
    box.place(x=25, y=25, width=500, height=100)

    title = Label(root,bg="#6f93ff", text = "Pocket Trainer",font =("Arial", 24), fg = "white")
    title.place(relx=0.5, rely=0.1, anchor=CENTER)

    box2 = Canvas(root,bg="#89a6ff", width=500, height=400)
    box2.place(x=25, y=200, width=500, height=300)

    box3 = Canvas(root,bg="grey", width=100, height=350, highlightthickness=0)
    box3.place(x=50, y=225, width=150, height=250)

    name_label = Label(root, bg = "grey", text= "[ Name ]",font =("Arial", 12), fg = "white")
    name_label.place(x=95, y=230)

    name_entry = Entry(root,bg = "white", fg = "black")
    name_entry.place(x=225, y=230, width=250, height=20)
    name_entry.bind("<Return>", getName)
    
    age_label = Label(root, bg = "grey", text= "[ Age ]",font =("Arial", 12), fg = "white")
    age_label.place(x=100, y=265)
    

    age_entry = Entry(root,bg = "white", fg = "black")
    age_entry.place(x=225, y=265, width=50, height=20)
    age_entry.bind("<Return>", getAge)


    gender_label = Label(root, bg = "grey", text= "[ Gender ]",font =("Arial", 12), fg = "white")
    gender_label.place(x=90, y=300)

    gender_girl_checkButt = Button(root, text= "Female",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 10))
    gender_girl_checkButt.place(x=225, y=300, width=75, height=20)
    gender_girl_checkButt.bind("<Button-1>",setFemale)


    gender_boy_checkButt = Button(root, text= "Male",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 10))
    gender_boy_checkButt.place(x=300, y=300, width=75, height=20)
    gender_boy_checkButt.bind("<Button-1>",setMale)


    height_label = Label(root, bg = "grey", text= "[ Height(cm) ]",font =("Arial", 12), fg = "white")
    height_label.place(x=80, y=335)


    height_entry = Entry(root,bg = "white", fg = "black")
    height_entry.place(x=225, y=335, width=50, height=20)
    height_entry.bind("<Return>", getHeight)


    weight_label = Label(root, bg = "grey", text= "[ Weight(kg) ]",font =("Arial", 12), fg = "white")
    weight_label.place(x=80, y=370)

    weight_entry = Entry(root,bg = "white", fg = "black")
    weight_entry.place(x=225, y=370, width=50, height=20)
    weight_entry.bind("<Return>", getWeight)


    activity_label = Label(root, bg = "grey", text= "[ Activity Level ]",font =("Arial", 12), fg = "white")
    activity_label.place(x=75, y=405)

    activity_sedentary_checkButt = Button(root, text= "sedentary",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 10))
    activity_sedentary_checkButt.place(x=225, y=405, width=75, height=20)
    activity_sedentary_checkButt.bind("<Button-1>",setSedintary)


    activity_moderate_checkButt = Button(root, text= "moderate",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 10))
    activity_moderate_checkButt.place(x=300, y=405, width=75, height=20)
    activity_moderate_checkButt.bind("<Button-1>",setModerate)


    activity_active_checkButt = Button(root, text= "active",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 10))
    activity_active_checkButt.place(x=375, y=405, width=75, height=20)
    activity_active_checkButt.bind("<Button-1>",setActive)


    phone_label = Label(root, bg = "grey", text= "[ Phone Number ]",font =("Arial", 12), fg = "white")
    phone_label.place(x=65, y=440)


    phone_entry = Entry(root,bg = "white", fg = "black")
    phone_entry.place(x=225, y=440, width=150, height=20)
    phone_entry.bind("<Return>", getPhone)



    calorie_button = Button(root, text= "Check Calories",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    calorie_button.place(x=85, y=550, width=175, height=125)
    calorie_button.bind("<Button-1>",calorie)

    progress_button = Button(root, text= "Check Progress",relief="groove",activebackground="grey",bg="#89a6ff",bd=1, fg="white", font=("Arial", 13))
    progress_button.place(x=300, y=550, width=175, height=125)
    progress_button.bind("<Button-1>",progress)

    root.mainloop()

if __name__ == "__main__":
    print("hi")

    name = "User"
    Age = 0
    Gender = "male"
    Height = 0
    Weight = 0
    HomeIntensity = "moderate"
    Phone = ""
    result = ""

    bg_color = "#bbeeff"    # light blue
    bg2_color = "#6fb7ff"   # white ish

    root = Tk()
    root.geometry("550x760")
    root.resizable(width=False, height=False)

    caloriesLeft = 0

    # box = Canvas(root)
    # box2 = Canvas(root)
    # box3 = Canvas(root)
    # name_label = Label(root)
    name_entry = Entry(root)
    age_entry = Entry(root)
    height_entry = Entry(root)
    weight_entry = Entry(root)
    phone_entry = Entry(root)
    gender_girl_checkButt = Button(root)
    gender_boy_checkButt = Button(root)

    activity_sedentary_checkButt = Checkbutton(root)
    activity_moderate_checkButt = Checkbutton(root)
    activity_active_checkButt = Checkbutton(root)

    home()

    print("bye")
