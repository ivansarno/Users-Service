# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class NewUser(Model):
    """NOTE: This class is auto generated by the swagger code generator program

    Do not edit the class manually.
    """

    def __init__(self, email: str = None, firstname: str = None,
                 lastname: str = None, password: str = None,
                 date_of_birth: str = None):  # noqa: E501
        """NewUser - a model defined in Swagger

        :param email: The email of this NewUser.  # noqa: E501
        :type email: str
        :param firstname: The firstname of this NewUser.  # noqa: E501
        :type firstname: str
        :param lastname: The lastname of this NewUser.  # noqa: E501
        :type lastname: str
        :param password: The password of this NewUser.  # noqa: E501
        :type password: str
        :param date_of_birth: The date_of_birth of this NewUser.  # noqa: E501
        :type date_of_birth: str
        """
        self.swagger_types = {
            'email': str,
            'firstname': str,
            'lastname': str,
            'password': str,
            'date_of_birth': str
        }

        self.attribute_map = {
            'email': 'email',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'password': 'password',
            'date_of_birth': 'date_of_birth'
        }

        self._email = email
        self._firstname = firstname
        self._lastname = lastname
        self._password = password
        self._date_of_birth = date_of_birth

    @classmethod
    def from_dict(cls, dikt) -> 'NewUser':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NewUser of this NewUser.  # noqa: E501
        :rtype: NewUser
        """
        return util.deserialize_model(dikt, cls)

    @property
    def email(self) -> str:
        """Gets the email of this NewUser.


        :return: The email of this NewUser.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this NewUser.


        :param email: The email of this NewUser.
        :type email: str
        """
        if email is None:
            raise ValueError(
                "Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def firstname(self) -> str:
        """Gets the firstname of this NewUser.


        :return: The firstname of this NewUser.
        :rtype: str
        """
        return self._firstname

    @firstname.setter
    def firstname(self, firstname: str):
        """Sets the firstname of this NewUser.


        :param firstname: The firstname of this NewUser.
        :type firstname: str
        """
        if firstname is None:
            raise ValueError(
                "Invalid value for `firstname`, must not be `None`")  # noqa: E501

        self._firstname = firstname

    @property
    def lastname(self) -> str:
        """Gets the lastname of this NewUser.


        :return: The lastname of this NewUser.
        :rtype: str
        """
        return self._lastname

    @lastname.setter
    def lastname(self, lastname: str):
        """Sets the lastname of this NewUser.


        :param lastname: The lastname of this NewUser.
        :type lastname: str
        """
        if lastname is None:
            raise ValueError(
                "Invalid value for `lastname`, must not be `None`")  # noqa: E501

        self._lastname = lastname

    @property
    def password(self) -> str:
        """Gets the password of this NewUser.


        :return: The password of this NewUser.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this NewUser.


        :param password: The password of this NewUser.
        :type password: str
        """
        if password is None:
            raise ValueError(
                "Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password

    @property
    def date_of_birth(self) -> str:
        """Gets the date_of_birth of this NewUser.


        :return: The date_of_birth of this NewUser.
        :rtype: str
        """
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str):
        """Sets the date_of_birth of this NewUser.


        :param date_of_birth: The date_of_birth of this NewUser.
        :type date_of_birth: str
        """
        if date_of_birth is None:
            raise ValueError(
                "Invalid value for `date_of_birth`, must not be `None`")  # noqa: E501

        self._date_of_birth = date_of_birth
