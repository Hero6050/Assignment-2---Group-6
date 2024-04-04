# Queue class
# We chose queue as our way of patient consultation system
# We chose this because of First-In-First-Out
# It will help patients not be frustrated for waiting too long
class PatientConsultationSystemQueue:
    def __init__(self):
        self.queue = []

    def register_patient(self, patient):
        # Here we are making a unique identifier
        patient_Identifier = len(self.queue) + 1
        # We update the patient's identifier
        patient.setIdentifier (patient_Identifier)
        self.queue.append(patient)
    def cancel_consultation(self, patient):
        if patient in self.queue:
            self.queue.remove(patient)
            return True
        return False
    def process_consultation(self):
        # Consultation process using queue
        if self.queue:
            nextPatient = self.queue.pop(0)
            nextPatient.displayPatient()
            return nextPatient
        else:
            print("No patients in the queue.")


# You can use any data structure to hold prescriptions
# We will use a simple list as a placeholder for patient data
class Patient:
    '''A class to hold patient information'''
    # Construct the object and define their attributes
    def __init__(self, name = "", age = 0, ID = "", medicalRecords = [], prescriptions = [], symptoms = []):
        self.__name = name
        self.__age = age
        self.__ID = ID
        # Identifier for when we give a patient an identifier
        self.__identifier = None
        self.__doctor = None
        self.__medicalRecords = medicalRecords
        self.__prescriptions = prescriptions
        self.__symptoms = symptoms
        self.__currentCondition = None

    # Setter/Getter functions
    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name
    def setAge(self, age):
        self.__age = age
    def getAge(self):
        return self.__age
    def setID(self, ID):
        self.__ID = ID
    def getID(self):
        return self.__ID
    def setIdentifier(self, identifier):
        self.__identifier = identifier
    def getIdentifier(self):
        return self.__identifier
    def setDoctor(self, doctor):
        self.__doctor = doctor
    def getDoctor(self):
        return self.__doctor
    def setCurrentCondition(self, condition):
        self.__currentCondition = condition
    def getCurrentCondition(self):
        return self.__currentCondition

    # Functions to add, remove, and get from lists
    def addMedicalRecord(self, record):
        if record not in self.__medicalRecords:
            self.__medicalRecords.append(record)
            return True
        return False
    def removeMedicalRecord(self, record):
        if record in self.__medicalRecords:
            self.__medicalRecords.remove(record)
            return True
        return False
    def getMedicalRecord(self):
        return self.__medicalRecords

    def addPrescription(self, prescription):
        if prescription not in self.__prescriptions:
            self.__prescriptions.append(prescription)
            return True
        return False
    def removePrescription(self, prescription):
        if prescription in self.__prescriptions:
            self.__prescriptions.remove(prescription)
            return True
        return False
    def getPrescriptions(self):
        return self.__prescriptions

    def addSymptom(self, symptom):
        if symptom not in self.__symptoms:
            self.__symptoms.append(symptom)
            return True
        return False
    def removeSymptom(self, symptom):
        if symptom in self.__symptoms:
            self.__symptoms.remove(symptom)
            return True
        return False
    def getSymptoms(self):
        return self.__symptoms

    # To schedules and appointment.
    def scheduleAppointment(self, hospital, receptionist, doctor):
        # We need to make sure the receptionist is in the hospital:
        if receptionist in hospital.getReceptionists():
            # The patient give the information to the receptionist
            # Then the receptionist takes schedules the patient
            return receptionist.schedulePatient(self, doctor)
        return False

    # To display patient details
    def displayPatient(self):
        print(f"Name: {self.getName()}")
        print(f"Age: {self.getAge()}")
        print(f"ID: {self.getID()}")
        print(f"Identifier: {self.getIdentifier()}")
        if self.__doctor is None:
            print(f"Assigned Doctor: None")
        else:
            print(f"Assigned Doctor: {self.__doctor.getName()}")
        print(f"Medical record: {self.getMedicalRecord()}")
        print(f"Prescription: {self.getPrescriptions()}")
        print(f"Symptoms: {self.__symptoms}")



