# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.controllers.default_controller import prize
from swagger_server.models.new_user import NewUser  # noqa: E501
from swagger_server.models.report import Report  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import create_ex_usr, get_usr_id, get_usr, \
    set_usr_points, set_filter_t, create_ex_report, create_ex_users, get_report


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_points(self):
        """Test case for add_points

        add points to the user
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='PUT',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode(
                           'utf-8'))
        user = get_usr(email)
        self.assertEqual(user.points, prize)

        # try a not existing user
        id += 1000
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='PUT',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode(
                           'utf-8'))

    def test_create_user(self):
        """Test case for create_user

        create a new user
        """
        data = NewUser()
        data.email = "example@example.com"
        data.firstname = "example"
        data.lastname = "example"
        data.password = "1234"
        data.date_of_birth = "01/01/2000"
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIsNotNone(get_usr("example@example.com"))

        # try a second time and receive a user already exists error
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assertStatus(response, 409)

    def test_decr_points(self):
        """Test case for decr_points

        decrease points to the user
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        set_usr_points(email)
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        user = get_usr(email)
        self.assertEqual(user.points, 0)

        # try to set a negative points count
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='DELETE',
            content_type='application/json')
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # try a not existing user
        id += 1000
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='DELETE',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        check if the user exist,
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        response = self.client.open(
            '/users/by_id/{id}'.format(id=id),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIsNone(get_usr(email))

    def test_edit_user(self):
        """Test case for edit_user

        edit the user's data
        """

        email, _ = create_ex_usr()
        id = get_usr_id(email)
        data = User()
        data.id = id
        data.firstname = "changed_name"
        response = self.client.open(
            '/users',
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        user = get_usr(email)
        self.assertEqual(user.firstname, "changed_name")

        # try a not existing user
        data.id += 1000
        response = self.client.open(
            '/users',
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # try a invalid input
        data = User()
        response = self.client.open(
            '/users',
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_exist_by_id(self):
        """Test case for exist_by_id

        check if the user exist,
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        response = self.client.open(
            '/users/by_id/{id}'.format(id=id),
            method='HEAD',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # try a not existing user
        id += 1000
        response = self.client.open(
            '/users/by_id/{id}'.format(id=id),
            method='HEAD',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_exist_by_mail(self):
        """Test case for exist_by_mail

        check if the user exist
        """
        email, _ = create_ex_usr()
        response = self.client.open(
            '/users/by_mail/{email}'.format(email=email),
            method='HEAD',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # try a not existing user
        email = "notexist@example.com"
        response = self.client.open(
            '/users/by_mail/{email}'.format(email=email),
            method='HEAD',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_by_id(self):
        """Test case for get_by_id

        get the user's data
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        response = self.client.open(
            '/users/by_id/{id}'.format(id=id),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn(bytes(email, 'utf-8'), response.data)

        # try a not existing user
        id += 1000
        response = self.client.open(
            '/users/by_id/{id}'.format(id=id),
            method='GET',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_by_mail(self):
        """Test case for get_by_mail

        get the user's data
        """
        email, _ = create_ex_usr()
        response = self.client.open(
            '/users/by_mail/{email}'.format(email=email),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn(bytes(email, 'utf-8'), response.data)

        # try a not existing user
        email = "notexist@example.com"
        response = self.client.open(
            '/users/by_mail/{email}'.format(email=email),
            method='GET',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_points(self):
        """Test case for get_points

        get the user's points
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(response.data, b'0\n')

        # try a not existing user
        id += 1000
        response = self.client.open(
            '/points/{id}'.format(id=id),
            method='GET',
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_reports(self):
        """Test case for get_reports

        get reports
        """
        _, description = create_ex_report()
        response = self.client.open(
            '/report',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn(bytes(description, "utf-8"), response.data)

    def test_get_users_list(self):
        """Test case for get_users_list

        get the list of the users
        """
        email, _ = create_ex_usr()
        response = self.client.open(
            '/users',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        self.assertIn(bytes(email, 'utf-8'), response.data)

    def test_report_user(self):
        """Test case for report_user

        report a user
        """
        users = create_ex_users(2)
        author = users[0][0]
        reported = users[1][0]
        data = Report()
        data.author_email = author
        data.reported_email = reported
        data.timestamp = "01/01/2000"
        data.description = "test report"
        response = self.client.open(
            '/report',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIsNotNone(get_report(author))

        # try a not existing user
        data.author_email = "notexist@example.com"
        response = self.client.open(
            '/report',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # try author mail == reported mail case
        data.author_email = data.reported_email
        response = self.client.open(
            '/report',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_filter(self):
        """Test case for set_filter

        set content filter
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        response = self.client.open(
            '/filter/{id}'.format(id=id),
            method='PUT',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        usr = get_usr(email)
        self.assertEqual(usr.content_filter, True)

    def test_unset_filter(self):
        """Test case for unset_filter

        unset content filter
        """
        email, _ = create_ex_usr()
        id = get_usr_id(email)
        set_filter_t(email)
        response = self.client.open(
            '/filter/{id}'.format(id=id),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        usr = get_usr(email)
        self.assertEqual(usr.content_filter, False)


if __name__ == '__main__':
    import unittest

    unittest.main()
