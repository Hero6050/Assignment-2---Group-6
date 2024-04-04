# Queue class
# We used dictionaries to house patient data here
# But will use classes in the main code
class PatientConsultationSystemQueue:
    def __init__(self):
        self.queue = []

    def register_patient(self, patient_details):
        # Here we are making a unique identifier
        patient_id = len(self.queue) + 1
        # must put all details in a dictionery
        assert isinstance(patient_details, dict), "Patient Details must be a dictionary."
        self.queue.append((patient_id, patient_details))
        print(f"Patient {patient_id} registered and added to the consultation queue.")
        for detail, value in patient_details.items():
            print(f"{detail.capitalize()}: {value}")
    def process_consultation(self):
        # Consultation process using queue
        if self.queue:
            patient_id, patient_details = self.queue.pop(0)
            print(f"Consultation complete for patient {patient_id}.")
            for detail, value in patient_details.items():
                print(f"{detail.capitalize()}: {value}")
        else:
            print("No patients in the queue.")

# Test-cases:

# MAKING AN OBJECT
patient_system_queue = PatientConsultationSystemQueue()

# FIRST PATIENT ADDED TO SYSTEM
patient_system_queue.register_patient({'name': 'Maryam', 'age': 20, 'Gender': 'Female'})

# SECOND PATIENT ADDED TO SYSTEM
patient_system_queue.register_patient({'name': 'Laiba', 'age': 23, 'Gender': 'Female'})

# doctor seeing patient using queue method
patient_system_queue.process_consultation()

# doctor seeing patient using queue method
patient_system_queue.process_consultation()

# doctor seeing patient using queue method
patient_system_queue.process_consultation()


# Stack class
class PatientConsultationSystemStack:
    def __init__(self):
        self.stack = []

    def register_patient(self, patient_details):
        # Unique identifier
        patient_id = len(self.stack) + 1
        assert isinstance(patient_details, dict), "Patient Details must be a dictionary."
        self.stack.append((patient_id, patient_details))
        print(f"Patient {patient_id} registered and added to the consultation stack.")
        for detail, value in patient_details.items():
            print(f"{detail.capitalize()}: {value}")

    def process_consultation(self):
        # stack tehnique
        if self.stack:
            patient_id, patient_details = self.stack.pop()
            print(f"Consultation complete for patient {patient_id}.")
            for detail, value in patient_details.items():
                print(f"{detail.capitalize()}: {value}")
        else:
            print("No patients in the stack.")

# Test-cases:

# MAKING AN OBJECT
patient_system_stack = PatientConsultationSystemStack()

# FIRST PATIENT ADDED TO SYSTEM
patient_system_stack.register_patient({'name': 'Maryam', 'age': 20, 'Gender': 'Female'})

# SECOND PATIENT ADDED TO SYSTEM
patient_system_stack.register_patient({'name': 'Laiba', 'age': 23, 'Gender': 'Female'})

# doctor seeing patient using stack method
patient_system_stack.process_consultation()

# doctor seeing patient using stack method
patient_system_stack.process_consultation()

# doctor seeing patient using stack method
patient_system_stack.process_consultation()


# Singly linked list node
class PatientSinglyNode:
    def __init__(self, patient_id, name, age, condition):
        """
        Represents a patient with attributes such as patient ID, name, age, and condition.
        """
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.condition = condition
        self.next = None  # Pointer to the next patient in the list

# Singly linked list class
class PatientSinglyLinkedList:
    def __init__(self):
        """
        Represents a singly linked list to manage patient records.
        """
        self.head = None  # Initialize an empty list

    def add_patient(self, patient):
        """
        Adds a patient to the end of the list.
        """
        if not self.head:
            self.head = patient
        else:
            current_patient = self.head
            while current_patient.next:
                current_patient = current_patient.next
            current_patient.next = patient

    def remove_patient(self, patient_id):
        """
        Removes a patient from the list based on their ID.
        """
        if not self.head:
            print("Patient list is empty.")
            return
        if self.head.patient_id == patient_id:
            self.head = self.head.next
            return
        prev_patient = self.head
        current_patient = self.head.next
        while current_patient:
            if current_patient.patient_id == patient_id:
                prev_patient.next = current_patient.next
                return
            prev_patient = current_patient
            current_patient = current_patient.next
        print("Patient with ID", patient_id, "not found.")

    def update_patient_condition(self, patient_id, new_condition):
        """
        Updates the condition of a patient with the given ID.
        """
        current_patient = self.head
        while current_patient:
            if current_patient.patient_id == patient_id:
                current_patient.condition = new_condition
                return
            current_patient = current_patient.next
        print("Patient with ID", patient_id, "not found.")

    def view_patients(self):
        """
        Displays information about all patients in the list.
        """
        current_patient = self.head
        while current_patient:
            print("ID:", current_patient.patient_id, "Name:", current_patient.name, "Age:", current_patient.age, "Condition:", current_patient.condition)
            current_patient = current_patient.next