# The receptionist will take the patient's info and schedule and appointment for them
# The receptionist will interact with the main system to queue patients
class Receptionist:
    '''This class represents a receptionist, they will take infor and schedule an appointment'''
    def __init__(self, name, recepID, hospital, shift):
        self.__name = name
        self.__recepID = recepID
        self.__shift = shift
        self.__hospital = hospital
        # Adding the receptionist to the hospital
        if hospital != None:
            hospital.addReceptionist(self)

    # Setter/Getter functions
    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name
    def setID(self, ID):
        # Polymorphic function
        self.__recepID = ID
    def getID(self):
        return self.__recepID
    def setShift(self, shift):
        self.__shift = shift
    def getShift(self):
        return  self.__shift
    def setHospital(self, hospital):
        # Check if the hospital exists first
        if hospital != None:
            # remove Receptionist from original hospital
            self.__hospital.removeReceptionist(self)
            # Update the receptionist to the new hospital and update the hospital
            self.__hospital = hospital
            self.__hospital.addReceptionist(self)
            return True
        self.__hospital = hospital
        return True

    def getHospital(self):
        return self.__hospital

    # To schedule appointments for patients and add them to queue.
    def schedulePatient(self, patient, doctor):
        # The receptionist plugs the infor into the system.
        # The system does the rest.
        # If doctor is not available we assign the patient to
        # the doctor with the least amount of patients in their queue
        if doctor not in self.__hospital.getDoctors():
            # If doctor is not available we assign the patient to
            # the doctor with the least amount of patients in their queue
            # Here we start with the first doctor and compare their queue time
            newDoc = self.__hospital.getDoctors()[0]
            for doc in self.__hospital.getDoctors():
                # If the doctor has a shorter queue than the new doctor
                # We update the new doctor
                if len(doc.getNextPatients()) < len(newDoc.getNextPatients()):
                    newDoc = doc
            doctor = newDoc
        return self.__hospital.queuePatient(patient, doctor)



    # To cancel appointments
    def cancelAppointment(self, patient):
        return self.__hospital.cancelConultation(patient)

    # To display receptionist
    def displayReceptionist(self):
        print(f"Receptionist ID: {self.getID()}")
        print(f"Shift: {self.getShift()}")
        print(f"Hospital: {self.__hospital.getHospName()}")


# Here is a class for doctor
# A doctor will consulate a patient, update their medical record, and give them prescription
class Doctor:
    def __init__(self, name, docID, field, hospital):
        self.__name = name
        self.__docID = docID
        self.__field = field
        # To see how many appointments this doctor has we will use a list of next patients
        self.__nextPatients = PatientConsultationSystemQueue()
        self.__currentPatient = None
        # Here we give the doctor an assigned hospital and
        self.__hospital = hospital
        if self.__hospital != None:
            self.__hospital.addDoctor(self)

    # Setter/Getter functions
    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name
    def setID(self, ID):
        self.__docID = ID
    def getID(self):
        return self.__docID
    def setField(self, field):
        self.__field = field
    def getField(self):
        return self.__field
    def setCurrentPatient(self, patient):
        # This sets the current patient if needed
        self.__currentPatient = patient
    def getCurrentPatient(self):
        return self.__currentPatient

    def setHospital(self, hospital):
        # remove doctor from original hospital
        self.__hospital.removeDoctor(self)
        # Update the doctor to the new hospital and update the hospital
        self.__hospital = hospital
        self.__hospital.addDoctor(self)
    def getHospital(self):
        return self.__hospital

    # To add a patient to the queue for the doctor
    def addNextPatient(self, patient):
        self.__nextPatients.register_patient(patient)
    def removeNextPatient(self, patient):
        # For when a patient wants to cancel their appointment
        if patient in self.__nextPatients.queue:
            return self.__nextPatients.cancel_consultation(patient)
        return False
    def getNextPatients(self):
        return self.__nextPatients.queue

    # For de-queuing next patient
    def nextPatient(self):
        # This makes the next patient in line the current patient
        # But the doctor must have no current patients first
        if self.__currentPatient is None:
            self.__currentPatient = self.__nextPatients.process_consultation()
            return True
        return False

    # For consulting current patient
    def consultPatient (self):
        # Here the doctor consults the patient and issues a prescription
        # We need to make sure there is a patient first
        if self.__currentPatient != None:
            patient = self.__currentPatient
            diseaseList = []
            if patient.getSymptoms() in diseaseList:
                # This connects the symptoms to a disease
                # The set it to variable x
                pass
            # Updates medical records then issue a prescription
            patient.addMedicalRecord("Here will be the newly added medical record")
            patient.addPrescription("Prescription X")
            patient.setCurrentCondition("Condition X")
            self.__currentPatient.setDoctor(None)
            self.__currentPatient = None
            return True
        return False

    def displayDoctor(self):
        print (f"Doctor: {self.getName()}")
        print (f"Doctor ID: {self.getID()}")
        print (f"Field: {self.getField()}")
        if self.__currentPatient is None:
            print (f"Current patient: None")
        else:
            print (f"Current patient:")
            self.__currentPatient.displayPatient()
            print("")

        print (f"Next patients: ")
        if self.__nextPatients != []:
            for patient in self.__nextPatients.queue:
                patient.displayPatient()
                print("")
        else:
            print (f"None")
        print(f"Hospital: {self.__hospital.getHospName()}")


