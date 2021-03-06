from getpass import getpass

from src import Main


class Worker:
    def __init__(self):
        self.worker_id = None
        self.conn = Main.create_connection()

    def worker_login(self):
        """
        worker authentication.
        :return:
        """
        email = input("Enter Email Id: ")
        sql = "SELECT email,password,id FROM Employees WHERE email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()
        if record:
            if record[1] is None:
                password = getpass('First time Login. Enter Password: ')
                sql = "Update Employees SET password = '{}' WHERE id = {}".format(password, record[2])
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                self.worker_id = record[2]
                return True
            else:
                password = getpass('Enter Password: ')
                if record[1] == password:
                    print("Authentication Successful")
                    self.worker_id = record[2]
                    return True
                else:
                    print("Authentication failed. Please check your credentials")
                    return False
        else:
            print("User does not exist")
            return False

    def worker_tasks(self):
        """
        show worker tasks.
        :return:
        """
        option = ''
        while option != '5':
            print("\nMenu\n"
                  "1: Create Complaint\n"
                  "2: Show Complaint History\n"
                  "3: Show Active Complaints\n"
                  "4: Show Profile\n"
                  "5: Exit\n")
            option = input("Select Your Option ")

            if option == '1':
                self.create_complaint()
            elif option == '2':
                self.show_complaint_history()
            elif option == '3':
                self.show_active_complaints()
            elif option == '4':
                self.show_worker_profile()
            elif option == '5':
                print("Thank You")
            else:
                print("Invalid choice")

    def create_complaint(self):
        """
        create new complaint.
        :return:
        """
        try:
            accident_name = input("Enter details: ")
            comments = input("Enter comments: ")

            sql = """INSERT INTO Complaints (accident_name, comments, worker_id)
                                VALUES ('{}','{}',{})""".format(accident_name, comments, self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            print("Complaint created successfully!")
            return True
        except Exception as e:
            print("Error is", e)
            return False

    def show_complaint_history(self):
        """
        show complaint history.
        :return:
        """
        try:
            sql = "select * from Complaints where worker_id = {}".format(self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                result = cur.fetchall()
            print(result)
            if result:
                for i in result:
                    print("id : {}".format(i[0]))
                    print("Accident_name : {}".format(i[1]))
                    print("Comments : {}".format(i[2]))
                    print("Status : {}".format(i[4]))
                    print("----------------------------")
                return True
            else:
                print("Record not found")
                return False

        except Exception as e:
            print("Error in reading data")
            return False

    def show_active_complaints(self):
        """
        show complaints with investigation status WIP.
        :return:
        """
        try:
            sql = "select * from Complaints where worker_id = {} and status = 'WIP'".format(self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                result = cur.fetchall()
            if result:
                for i in result:
                    print("Complaint_id : {}".format(i[0]))
                    print("Accident_name : {}".format(i[1]))
                    print("Comments : {}".format(i[2]))
                    print("Status : {}".format(i[4]))
                    print("----------------------------")
                    return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Error in reading data")
            return False

    def show_worker_profile(self):
        """
        show profile details.
        :return:
        """
        try:
            sql = "select * from Employees where id = {}".format(self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                result = cur.fetchone()
            print("Employee_id : {}".format(result[0]))
            print("Name : {}".format(result[1]))
            print("Email : {}".format(result[2]))
            print("Role : {}".format(result[4]))
            return True
        except Exception as e:
            print("Error in reading data")
            return False
