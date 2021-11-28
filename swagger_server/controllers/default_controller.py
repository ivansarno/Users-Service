from datetime import datetime

import connexion
import six
from flask import jsonify

from swagger_server.models.new_user import NewUser  # noqa: E501
from swagger_server.models.report import Report  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
from swagger_server.database import User as DBUser
from swagger_server.database import Report as DBReport
from swagger_server.database import db

# lottery constants
prize = 100
price = 100


def add_points(id):  # noqa: E501
    """add points to the user

    Add the fixed \&quot;prize\&quot; quantity of points to the user&#39;s account.  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        return None, 404
    user.points += prize
    db.session.commit()
    return None, 200


def create_user(data):  # noqa: E501
    """create a new user

    Create a new user from provided user&#39;s data.  # noqa: E501

    :param data: new user&#39;s data
    :type data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        data = NewUser.from_dict(connexion.request.get_json())  # noqa: E501
        if db.session.query(DBUser) \
                .filter(DBUser.email == data.email).first():
            return None, 409
        user = _user2dbuser(data)
        db.session.add(user)
        db.session.commit()
        return None, 200
    return None, 400


def decr_points(id):  # noqa: E501
    """decrease points to the user

    Remove the fixed \&quot;price\&quot; quantity of points to the user&#39;s account.  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        return None, 404
    if user.points < price:
        return None, 401
    user.points -= price
    db.session.commit()
    return None, 200


def delete_user(id):  # noqa: E501
    """check if the user exist,

    Delete a user, referenced by id  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return None, 200


def edit_user(data):  # noqa: E501
    """edit the user&#39;s data

    Edit the user&#39;s data, id is required, only the data to change must be provided.  # noqa: E501

    :param data: new user&#39;s data, the id field is required
    :type data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        data = connexion.request.get_json()  # noqa: E501
        id = data.get('id')
        user = db.session.query(DBUser).filter(DBUser.id == id).first()
        if user is None:
            return None, 404
        _edit_dbuser(user, data)
        db.session.commit()
        return None, 200
    return None, 400


def exist_by_id(id):  # noqa: E501
    """check if the user exist,

    Check if the user exist, referenced by id  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        return None, 404
    return None, 200


def exist_by_mail(email):  # noqa: E501
    """check if the user exist

    Check if the user exist, referenced by mail.  # noqa: E501

    :param email: user&#39;s email
    :type email: str

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.email == email).first()
    if user is None:
        return None, 404
    return None, 200



def get_by_id(id):  # noqa: E501
    """get the user&#39;s data

    Get the user&#39;s data, referenced by id.  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: User
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        return None, 404
    user = _dbuser2user(user)
    return jsonify(user), 200


def get_by_mail(email):  # noqa: E501
    """get the user&#39;s data

    Get the user&#39;s data, referenced by mail.  # noqa: E501

    :param email: user&#39;s email
    :type email: str

    :rtype: User
    """
    user = db.session.query(DBUser).filter(DBUser.email == email).first()
    if user is None:
        return None, 404
    user = _dbuser2user(user)
    return jsonify(user), 200


def get_points(id):  # noqa: E501
    """get the user&#39;s points

    Get the user&#39;s lottery points.  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: int
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        return None, 404
    return user.points, 200


def get_reports():  # noqa: E501
    """get reports

    Get the reports.  # noqa: E501


    :rtype: List[Report]
    """
    query_reports = db.session.query(DBReport).order_by(DBReport.id.desc())
    reports = [_dbreport2report(r) for r in query_reports]
    return jsonify(reports), 200


def get_users_list():  # noqa: E501
    """get the list of the users

    Get the list of the users.  # noqa: E501


    :rtype: List[User]
    """
    query = db.session.query(DBUser).order_by(DBUser.id)
    users = [_dbuser2user(u) for u in query]
    return jsonify(users)


def report_user(data):  # noqa: E501
    """report a user

    Report a user.  # noqa: E501

    :param data: content of the report, the id will be assigned automatically
    :type data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        data = Report.from_dict(connexion.request.get_json())  # noqa: E501
        if data.reported_email == data.author_email:
            return None, 400
        reported = db.session.query(DBUser) \
            .filter(DBUser.email == data.reported_email).first()
        author = db.session.query(DBUser) \
            .filter(DBUser.email == data.author_email).first()
        if not (reported and author):
            return None, 404
        report = _report2dbreport(data)
        db.session.add(report)
        db.session.commit()
        return None, 200
    return None, 400


def set_filter(id):  # noqa: E501
    """set content filter

    Set the content filter.  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is not None:
        user.content_filter = True
        db.session.commit()
    return None, 200


def unset_filter(id):  # noqa: E501
    """unset content filter

    Unset the content filter.  # noqa: E501

    :param id: user&#39;s id
    :type id: int

    :rtype: None
    """
    user = db.session.query(DBUser).filter(DBUser.id == id).first()
    if user is not None:
        user.content_filter = False
        db.session.commit()
    return None, 200


def _user2dbuser(data):
    user = DBUser()
    user.email = data.email
    user.firstname = data.firstname
    user.lastname = data.lastname
    user.set_password(data.password)
    user.date_of_birth = data.date_of_birth
    return user


def _dbuser2user(data: DBUser):
    user = User(
        data.id,
        data.email,
        data.firstname,
        data.lastname,
        data.password,
        data.date_of_birth,
        data.points
    )
    return user


def _edit_dbuser(user: DBUser, data: dict):
    user.email = data.get('email', user.email)
    user.firstname = data.get('firstname', user.firstname)
    user.lastname = data.get('lastname', user.lastname)
    user.password = data.get('password', user.password)


def _report2dbreport(data: Report):
    report = DBReport()
    report.author_email = data.author_email
    report.reported_email = data.reported_email
    report.timestamp = data.timestamp
    report.description = data.description
    return report


def _dbreport2report(data: DBReport):
    report = Report()
    report.author_email = data.author_email
    report.reported_email = data.reported_email
    report.timestamp = data.timestamp
    report.description = data.description
    return report

