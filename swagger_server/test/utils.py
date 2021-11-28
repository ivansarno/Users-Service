from swagger_server.controllers.default_controller import prize
from swagger_server.database import db
from swagger_server.database import User as DBUser
from swagger_server.database import Report as DBReport


def create_user(client, mail, firstname, lastname, date_of_birth, password):
    """
    Utility function to create a new user in the tests
    """

    user = DBUser()
    user.email = mail
    user.firstname = firstname
    user.lastname = lastname
    user.set_password(password)
    user.date_of_birth = date_of_birth
    db.session.add(user)
    db.session.commit()


# a counter to create uniques example users
_next_example_user = 1
_next_example_report = 1


def create_ex_usr(client):
    """
    Create an unique example user with username = user<counter and
    this data:
    (username@example.com, username, username, "02/02/2000", passusername)
    :param client: the testing app
    :return: (email, password) of the new user
    """
    global _next_example_user
    name = "user" + str(_next_example_user)
    _next_example_user += 1
    email = name + "@example.com"
    password = "pass" + name
    create_user(client, email, name, name, "02/02/2000", password)
    return email, password


def create_ex_users(client, number):
    """
    Create multiple example users
    :param client: the testing app
    :param number: number of users to create
    :return: list of (email, password) tuple of the new users
    """
    return [create_ex_usr(client) for _ in range(number)]



def get_usr_id(email):
    usr = db.session.query(DBUser).filter(DBUser.email == email).first()
    return usr.id

def get_usr(email):
    usr = db.session.query(DBUser).filter(DBUser.email == email).first()
    return usr

def set_usr_points(email, points=prize):
    usr = db.session.query(DBUser).filter(DBUser.email == email).first()
    usr.points += points
    db.session.commit()

def set_filter_t(email):
    usr = db.session.query(DBUser).filter(DBUser.email == email).first()
    usr.content_filter = True
    db.session.commit()

def create_ex_report():
    global _next_example_report
    report = DBReport()
    report.author_email = "user" + str(_next_example_user-1) + "@example.com"
    report.reported_email = "user" + str(_next_example_user) + "@example.com"
    report.timestamp = "01/01/2000"
    report.description = "Report number: " + str(_next_example_report)
    _next_example_report += 1
    db.session.add(report)
    db.session.commit()
    return report.author_email, report.description

def get_report(author):
    return db.session.query(DBReport).filter(DBReport.author_email == author).first()

