import json
from nose.tools import *
from tests import test_app, make_request, faker


def check_content_type(headers):
    eq_(headers['Content-Type'], 'application/json')


def test_Authenticate():
    # test request Authenticating
    rv = test_app.get('/api/v1/user/x5050')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    eq_(rv.status_code, 401)
    eq_(resp["error"], 'Could not verify your access level for that URL. You have to login with proper credentials')


def test_user_api():
    # testing creating new user
    data = {}
    data['username'] = faker.user_name()
    data['email'] = faker.email()
    rv = make_request(url="/api/v1/user", method="POST", data=data)
    check_content_type(rv.headers)
    res = json.loads(rv.data)
    eq_(rv.status_code, 201)
    eq_(res['user']['username'], data['username'])
    eq_(res['user']['email'], data['email'])

    # save it for couple other tests
    accountId = res['user']['account_id']

    # testing retrieving invalid user
    rv2 = make_request(url='/api/v1/user/X34RTY', method="GET")
    check_content_type(rv2.headers)
    res2 = json.loads(rv2.data)
    eq_(rv2.status_code, 404)
    eq_(res2["error"], "user not found")

    # testing retrieving the same user data
    rv2 = make_request(url='/api/v1/user/'+accountId, method="GET")
    check_content_type(rv2.headers)
    res2 = json.loads(rv2.data)
    eq_(rv2.status_code, 200)
    eq_(res2['user']['account_id'], accountId)
    eq_(res2['user']['username'], data['username'])
    eq_(res2['user']['email'], data['email'])

    #testing updating user email
    update = {}
    update['email'] = faker.email()
    update['username'] = faker.user_name()
    rv3 = make_request(url='/api/v1/user/'+accountId, method="PUT", data=update)
    check_content_type(rv3.headers)
    res3 = json.loads(rv3.data)
    eq_(rv3.status_code, 201)
    eq_(res3['user']['email'], update['email'])
    eq_(res3['user']['username'], update['username'])

    # testing update user with non email unique values
    update2 = {}
    update2['email'] = update['email']
    rv3 = make_request(url='/api/v1/user/'+accountId, method="PUT", data=update2)
    check_content_type(rv3.headers)
    res3 = json.loads(rv3.data)
    eq_(rv3.status_code, 400)
    eq_(res3["error"], "email already exists")

    # testing update user with non username unique values
    update2 = {}
    update2['username'] = update['username']
    rv3 = make_request(url='/api/v1/user/'+accountId, method="PUT", data=update2)
    check_content_type(rv3.headers)
    res3 = json.loads(rv3.data)
    eq_(rv3.status_code, 400)
    eq_(res3["error"], "username already exists")

    # testing updating user statistics
    stats = {}
    stats['wins'] = 5
    stats['losses'] = 2
    stats['score'] = 12
    stats['level'] = 3
    rv4 = make_request(url="/api/v1/user/"+accountId+"/statistics", method="POST", data=stats)
    check_content_type(rv4.headers)
    res4 = json.loads(rv4.data)
    eq_(rv4.status_code, 201)
    eq_(res4['success'], "statistics has been added successfully")

    # testing updating fake user statistics
    rv4 = make_request(url="/api/v1/user/XUXUXUXUX/statistics", method="POST", data={})
    check_content_type(rv4.headers)
    res4 = json.loads(rv4.data)
    eq_(rv4.status_code, 404)
    eq_(res4["error"], "user not found")

    # testing retrieving user statistics
    rv4 = make_request(url="/api/v1/user/"+accountId+"/statistics", method="GET")
    check_content_type(rv4.headers)
    res4 =  json.loads(rv4.data)
    eq_(rv4.status_code, 200)
    eq_(res4['statistics']['wins'], stats['wins'])
    eq_(res4['statistics']['losses'], stats['losses'])
    eq_(res4['statistics']['score'], stats['score'])
    eq_(res4['statistics']['level'], stats['level'])

    # testing updating user achievements
    achv = {}
    achv['achievement'] = "Top 10 player in UEA League"
    rv5 = make_request(url="/api/v1/user/" + accountId + "/achievements", method="POST", data=achv)
    check_content_type(rv5.headers)
    res5 = json.loads(rv5.data)
    eq_(rv5.status_code, 201)
    eq_(res5["success"], "achievement has been added successfully")

    # testing updating fake user achievements
    rv5 = make_request(url="/api/v1/user/G87NXEW/achievements", method="POST", data={})
    check_content_type(rv5.headers)
    res5 = json.loads(rv5.data)
    eq_(rv5.status_code, 404)
    eq_(res5["error"], "user not found")

    # testing retreiving user achievements
    rv5 = make_request("/api/v1/user/" + accountId + "/achievements", method="GET")
    check_content_type(rv5.headers)
    res5 = json.loads(rv5.data)
    eq_(rv5.status_code, 200)
    eq_(res5["achievements"]['0']["achievment"], achv["achievement"])