# Here we create the main system that operates everything
# The system will do all the technical work
class Hospital:
    def __init__(self, hospName):
        self.__hospName = hospName
        self.__receptionists = []
        self.__doctors = []
        # This is used to hold patient information for record keeping
        # We will use a list, but we think a hashtable will be more secure
        # and have a better time complexity, same for holding receptionists and doctors information
        self.__allPatients = []

    # Setter/Getter function
    def setHospName(self, hospName):
        self.__hospName = hospName
    def getHospName(self):
        return self.__hospName

    # To add, remove, and get receptionists
    # See add and remove patient functions as they use hashtable as well.
    def addReceptionist(self, receptionist):
        if receptionist not in self.__receptionists:
            self.__receptionists.append(receptionist)
            if receptionist.getHospital() != self:
                receptionist.setHospital(self)
            return True
        return False
    def removeReceptionist(self, receptionist):
        if receptionist in self.__receptionists:
            self.__receptionists.remove(receptionist)
            receptionist.setHospital(None)
            return True
        return False
    def getReceptionists(self):
        return self.__receptionists

    # Add, remove, and get doctors
    # See add and remove patient functions as they use hashtable as well.
    def addDoctor(self, doctor):
        if doctor not in self.__doctors:
            self.__doctors.append(doctor)
            if doctor.getHospital() != self:
                doctor.setHospital(self)
            return True
        return False
    def removeDoctor(self, doctor):
        if doctor in self.__doctors:
            self.__doctors.remove(doctor)
            doctor.setHospital(None)
            return True
        return False
    def getDoctors(self):
        return self.__doctors

    # add, remove, and get patients
    # We will be using hashtable
    # To add a patient you find their hash
    # and use the formula to get the index
    # hash % n = index
    # n being the number of patients the hashtable can hold
    # This is a best-case of O(1)
    # We choose closed addressing meaning collision
    # Will be resolved via using linked list in each index
    # Meaning a worst-case of O(n)
    # n being the number of nodes in the linked list
    def addPatient(self, patient):
        if patient not in self.__allPatients:
            self.__allPatients.append(patient)
            return True
        return False
    # Removing elements is the same thing
    # Find the hash, the index, then remove the node the patient is in
    # However, you will need to make sure the list is linked properly afterward
    # So no data is lost
    def removePatient(self, patient):
        if patient in self.__allPatients:
            self.__allPatients.remove(patient)
            return True
        return False
    def getPatients(self):
        return self.__allPatients

    def queuePatient(self, patient, doctor):
        # To queue patient
        # Make sure that patient has no existing appointment
        # You can't be at two appointments at the same time
        if patient.getDoctor() is None:
            self.addPatient(patient)
            patient.setDoctor(doctor)
            if doctor in self.__doctors:
                doctor.addNextPatient(patient)
                return True
        return False
    def dequeuePatient(self, doctor):
        # To dequeue patient
        if doctor in self.__doctors:
            if doctor.getCurrentPatient() is None:
                doctor.nextPatient()
                return True
        return False

    # To find a certain patient
    # In hashtable we will be hashing the patient
    # Then use that hash to get the index of the patient
    # This is a best-case of O(1)
    # We choose closed addressing meaning collision
    # Will be resolved via using linked list in each index
    # Meaning a worst-case of O(n)
    # n being the number of nodes in the linked list
    def findPatient(self, patient):
        if patient in self.__allPatients:
            print("Patient is found:")
            patient.displayPatient()
            return True
        print("Patient is not available.")
        return False

    # To cancel appointments
    def cancelConsultation(self, patient):
        # Get the doctor of the patient
        doctor = patient.getDoctor()
        # If the patient is assigned a doctor, you cancel the appointment
        if doctor != None:
            return doctor.removeNextPatient(patient)
        return False

    # To display hospital details
    def displayHospital(self):
        print(f"Hospital: {self.__hospName}")
        print("Receptionists: ")
        if self.__receptionists == []:
            print("None")
        else:
            for receptionist in self.__receptionists:
                receptionist.displayReceptionist()
            print("")
        print("Doctors: ")
        if self.__doctors == []:
            print("None")
        else:
            for doctor in self.__doctors:
                doctor.displayDoctor()
                print("")

        print("Patients: ")
        if self.__allPatients == []:
            print("None")
        else:
            for patient in self.__allPatients:
                patient.displayPatient()
                print("")



