import mysql.connector as connector


class QuizDB:
    def __init__(self):

        self._con = connector.connect(user="root", password="Ishu2004*",
                                      host="localhost", port="3306", database="QUIZDB"
                                      )

        self._cursor = self._con.cursor()
        self.__create_table()

    def __create_table(self):
        __table_query = """CREATE TABLE IF NOT EXISTS
        MCQ (
            question_no INT PRIMARY KEY AUTO_INCREMENT,
            question VARCHAR(150) UNIQUE NOT NULL,
            op_a VARCHAR(50) NOT NULL,
            op_b VARCHAR(50) NOT NULL,
            op_c VARCHAR(50) NOT NULL,
            op_d VARCHAR(50) NOT NULL,
            correct CHAR(1) NOT NULL
            );"""

        self._cursor.execute(__table_query)

        __auto_inc_query = "ALTER TABLE MCQ AUTO_INCREMENT=1;"
        self._cursor.execute(__auto_inc_query)
        self._con.commit()

    def insert_mcq(self, question, op_a, op_b, op_c, op_d, correct):
        __query = """INSERT INTO MCQ VALUES (default, %s, %s, %s, %s, %s, %s);"""
        self._cursor.execute(__query,
                             (question, op_a, op_b, op_c, op_d, correct))
        self._con.commit()

    def delete_mcq(self, q_no):
        __query = "DELETE FROM MCQ WHERE question_no=%s;"
        self._cursor.execute(__query, (q_no,))
        self._con.commit()

    def get_mcq(self, q_no):
        __query = "SELECT * FROM MCQ WHERE question_no=%s;"
        self._cursor.execute(__query, (q_no,))
        return self._cursor.fetchone()

    def get_all_mcq(self):
        __query = "SELECT * FROM MCQ ORDER BY question_no;"
        self._cursor.execute(__query)
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()
        self._con.close()


if __name__ == "__main__":
    mydb = QuizDB()
    """QUERIES TO ADD SOME MCQs"""
    # mydb.insert_mcq(
    #     "What is the full form of WWW ?",
    #     "World Wide Ware", "World Wide Website",
    #     "World Wide Web", "World Wide Weather",
    #     correct="c"
    # )
    # mydb.insert_mcq(
    #     "MAN stands for ?",
    #     "Metropolitan Area Network", "Main Area Network",
    #     "Metrpolitan Access Network", "Metro Access Network",
    #     correct="a"
    # )
    # mydb.insert_mcq(
    #     "Which of the following is the smallest network ?",
    #     "WAN", "MAN", "PAN", "LAN", correct="c"
    # )
    # mydb.insert_mcq(
    #     "A device that forwards data packet from one network to another is called a",
    #     "Bridge", "Router", "Hub", "Gateway", correct="b"
    # )
    # mydb.insert_mcq(
    #     "The device that can operate in place of a hub is a",
    #     "Switch", "Bridge", "Router", "Gateway", correct="a"
    # )
    # mydb.insert_mcq(
    #     "In computer, converting a digital signal in to an analog signal is called",
    #     "modulation", "demodualation", "conversion", "transformation",
    #     correct="a"
    # )
    mydb.close()