# Hospital System for singly linked list
class HospitalSystem1:
    def __init__(self):
        """
        Represents a hospital system with a patient list.
        """
        self.patient_list = PatientSinglyLinkedList()

    def add_patient_record(self, patient):
        """
        Adds a patient record to the hospital system.
        """
        self.patient_list.add_patient(patient)

    def remove_patient_record(self, patient_id):
        """
        Removes a patient record from the hospital system based on their ID.
        """
        self.patient_list.remove_patient(patient_id)

    def update_patient_condition(self, patient_id, new_condition):
        """
        Updates the condition of a patient in the hospital system.
        """
        self.patient_list.update_patient_condition(patient_id, new_condition)

    def view_all_patients(self):
        """
        Displays information about all patients in the hospital system.
        """
        self.patient_list.view_patients()

# Example usage:
hospital = HospitalSystem1()
patient1 = PatientSinglyNode(1, "Hessa", 19, "Fever")
patient2 = PatientSinglyNode(2, "Amna", 25, "Cough")
hospital.add_patient_record(patient1)
hospital.add_patient_record(patient2)
print("Patients in the hospital:")
hospital.view_all_patients()
print("\nUpdating patient condition...")
hospital.update_patient_condition(1, "Recovered")
print("\nPatients after update:")
hospital.view_all_patients()
print("\nRemoving patient with ID 2...")
hospital.remove_patient_record(2)
print("\nPatients after removal:")
hospital.view_all_patients()


# Doubly linked list node
class PatientDoublyNode:
    """Class representing a patient."""
    def __init__(self, patient_id, name, age, condition):
        """Initialize a patient with given attributes."""
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.condition = condition
        self.next = None  # Reference to the next patient node
        self.prev = None  # Reference to the previous patient node

# Doubly linked list class
class PatientDoublyLinkedList:
    """Class representing a doubly linked list of patients."""
    def __init__(self):
        """Initialize an empty doubly linked list."""
        self.head = None  # Reference to the first patient node
        self.tail = None  # Reference to the last patient node

    def add_patient(self, patient):
        """Add a patient to the end of the doubly linked list."""
        if not self.head:
            self.head = patient
            self.tail = patient
        else:
            self.tail.next = patient
            patient.prev = self.tail
            self.tail = patient

    def remove_patient(self, patient_id):
        """Remove a patient with the given ID from the doubly linked list."""
        current_patient = self.head
        while current_patient:
            if current_patient.patient_id == patient_id:
                if current_patient == self.head:
                    self.head = current_patient.next
                    if self.head:
                        self.head.prev = None
                    else:
                        self.tail = None
                elif current_patient == self.tail:
                    self.tail = current_patient.prev
                    self.tail.next = None
                else:
                    current_patient.prev.next = current_patient.next
                    current_patient.next.prev = current_patient.prev
                return
            current_patient = current_patient.next
        print("Patient with ID", patient_id, "not found.")

    def update_patient_condition(self, patient_id, new_condition):
        """Update the condition of a patient with the given ID."""
        current_patient = self.head
        while current_patient:
            if current_patient.patient_id == patient_id:
                current_patient.condition = new_condition
                return
            current_patient = current_patient.next
        print("Patient with ID", patient_id, "not found.")

    def view_patients(self):
        """View all patients in the doubly linked list."""
        current_patient = self.head
        while current_patient:
            print("ID:", current_patient.patient_id, "Name:", current_patient.name, "Age:", current_patient.age, "Condition:", current_patient.condition)
            current_patient = current_patient.next

# Hospital system for doubly linked lists
class HospitalSystem2:
    """Class representing a hospital system."""
    def __init__(self):
        """Initialize a hospital system with a patient doubly linked list."""
        self.patient_list = PatientDoublyLinkedList()

    def add_patient_record(self, patient):
        """Add a patient record to the hospital system."""
        self.patient_list.add_patient(patient)

    def remove_patient_record(self, patient_id):
        """Remove a patient record from the hospital system."""
        self.patient_list.remove_patient(patient_id)

    def update_patient_condition(self, patient_id, new_condition):
        """Update the condition of a patient in the hospital system."""
        self.patient_list.update_patient_condition(patient_id, new_condition)

    def view_all_patients(self):
        """View all patients in the hospital system."""
        self.patient_list.view_patients()

# Example usage:
hospital = HospitalSystem2()
patient1 = PatientDoublyNode(1, "Shamsa", 19, "Fever")
patient2 = PatientDoublyNode(2, "Mahra", 25, "Cough")
hospital.add_patient_record(patient1)
hospital.add_patient_record(patient2)
print("Patients in the hospital:")
hospital.view_all_patients()
print("\nUpdating patient condition...")
hospital.update_patient_condition(1, "Recovered")
print("\nPatients after update:")
hospital.view_all_patients()
print("\nRemoving patient with ID 2...")
hospital.remove_patient_record(2)
print("\nPatients after removal:")
hospital.view_all_patients()

