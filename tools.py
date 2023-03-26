
import math
#messaging system
from datetime import datetime, timedelta
import os
from twilio.rest import Client

#sends text to phone number when use hits benchmark
def sendBenchmarkText(phonenumber):
    # Your Account SID from twilio.com/console
    account_sid = "ACb1de3838939b16218154e0f591823a4e"
    # Your Auth Token from twilio.com/console
    auth_token  = "db514644992d1141d6e995cbd997345b"

    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        to=phonenumber, 
        from_="+18665169572",
        body="Congrats! You hit your goal!")

#send text once a day
def sendDailyText(phonenumber):
    account_sid = "ACb1de3838939b16218154e0f591823a4e"
    auth_token = "db514644992d1141d6e995cbd997345b"
    client = Client(account_sid, auth_token)
    num = "+1" + phonenumber
    # send_when = datetime.utcnow() + timedelta(hours=24)

    messaging_service_sid = "MG95c9822be2a164a9cbdd7b4e6c505493"
    
    message = client.messages.create(
        to=num, 
        from_=messaging_service_sid,
        body="Don't forget to enter your goals today if you haven't already!",
        # schedule_type="fixed",
        # send_at=send_when.isoformat() + "Z",
        )

#greeting message after opening app and entering name
def currentTimeGreeting(Person):
    currentTime = str(datetime.utcnow())
    currentTime = int(currentTime[11:13])
    
    if currentTime >= 0 and currentTime < 12:
        return f"Good morning {Person.name}!"
    elif currentTime >= 12 and currentTime < 18:
        return f"Good afternoon {Person.name}!"
    elif currentTime >= 18 and currentTime < 24:
        return f"Good evening {Person.name}."

class Person():
    
    def __init__(self, name, age, height, weight, gender, activity, phonenumber):
        self.name = name
        self.age = age #years
        self.height = height #centimeters
        self.weight = weight #Kilograms
        self.gender = gender.upper() #MALE or FEMALE
        self.activity = activity.upper() #SEDENTARY, MODERATE, ACTIVE
        self.phonenumber = f"+1{phonenumber}" #+1**********

    def __str__(self):
        return f"Name: {self.name}\nAge: {self.age}\nHeight: {self.height}\nWeight: {self.weight}\nGender: {self.gender}\nActivity Level: {self.activity}\nPhone Number: {self.phonenumber}"

class DailyCalories():
    def __init__(self, Person):
        self.Person = Person

    #calculate basal metabolic rate using Mifflin-St. Jeor equation
    def calculateBMR(self):
        if self.Person.gender == "MALE":
            return (10*self.Person.weight) + (6.25*self.Person.height) - (5*self.Person.age) + 5
        elif self.Person.gender == "FEMALE":
            return (10*self.Person.weight) + (6.25*self.Person.height) - (5*self.Person.age) - 161

    #values based on medicalnewstoday
    def calculateDailyCalories(self):
        if self.Person.activity == "SEDENTARY":
            return self.calculateBMR() * 1.2
        elif self.Person.activity == "MODERATE":
            return self.calculateBMR() * 1.55
        elif self.Person.activity == "ACTIVE":
            return self.calculateBMR() * 1.725

#use to see if person hit their goals
#call when benchmarks are hit:
#   when calories left == 0: call hitDailyCalories
#   when caloriesBurned == caloriesBurnedGoal
class Benchmarks():
    def __init__(self, dailyCalories, caloriesIntake, caloriesBurned, caloriesBurnedGoal, Person):
        self.dailyCalories = dailyCalories
        self.caloriesBurned = caloriesBurned
        self.caloriesIntake = caloriesIntake
        self.caloriesBurnedGoal = caloriesBurnedGoal
        self.Person = Person

    def hitDailyCalories(self):
        if self.caloriesIntake >= self.dailyCalories:
            sendBenchmarkText(self.Person.phonenumber)
    
    def hitCaloriesBurnedGoal(self):
        if self.caloriesBurned >= self.caloriesBurnedGoal:
            sendBenchmarkText(self.Person.phonenumber)

