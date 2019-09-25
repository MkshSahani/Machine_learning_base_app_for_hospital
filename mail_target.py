# for mail the required info to the targeted patient.

import pymysql
import patient_mail_gen
# def gen_patient_mail(degi,dept,mess, to):
import mail
def main_target_patient(patient_uid, department_id):
    if patient_uid != []:
        filelist = ["tips_medicine_patient.txt","tips_ent_patient.txt","tips_eye_patient.txt","tips_heart_patient.txt","tips_allergy_patient.txt","tips_psycho_patient.txt","tips_surgery_patient.txt"]
        main_sql_server = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
        sql_cursor = main_sql_server.cursor()
        patient_uid_data = tuple(patient_uid)
        sql_statement = f"select username from pat_uid where p_uid in {patient_uid_data}"
        sql_cursor.execute(sql_statement)
        usernamedata = sql_cursor.fetchall()
        print(usernamedata)
        data_username = []
        for i in usernamedata:
            for j in i:
                data_username.append(j)
        print(data_username)
        data_username = tuple(data_username)
        sql_statement = f"select email from Patient where username in {data_username}"
        sql_cursor.execute(sql_statement)
        data_email = sql_cursor.fetchall()
        print(data_email)
        data_need_email = []
        for i in data_email:
            for j in i:
                data_need_email.append(j)
        print(data_need_email)
        main_sql_server.close()
        index_value = 0
        em_dict = zip(data_need_email, department_id)
        em_dict = dict(em_dict)
        print(em_dict)
        dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgeon"]
        i = 0
        for em in data_need_email:
            try:
                f = open(filelist[department_id[i]],'r')
                text_file = f.read()
                f.close()
                body_of_mail = patient_mail_gen.gen_patient_mail("System", dlist[department_id[i]], text_file, em)
                mail.mail_function(em, text_file)
                print(f"Mail send to {em} from system for {dlist[department_id[i]]} department")
                i += 1
            except:
                pass

if __name__ == '__main__':
    main_target_patient([61000, 61001],[1,2])