# Function to be used in menu interface
def createHospital():
    hospName = input("Enter hospital name: ")
    return Hospital(hospName)
def createReceptionist(hospital):
    name = input("Enter receptionist name: ")
    recepID = input("Enter receptionist ID: ")
    shift = input ("Enter shift (Day/Night shift): ")
    print(f"We assigned the receptionist to {hospital.getHospName()}.")
    return Receptionist(name, recepID, hospital, shift)
def creatDoctor(hospital):
    name = input("Enter doctor name: ")
    docID = input("Enter doctor ID: ")
    field = input("Enter field: ")
    print(f"We assigned the doctor to {hospital.getHospName()}.")
    return Doctor(name, docID, field, hospital)
def createPatient():
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    ID = input("Enter patient ID: ")
    medicalRecord = [input("Enter medical record: ")]
    prescription = None
    prescriptions = []
    while prescription != "No":
        prescription = input("Enter prescription (enter 'No' if done): ")
        if prescription != "No":
            prescriptions.append(prescription)
    symptom = None
    symptoms = []
    while symptom != "No":
        symptom = input("Enter symptom (enter 'No' if done): ")
        if symptom != "No":
            symptoms.append(symptom)
    return Patient(name, age, ID, medicalRecord, prescriptions, symptoms)

def option1():
    # Picking a patient to queue
    patient = input(f"Enter patient you want to queue (enter '1', '2', '3', '4', '5)': \n")
    # This while loop ensures the input is valid
    while patient not in ("1", "2", "3", "4", "5"):
        print ("Error: YOU MUST ENTER AN INTEGER BETWEEN 1 AND 5")
        patient = input(f"Enter patient you want to queue (enter '1', '2', '3', '4', '5)': \n")

    if int(patient) == 1:
        patient = patient1
    elif int(patient) == 2:
        patient = patient2
    elif int(patient) == 3:
        patient = patient3
    elif int(patient) == 4:
        patient = patient4
    else:
        patient = patient5

    # Picking a receptionist to queue a patient
    receptionist = input(f"Enter receptionist to queue (1 or 2): \n")
    while receptionist not in ("1", "2"):
        print("ERROR: YOU MUST ENTER AN INTEGER BETWEEN 1 AND 2")
        receptionist = input(f"Enter receptionist to queue (1 or 2): \n")
    if int(receptionist) == 1:
        receptionist = receptionist1
    else:
        receptionist = receptionist2

    # To find doctor with the shortest queue
    newDoc = hospital1.getDoctors()[0]
    for doc in hospital1.getDoctors():
        if len(doc.getNextPatients()) < len(newDoc.getNextPatients()):
            newDoc = doc

    # Patient picking a doctor
    doctor = input(f"Enter the doctor the patient wants (1 or 2, if doctor not available you will get the doctor with the shortest queue): \n")
    if doctor in ("1", "2"):
        if int(doctor) == 1:
            doctor = doctor1
        else:
            doctor = doctor2

    print ("Input:")
    print (f"Patient: {patient.getName()}")
    print (f"Receptionist: {receptionist.getName()}")
    if doctor == doctor1 or doctor == doctor2:
        print (f"Doctor: {doctor.getName()}\n")
    else:
        print (f"Doctor (not available): {doctor}\n")
        doctor = newDoc

    print("Before:")
    print("Doctor perspective: ")
    doctor.displayDoctor()
    print("")
    print("Patient perspective: ")
    patient.displayPatient()
    print("")

    # Apply the function
    result = receptionist.schedulePatient(patient, doctor)

    print("Output: ")
    if result == True:
        print(f"Patient {patient.getName()} got assigned doctor {doctor.getName()}.\n")
    else:
        print(f"Patient has an existing appointment.\n")

    print("After:")
    print("Doctor perspective: ")
    doctor.displayDoctor()
    print("")
    print("Patient perspective: ")
    patient.displayPatient()
    print("")

    return