#running, swimming, cycling (GETS TIME IN SECONDS)
class AerobicWorkout():
    def __init__(self, time, distance,intensity, Person):
        self.time = time
        self.distance = distance
        self.Person = Person
        self.intensity = intensity
    
    #meters per minute
    def getSpeed(self):
        speed = self.distance/(self.time/60)
        return speed

    #sedentary, moderate, active
    def caloriesLostAer(self):
        if(self.intensity == 1):
            if(self.Person.gender == "MALE"):
                88.362 + (13.397 * self.Person.weight) + (4.799 * self.Person.height) - (5.677 * self.Person.age)
            else:
                447.593 + (9.247 * self.Person.weight) + (3.098 * self.Person.height) - (4.330 * self.Person.age)
        else:
            if(self.Person.gender == "MALE"):
                if(self.Person.activity == "SEDENTARY"):
                    if(self.Person.age >= 1 and self.Person.age <= 17):
                        VO2 = 23 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 18 and self.Person.age <= 25):
                        VO2 = 24 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 26 and self.Person.age <= 35):
                        VO2 = 22 + (35 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 36 and self.Person.age <= 45):
                        VO2 = 17 + (45 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 46 and self.Person.age <= 55):
                        VO2 = 14 + (55 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 56 and self.Person.age <= 65):
                        VO2 = 11 + (65 - self.Person.age) + (1.7**self.intensity)
                    else:
                        VO2 = 11 - (0.1*self.Person.age) + (1.7**self.intensity)

                elif(self.Person.activity == "MODERATE"):
                    if(self.Person.age >= 1 and self.Person.age <= 17):
                        VO2 = 35 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 18 and self.Person.age <= 25):
                        VO2 = 36 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 26 and self.Person.age <= 35):
                        VO2 = 34 + (35 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 36 and self.Person.age <= 45):
                        VO2 = 30 + (45 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 46 and self.Person.age <= 55):
                        VO2 = 27 + (55 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 56 and self.Person.age <= 65):
                        VO2 = 25 + (65 - self.Person.age) + (1.7**self.intensity)
                    else:
                        VO2 = 25 - (0.1*self.Person.age) + (1.7**self.intensity)
                else:
                    if(self.Person.age >= 1 and self.Person.age <= 17):
                        VO2 = 46 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 18 and self.Person.age <= 25):
                        VO2 = 47 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 26 and self.Person.age <= 35):
                        VO2 = 45 + (35 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 36 and self.Person.age <= 45):
                        VO2 = 38 + (45 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 46 and self.Person.age <= 55):
                        VO2 = 31 + (55 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 56 and self.Person.age <= 65):
                        VO2 = 29 + (65 - self.Person.age) + (1.7**self.intensity)
                    else:
                        VO2 = 29 - (0.1*self.Person.age) + (1.7**self.intensity)
            else:
                if(self.Person.activity == "SEDENTARY"):
                    if(self.Person.age >= 1 and self.Person.age <= 17):
                        VO2 = 16 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 18 and self.Person.age <= 25):
                        VO2 = 17 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 26 and self.Person.age <= 35):
                        VO2 = 15 + (35 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 36 and self.Person.age <= 45):
                        VO2 = 11 + (45 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 46 and self.Person.age <= 55):
                        VO2 = 10 + (55 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 56 and self.Person.age <= 65):
                        VO2 = 8 + (65 - self.Person.age) + (1.7**self.intensity)
                    else:
                        VO2 = 8 - (0.1*self.Person.age) + (1.7**self.intensity)

                elif(self.Person.activity == "MODERATE"):
                    if(self.Person.age >= 1 and self.Person.age <= 17):
                        VO2 = 29 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 18 and self.Person.age <= 25):
                        VO2 = 30 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 26 and self.Person.age <= 35):
                        VO2 = 28 + (35 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 36 and self.Person.age <= 45):
                        VO2 = 22 + (45 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 46 and self.Person.age <= 55):
                        VO2 = 21 + (55 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 56 and self.Person.age <= 65):
                        VO2 = 19 + (65 - self.Person.age) + (1.7**self.intensity)
                    else:
                        VO2 = 19 - (0.1*self.Person.age) + (1.7**self.intensity)
                else:
                    if(self.Person.age >= 1 and self.Person.age <= 17):
                        VO2 = 41 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 18 and self.Person.age <= 25):
                        VO2 = 42 + (25 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 26 and self.Person.age <= 35):
                        VO2 = 40 + (35 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 36 and self.Person.age <= 45):
                        VO2 = 33 + (45 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 46 and self.Person.age <= 55):
                        VO2 = 29 + (55 - self.Person.age) + (1.7**self.intensity)
                    elif(self.Person.age >= 56 and self.Person.age <= 65):
                        VO2 = 27 + (65 - self.Person.age) + (1.7**self.intensity)
                    else:
                        VO2 = 27 - (0.1*self.Person.age) + (1.7**self.intensity)

        MET = VO2/3.5
        return round(((MET*3.5*self.Person.weight)/200)*(self.time/360))
        #vo2 during exercise/3.5 = mets
        #METs x 3.5 x (your body weight in kilograms) / 200 = CALORIES BURNED PER MIN


#typical gym exercises
class AnaerobicWorkout():
    def __init__(self, reps, repWeight, sets, Person):
        self.reps = reps
        self.repWeight = repWeight
        self.sets = sets
        self.Person = Person

    def caloriesLostAn(self):
        return round(self.sets*self.reps*1.5*(1 + self.repWeight/self.Person.weight))


#create person, parameters are user entered

# p1 = Person("Justin", 21, 178, 125, "MalE", "ModeraTE", "7032202339")

# #creates aerobicWorkout, user entered params except p1 (time in seconds, distance in meters, person)

# ae1 = AerobicWorkout(2700, 1000, p1)

# #creates anaerobicWorkout, user entered params except p1 (how many reps, rep weight in kg, how many sets, person)

# an1 = AnaerobicWorkout(15, 45, 4, p1)
# print(p1) #toString to check

# #calculates how many calories were burned in the aerobic and anaerobic exercises and adds them together for total calories burned
# burnedCals1 = ae1.caloriesLostAer()
# burnedCals2 = an1.caloriesListAn()
# totalBurned = burnedCals1 + burnedCals2

# #DailyCalories is where all the calculations will take place, takes person as param
# diet1 = DailyCalories(p1)
# #calculates the recommended total calories a person should eat in a day
# diet1DailyCals = diet1.calculateDailyCalories()
# print(float(diet1DailyCals)) #prints number

# #Benchmarks is Twilio, will send messages
# #takes the recommended total calories, the calories already eaten, calories already burned, goal for calories burned (user input), and person in that order 
# benchmarks = Benchmarks(diet1DailyCals, (diet1DailyCals-1), totalBurned, 10, p1)
# benchmarks.hitDailyCalories() #send text if current calories intaked > daily calorie intake
# benchmarks.hitCaloriesBurnedGoal() #send text if current calories burned > goal
# print(currentTimeGreeting(p1))
# #sendDailyText()

