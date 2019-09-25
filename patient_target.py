import pymysql
import pandas as pd
import mail_target
conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
c = conn.cursor()
sql = "select p_uid from pat_uid"
c.execute(sql)
data = c.fetchall()
conn.close()
val = []
for i in data:
    for j in i:
        val.append(j)
val.pop(0)
department_list = []
dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgon"]
dname_data = []
for i in val:
    try:
        data_file_load = pd.read_csv(f"patient_data/{i}/department_hostpital.csv")
        print(data_file_load)
        patient_data = data_file_load.iloc[:,1].values
        print(patient_data)
        patient_data = list(patient_data)
        max_visit_department = max(patient_data)
        if max_visit_department == 0:
            pass
            val.pop(i)
        else:
            department_list.append(patient_data.index(max_visit_department))
        dname_data.append(dlist[patient_data.index(max_visit_department)])
    except:
        pass

print(department_list)
print(dname_data)
final_data_deptname = zip(val, dname_data)
final_data = dict(final_data_deptname)
final_data_lite = zip(val,department_list)
final_number_data = dict(final_data_lite)
print(final_data)
print(final_number_data)
print(val)
print(department_list)
mail_target.main_target_patient(val, department_list)
