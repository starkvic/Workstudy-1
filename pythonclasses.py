#create an employee class
class Employee:
    """class variable will go hear. A class variable is shared among all instances"""
    raise_amount = 1.04
    num_of_employees=0


    #create a constructor 
    #A constructor contain instance variables
    """An instance varible is only for a particular instance while.This mean that an instant variable is unique for a particular instance"""
    def __init__(self,first_name,last_name,age,pay):
        self.first_name=first_name
        self.last_name = last_name
        self.age = age
        self.pay=pay

        #Use the class name to avoid a class variable from being overridden by an instance
        Employee.num_of_employees+=1

    "Here are regular methods that automatically pass the instance as the first argument, that is self"
    @property
    def fullname(self):
        return '{} {}'.format(self.first_name,self.last_name)
    def apply_raise(self):
        #Here we can use both self and class name with the raise_amount class variable
        # The difference is that with class name the constant cannot be changed by any instance or subclass
        """But with self.raise_amount, this mean that an instance/subclass can be used to change the value or override the default"""
        self.pay = int(self.pay * self.raise_amount)
        return self.pay
    
    "Here are class methods that pass the class as the first argument, that is cls"
    """ The decorator @classmethod can be used as an alternative constructor"""
    @classmethod
    def set_raise_amount(cls,amount):
        cls.raise_amount = amount
    """ The decorator @classmethod can be used as an alternative constructor Here is a good example"""
    @classmethod
    def create_instance_from_string(cls,instant_str):
        first_name,last_name,age,pay=instant_str.split('-')
        return cls(first_name,last_name,age,pay)
    
    "Here are static methods that don't pass anything at all"
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or  day.weekday() ==6:
            return False
        return True


    "Class special methods/Dunder/Double underscore methods"
    def __repr__(self):
        return "Employee('{}','{}','{}','{}')".format(self.first_name,self.last_name,self.age,self.pay)
    
    def __str__(self):
        return "{}-{}-{}".format(self.first_name,self.last_name,self.age)
    
    "Add employee salary "
    def __add__(self,other):
        return self.pay+other.pay
    
    "Use len(obj) or use the lenght function on objects"

    def __len__(self):
        return len(self.fullname)
    

    "The @property decorator is used to access a method as an attribute For example "
    @property
    def email(self):
        return '{}{}@gmail.com'.format(self.first_name,self.last_name)


    "Setters used to set the first and last name from full name"
    @fullname.setter
    def fullname(self,name):
        self.first_name,self.last_name = name.split(' ')

    "Deleters are used to delete the full name then set the firs_name and last_name to none"
    @fullname.deleter
    def fullname(self):
        print("Deleted Full Name!")
        self.first_name,self.last_name = None,None

    

#python class inheritance and subclasses
#Changes can be made in  the subclasses without affecting the parent class

class Developer(Employee):
    "For example you can change the raise_amount value"
    raise_amount = 1.05
    def __init__(self,first_name,last_name,age,pay,prog_lang):
        super().__init__(first_name,last_name,age,pay)
        self.prog_lang = prog_lang

class Manager(Employee):
    def __init__(self,first_name,last_name,age,pay,employees=None):
        super().__init__(first_name,last_name,age,pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
    def add_emp(self,emp):
        if emp not in self.employees:
            self.employees.append(emp)
    def remove_emp(self,emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->',emp.fullname)










dev_1 = Developer('Ian','Aron',23,6000,'Javascript')#'Brian-Aron-23-6000-Javascript')
dev_2 = Developer('Bullest','Ben',23,4000,'C++')#'Bullest-Ben-23-6000-C++')

print(dev_1+dev_2)
print(len(dev_1))

"Still using email as if it's an attribute though it's a method"
print(dev_1.email)

"The same can be done to fullname"
print(dev_1.fullname)

"Use of setters to get first_name and last_name from given full name"
dev_1.fullname = "Michael Green"
print(dev_1.first_name,dev_1.last_name)
#The same update is done to the email
print(dev_1.email)

"Use of deleter"
del dev_1.fullname
print(dev_1.first_name)



    
# # print(dev_1.email)
# # print(dev_1.prog_lang)
# mgr_1 = Manager('Lauryn','Bedzame',23,7000,[dev_1])
# mgr_1.add_emp(dev_2)
# mgr_1.remove_emp(dev_1)
# print(mgr_1.print_emps())

"Check is an object is an instance or a subclass"
# print(isinstance(dev_2,Developer))
# print(issubclass(Manager,Employee))




"Making use of help functionality"
#print(help(Developer))


# emp1 = Employee('Lennox','Kahati',21,5000)
# print(emp1.get_fullname())
# print(Employee.get_fullname(emp1))
# print(emp1.apply_raise())
# print(emp1.__dict__)
# print("employees number",emp1.num_of_employees)
# Employee.set_raise_amount(1.06)
# print(emp1.raise_amount)
# emp2 = Employee.create_instance_from_string('Brian-Aron-23-6000')
# print(emp2.get_fullname())

# import datetime
# my_date = datetime.date(2016,3,16)
# print(my_date.weekday())
# print(Employee.is_workday(my_date))

try:
    x,y=5
except Exception as e:
    print(e)
    f=None
    print("hhsg"+f)

print(len("h-h".split('-')))