def option2():
    # A doctor calling their next patient
    # In other words, de-queuing a doctor's patients
    doctor = input(f"Pick a doctor to call in their next patient (1 or 2): \n")
    while doctor not in ("1", "2"):
        print("ERROR: INPUT MUST BE AN INTEGER BETWEEN 1 AND 2")
        doctor = input(f"Pick a doctor to call in their next patient (1 or 2): \n")
    if int(doctor) == 1:
        doctor = doctor1
    else:
        doctor = doctor2

    print("Input: ")
    print(f"De-queued doctor: {doctor.getName()}\n")
    print(f"Before:")
    doctor.displayDoctor()
    print("")

    # De-queue
    result = hospital1.dequeuePatient(doctor)

    print(f"OutPut: ")
    if result == True:
        print(f"Doctor has called their next patient.\n")
    else:
        print(f"Doctor has not called next patient (their current patient has not finished their session).\n")
    print("After: ")
    doctor.displayDoctor()
    return

def option3():
    # Doctor treating their patient
    doctor = input(f"Pick a doctor to treat their current patient (1 or 2): \n")
    while doctor not in ("1", "2"):
        print("ERROR: INPUT MUST BE AN INTEGER BETWEEN 1 AND 2")
        doctor = input(f"Pick a doctor to treat their current patient (1 or 2): \n")
    if int(doctor) == 1:
        doctor = doctor1
    else:
        doctor = doctor2

    currentPatient = doctor.getCurrentPatient()

    print("Input: ")
    print(f"Doctor to treat their patient: {doctor.getName()}\n")
    print("Before: ")
    doctor.displayDoctor()
    print("")

    # Consult patient
    result = doctor.consultPatient()

    print("Output: ")
    if result == True:
        print(f"Doctor has treated their patient (Patient has consulted their doctor).\n")
    else:
        print(f"Doctor has no current patients.\n")

    print("After:")
    doctor.displayDoctor()
    if result==True:
        print("")
        print(f"Patient who was treated: ")
        currentPatient.displayPatient()

    return

def option4():
    # cancel consultation
    patient = input(f"Enter patient you want to cancel consultation of (enter '1', '2', '3', '4', '5)': \n")
    # This while loop ensures the input is valid
    while patient not in ("1", "2", "3", "4", "5"):
        print("Error: YOU MUST ENTER AN INTEGER BETWEEN 1 AND 5")
        patient = input(f"Enter patient you want to cancel consultation of (enter '1', '2', '3', '4', '5)': \n")

    if int(patient) == 1:
        patient = patient1
    elif int(patient) == 2:
        patient = patient2
    elif int(patient) == 3:
        patient = patient3
    elif int(patient) == 4:
        patient = patient4
    else:
        patient = patient5

    # Get the doctor
    doctor = patient.getDoctor()

    print("Input: ")
    print(f"Patient wanting to cancel appointment: {patient.getName()}\n")
    print(f"Before: ")
    patient.displayPatient()
    if doctor != None:
        print("")
        doctor.displayDoctor()
    print("")

    # Cancel appointment
    # You can do this via receptionists if wanted as well.
    # We used the hospital here because it is one less step
    result = hospital1.cancelConsultation(patient)

    print("Output: ")
    if result == True:
        print (f"Patient canceled their appointment.\n")
    else:
        print (f"Patient does not have an appointment to cancel.\n")

    print("After: ")
    patient.displayPatient()
    if result == True:
        print("")
        doctor.displayDoctor()

    return

def option5():
    # find and display patient
    patient = input(f"Enter patient you want to display (enter '1', '2', '3', '4', '5)': \n")
    # This while loop ensures the input is valid
    while patient not in ("1", "2", "3", "4", "5"):
        print("Error: YOU MUST ENTER AN INTEGER BETWEEN 1 AND 5")
        patient = input(f"Enter patient you want to display (enter '1', '2', '3', '4', '5)': \n")

    if int(patient) == 1:
        patient = patient1
    elif int(patient) == 2:
        patient = patient2
    elif int(patient) == 3:
        patient = patient3
    elif int(patient) == 4:
        patient = patient4
    else:
        patient = patient5

    print("Input: ")
    print(f"Patient we are looking for: {patient.getName()}\n")
    print("Output: ")
    hospital1.findPatient(patient)
    return

