import json # Import to let us parse the JSON data
from datetime import datetime # Import to let us find difference between start and end times

# Class to store employee data
class Employee:
    def __init__(self, name):
        self.name = name

        self.hours = 0
        self.regular = 0
        self.overtime = 0
        self.doubletime = 0

        self.wageTotal = 0
        self.benefitTotal = 0

    # Update function to do the calculations based on the hours and rate
    # This properly calculates the regular, overtime, and doubletime wages for each shift with various checks
    def update(self, hours, rate, benefit_rate):

        self.hours += hours
        self.benefitTotal += benefit_rate * hours

        if self.hours <= 40:
            self.regular += hours * rate

        # Example:
        # If the employee has worked 42 hours and the current shift is 6 hours,
        # the first 4 hours are regular, the next 2 hours are overtime
        elif self.hours >= 40 and self.hours - hours <= 40:
            self.regular += (hours - (self.hours - 40)) * rate 
            self.overtime += (self.hours - 40) * (rate * 1.5)

        elif self.hours >= 40 and self.hours < 48:
            self.overtime += rate * 1.5 * hours

        elif self.hours >= 48 and self.hours - hours < 48:
            self.overtime += (hours - (self.hours - 48)) * (rate * 1.5)
            self.doubletime += (self.hours - 48) * (rate * 2)

        else:
            self.doubletime += hours * (rate * 2)

    # Function to calculate total hours in each cateogry
    def get_hours(self):
        regular, overtime, doubletime = 0, 0, 0
        if self.hours <= 40:
            regular = self.hours
        elif self.hours > 40 and self.hours <= 48:
            regular = 40
            overtime = self.hours - 40
        elif self.hours > 48:
            regular = 40
            overtime = 8
            doubletime = self.hours - 48

        return regular, overtime, doubletime
    
    # Function to return values in proper output format
    def getValues(self):
        regular, overtime, doubletime = self.get_hours()
        return {
            'employee': self.name,
            'regular': f"{regular:.4f}",
            'overtime': f"{overtime:.4f}",
            'doubletime': f"{doubletime:.4f}",
            'wageTotal': f"{self.regular + self.overtime + self.doubletime:.4f}",
            'benefitTotal': f"{self.benefitTotal:.4f}"
        }
    

# Class to store the job metadata in the 'data.json' file
class JobMeta:
    def __init__(self, data):

        self.jobMeta = {}
        for job_data in data['jobMeta']:
            self.add_job(job_data['job'], job_data['rate'], job_data['benefitsRate'])
    
    def add_job(self, job, rate, benefitsRate):
        self.jobMeta[job] = {'rate': rate, 'benefits': benefitsRate}

    def get_rate(self, job):
        return self.jobMeta.get(job).get('rate', 0)
    
    def get_benefits(self, job):
        return self.jobMeta.get(job).get('benefits', 0)

    # From the testing data, this prints:
    # Job: Hospital - Painter, Rate: 31.25, Benefits: 1
    # Job: Hospital - Laborer, Rate: 20.0, Benefits: 0.5
    # Job: Shop - Laborer, Rate: 16.25, Benefits: 1.25
    def print(self):
        for job, details in self.jobMeta.items():
            print(f"Job: {job}, Rate: {details['rate']}, Benefits: {details['benefits']}")


def main():
    data = json.load(open('data.json', 'r'))
    job = JobMeta(data)
    emps = {} # tracks the employees and their wages

    # Iterate over each employee
    for record in data['employeeData']:
        name = record["employee"]
        emp = Employee(name)

        # Iterate over shifts for each employee
        for shift in record["timePunch"]:
            job_name = shift["job"]
            start = shift["start"]
            end = shift["end"]

            rate = job.get_rate(job_name)
            benefits = job.get_benefits(job_name)

            start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            total_time = (end_time - start_time).total_seconds() / 3600

            emp.update(total_time, rate, benefits)

        # Store the employee data in our result dictionary
        emps[emp.name] = emp.getValues()

    # Final print to show output in proper format
    for emp in emps.values():
        print(json.dumps(emp, indent=4))
        
            

if __name__ == "__main__":
    main()
