import mysql.connector as connection
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine

user = "root"
password = ""
host = "localhost"

try:
    mydb = connection.connect(
        host = host,
        user = user, 
        passwd = password)
    cursor = mydb.cursor()
    query = "CREATE DATABASE IF NOT EXISTS companydata;"
    cursor.execute(query)
    mydb.close() 

    mydb = connection.connect(
        host = host,
        database = 'companydata',
        user = user, 
        passwd = password)
    cursor = mydb.cursor()
    query = '''
CREATE TABLE IF NOT EXISTS employeeperformance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    department VARCHAR(255) NOT NULL,
    performance_score DECIMAL(10, 2) NOT NULL,
    years_with_company INT NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);
'''
    cursor.execute(query)
    mydb.close() 

    connection_query = f'mysql+mysqlconnector://{user}:{password}@{host}/companydata'
    engine = create_engine(connection_query)

    query = "SELECT * FROM employeeperformance;"

    result_dataFrame = pd.read_sql(query, con=engine)

    if (len(result_dataFrame) == 0):
        data = pd.read_csv("data.csv")

        data.to_sql('employeeperformance', con=engine, if_exists='append', index=False)

        result_dataFrame = pd.read_sql(query, con=engine)
except Exception as e:
    print(str(e))

def total_employees_per_department ():
    employees_by_department = result_dataFrame.groupby(by="department").count()["employee_id"]

    return employees_by_department

def mean_median_std_performance_score ():
    groupby_department = result_dataFrame.groupby(by="department")

    ps_mean = groupby_department.mean()["performance_score"]
    ps_median = groupby_department.median()["performance_score"]
    ps_std = groupby_department.std()["performance_score"]

    return {
        "mean": ps_mean, # Media
        "median": ps_median, # Mediana
        "std": ps_std, # Desviación Estandar
    }

def mean_median_std_salary ():
    groupby_department = result_dataFrame.groupby(by="department")

    s_mean = groupby_department.mean()["salary"]
    s_median = groupby_department.median()["salary"]
    s_std = groupby_department.std()["salary"]

    return {
        "mean": s_mean, # Media
        "median": s_median, # Mediana
        "std": s_std, # Desviación Estandar
    }

def correlation_year_performance():
    correlation = pd.DataFrame()

    correlation["department"] = result_dataFrame["department"]
    correlation["years_with_company"] = result_dataFrame["years_with_company"]
    correlation["performance_score"] = result_dataFrame["performance_score"]
    
    return correlation.groupby(by="department").corr()["years_with_company"].unstack()["performance_score"]

def correlation_salary_performance():
    correlation = pd.DataFrame()

    correlation["department"] = result_dataFrame["department"]
    correlation["salary"] = result_dataFrame["salary"]
    correlation["performance_score"] = result_dataFrame["performance_score"]
    
    return correlation.groupby(by="department").corr()["salary"].unstack()["performance_score"]

def hist_performance_per_department ():
    department_performance = result_dataFrame.groupby(by="department").mean()
    
    plt.bar(department_performance.index, department_performance["performance_score"])

    plt.xticks(rotation=45, ha='right')

    plt.show()

def scatter_years_performance():
    plt.scatter(result_dataFrame["years_with_company"], result_dataFrame["performance_score"])
    plt.xlabel("Años en la compañia")
    plt.ylabel("Rendimiento")
    plt.show()

def scatter_salary_performance():
    plt.scatter(result_dataFrame["performance_score"], result_dataFrame["salary"])
    plt.xlabel("Rendimiento")
    plt.ylabel("Salario")
    plt.show()