def option6():
    # display doctor
    doctor = input(f"Pick a doctor to display (1 or 2): \n")
    while doctor not in ("1", "2"):
        print("ERROR: INPUT MUST BE AN INTEGER BETWEEN 1 AND 2")
        doctor = input(f"Pick a doctor to display (1 or 2): \n")
    if int(doctor) == 1:
        doctor = doctor1
    else:
        doctor = doctor2

    print("Input: ")
    print (f"Doctor we want to display: {doctor.getName()}\n")
    print(f"Output:")
    doctor.displayDoctor()
    return

def option7():
    # display receptionist
    receptionist = input("Enter receptionist to display (1 or 2): ")
    while receptionist not in ("1", "2"):
        print("ERROR: YOU MUST ENTER AN INTEGER BETWEEN 1 AND 2")
        receptionist = input("Enter receptionist to display (1 or 2): ")
    if int(receptionist) == 1:
        receptionist = receptionist1
    else:
        receptionist = receptionist2

    print("Input: ")
    print(f"Receptionist we want to display: {receptionist.getName()}\n")
    print("Output: ")
    receptionist.displayReceptionist()

    return

def option8():
    # display hospital
    hospital1.displayHospital()

    return

def option9():
    # close menu
    closeMenu = True
    return closeMenu



# Create a hospital
print("First we will create a hospital for the system:")
hospital1 = createHospital()
hospital1.displayHospital()
print("")

# Create receptionists
print("Next we will create receptionists that will be assigned a hospital at creation.")
print("receptionist1: ")
receptionist1 = Receptionist("Recep", "00001", hospital1, "Day shift")
receptionist1.displayReceptionist()
print("")
print("We created receptionist1, try creating receptionist2 (details will be printed afterward): ")
receptionist2 = createReceptionist(hospital1)
receptionist2.displayReceptionist()
print("")

# Create a doctor
print("Next we will create doctors who will also be assigned hospitals at creation.")
print("doctor1: ")
doctor1 = Doctor("Andrew", "00001", "Pediatrician", hospital1)
doctor1.displayDoctor()
print("")
print("We created doctor1, try creating doctor2 (details will be printed afterward): ")
doctor2 = creatDoctor(hospital1)
doctor2.displayDoctor()
print("")


# Create a patient
print("Lastly, we create patients so we can queue them and give them prescriptions: ")
print("patient1: ")
patient1 = Patient("Ahmad", 19, "00001", [], [], ["Cough", "Fever"])
patient1.displayPatient()
print("")
print("patient2: ")
patient2 = Patient("Abdulla", 20, "00002", [], [], ["Migraines", "Fatigue"])
patient2.displayPatient()
print("")
print("patient3: ")
patient3 = Patient("Mohammed", 18, "00003", [], [], ["Broken leg"])
patient3.displayPatient()
print("")
print("patient4: ")
patient4 = Patient("Rashid", 19, "00004", [], [], ["Insomnia"])
patient4.displayPatient()
print("")
print("We created patient1, patient2, patient3, and patient4, try creating patient5: ")
patient5 = createPatient()
patient5.displayPatient()
print("")

# This menu serves as a very flexible test-cases method
# It allows you to see what will happen if an error might occur
# For example, when you try to dequeue the line but a doctor is not done with the current patient
# Or what will happen if you try to set up two appointments at the same time
# It also shows what will happen if you try to cancel an appointment when you don't have one.
# Lastly, it allows you to see how the system changes by giving you the options to display
# patient, doctor, receptionist, or hospital details.
# This shows how the system generally functions.
closeMenu = False
while closeMenu == False:
    print("="*10, "MENU", "="*10)
    print("Option 1: Queue a patient")
    print("Option 2: A doctor calling their next patient")
    print("Option 3: A doctor treating their patient")
    print("Option 4: A patient cancels consultation")
    print("Option 5: Find and display patient")
    print("Option 6: Display doctor")
    print("Option 7: Display receptionist")
    print("Option 8: Display hospital")
    print(f"Option 9: Close menu\n")

    option = input("Pick an option: ")

    while option not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
        print("ERROR: INPUT MUST BE AN INTEGER BETWEEN 1 AND 9")
        option = input(f"Pick an option: \n")

    option = int(option)
    if option == 1:
        option1()
    elif option == 2:
        option2()
    elif option == 3:
        option3()
    elif option == 4:
        option4()
    elif option == 5:
        option5()
    elif option == 6:
        option6()
    elif option == 7:
        option7()
    elif option == 8:
        option8()
    else:
        closeMenu = option9()