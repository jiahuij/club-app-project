from flask import Flask, request, Response
from json import dumps, loads
from mysql_run import *
import datetime

app = Flask(__name__)

#--/api/user--
@app.route('/api/user', methods=['POST'])
def user():
    resp = {}
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: user_id , return first_name, last_name, email, password, profile_pic

            if json_data.get("method") == "GET":

                if ("user_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    #SQL SELECT user_id --> first_name, last_name, email, password, profile_pic
                    userGET = getUser(user_id)
                    print(userGET)
                    if userGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif userGET == None:
                        resp = {"err": "User not found in database"}
                        status = 204
                    else:
                        first_name = userGET["first_name"]
                        last_name = userGET["last_name"]
                        email = userGET["email"]
                        password = userGET["password"]
                        resp = {"request_type":"GET", "first_name":f"{first_name}", "last_name":f"{last_name}", "email":f"{email}", "password":f"{password}"}
                        status = 200

            #--POST--
            # @json: {first_name, last_name, email, password}

            elif json_data.get("method") == "POST":

                if ("first_name" or "last_name" or "email" or "password") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    first_name = json_data.get("first_name")
                    last_name = json_data.get("last_name")
                    email = json_data.get("email")
                    password = json_data.get("password")
                    #SQL INSERT first_name, last_name, email, password
                    userPOST= postUser(first_name, last_name, email, password)
                    print(userPOST)
                    #If Database returned an error
                    if userPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        user_id = userPOST["user_id"]
                        resp = {"request_type":"POST","message":f"User {user_id} Successfully Created","user_id":f"{user_id}"}
                        status = 200

            #--PUT--
            # @json: {user_id, first_name, last_name, email, password} , returns: {first_name, last_name, email, password}

            elif json_data.get("method") == "PUT":

                if ("user_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    first_name = json_data.get("first_name")
                    last_name = json_data.get("last_name")
                    email = json_data.get("email")
                    password = json_data.get("password")
                    #SQL UPDATE first_name, last_name, email, password on user_id
                    userPUT = putUser(first_name, last_name, email, password, user_id)
                    if userPUT == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"PUT","message":f"User {user_id} Successfully Updated","user_id":f"{user_id}"}
                        status = 200

            #--DELETE--
            # @json: user_id

            elif json_data.get("method") == "DELETE":
                if ("user_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    #SQL DELETE USER on user_id
                    userDEL = deleteUser(user_id)
                    print(userDEL)
                    #If Database returned an error
                    if userDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"User {user_id} Successfully Deleted","user_id":f"{user_id}"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/user--

#--/api/user/membership--
@app.route('/api/user/membership', methods=['POST'])
def membership():
    resp = {}
    cnt = 0
    status = 404

    group_id = []

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            if json_data.get("method") == "GET":

                if ("user_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    #SQL SELECT user_id --> group_id[]
                    membershipGET = getMembership(user_id)
                    if membershipGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif membershipGET == None:
                        resp = {"err": "Membership not found in Database"}
                        status = 204
                    else:
                        resp = {"request_type":"GET"}
                        for membership in membershipGET:
                            cnt += 1
                            resp[f"membership{cnt}"] = {}
                            resp[f"membership{cnt}"]["name"] = membership["GroupName"]
                            resp[f"membership{cnt}"]["leader_id"] = membership["LeaderID"]
                            resp[f"membership{cnt}"]["color"] = membership["GroupColor"]
                            resp[f"membership{cnt}"]["description"] = membership["GroupDescription"]
                        resp["count"] = str(cnt)
                        status = 200

            #--POST--
            elif json_data.get("method") == "POST":

                if ("user_id" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    group_id = json_data.get("group_id")
                    #SQL INSERT user_id, group_id in membership
                    membershipPOST = postMembership(user_id, group_id)
                    print(membershipPOST)
                    if membershipPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        member_id = membershipPOST["memberID"]
                        resp = {"request_type":"POST", "message":f"Membership created of User {user_id} in Group {group_id}", "member_id":f"{member_id}"}
                        status = 200

            #--PUT--
            elif json_data.get("method") == "PUT":

                if ("user_id" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    group_id = json_data.get("group_id")
                    privilege = json_data.get("privilege")
                    #SQL UPDATE privilege on user_id, group_id
                    membershipPUT = updateMembership(user_id, group_id, privilege)
                    print(membershipPUT)
                    if membershipPUT == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"PUT", "message":f"User {user_id} in Group {group_id} privileges updated"}
                        status = 200

            #--DELETE--
            elif json_data.get("method") == "DELETE":
                if ("user_id" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    group_id = json_data.get("group_id")
                    #SQL DELETE membership on user_id, group_id
                    membershipDEL = deleteMembership(user_id, group_id)
                    print(membershipDEL)
                    if membershipDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE", "message":f"User {user_id}\'s membership in Group {group_id} has been deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/user/membership--

#--/api/user/membership/privilege--
@app.route('/api/user/membership/privilege', methods=['POST'])
def privilege():
    resp = {}
    status = 404

    #--GET--
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:
            if json_data.get("method") == "GET":
                if ("user_id" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    group_id = json_data.get("group_id")
                    #SQL SELECT user_id, group_id --> return true or false or privilege level
                    privilegeGET = getMemberPrivilege(user_id, group_id)
                    print(privilegeGET)
                    if privilegeGET == -1:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif privilegeGET == None:
                        resp = {"err": "Membership not found in Database"}
                        status = 204
                    else:
                        privilege = privilegeGET["UserPrivileges"]
                        resp = {"request_type":"GET", "message":f"User {user_id} is a member of Group {group_id}", "privilege": f"{privilege}"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/user/membership/privilege--

#--/api/user/login--
@app.route('/api/user/login', methods=['POST'])
def login():
    resp = {}
    status = 404

    #--GET--
    # @json: {email, password} , returns user_id
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:
            if json_data.get("method") == "GET":
                if ("email" or "password") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    email = json_data.get("email")
                    password = json_data.get("password")
                    #SQL SELECT email, password --> user_id
                    loginGET = getLogin(email, password)
                    print(loginGET)
                    if loginGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif loginGET == None:
                        resp = {"err": "Credentials not found in Database"}
                        status = 204
                    else:
                        user_id = loginGET["user_id"]
                        resp = {"request_type":"GET", "message":f"User {user_id} Successfully Logged In", "user_id": f"{user_id}"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/user/login--

#--/api/group--
@app.route('/api/group', methods=['POST'])
def group():
    resp = {}
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: group_id , returns {name, description, color}

            if json_data.get("method") == "GET":
                if ("group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    group_id = json_data.get("group_id")
                    #SQL SELECT group_id --> name, description, color
                    groupGET = getGroup(group_id)
                    print(groupGET)
                    if groupGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif groupGET == None:
                        resp = {"err": "Group not found in Database"}
                        status = 204
                    else:
                        name = groupGET["name"]
                        description = groupGET["description"]
                        color = groupGET["color"]
                        leader_id = groupGET["leader_id"]
                        resp = {"request_type":"GET", "name": f"{name}", "description": f"{description}", "color": f"{color}", "leader_id": f"{leader_id}"}
                        status = 200

            #--POST--
            # @json: {user_id, name, description, color} , returns group_id

            elif json_data.get("method") == "POST":

                if ("user_id" or "name" or "description" or "color") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    leader_id = json_data.get("user_id")
                    name = json_data.get("name")
                    description = json_data.get("description")
                    color = json_data.get("color")
                    #SQL INSERT leader_id, name, description, color
                    groupPOST = postGroup(leader_id, name, description, color)
                    print(groupPOST)
                    if groupPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        group_id = groupPOST["GroupID"]
                        resp = {"request_type":"POST", "message": f"Group {group_id} Successfully Created", "group_id": f"{group_id}"}
                        status = 200

            #--PUT--
            # @json: {group_id, name, description, color}

            elif json_data.get("method") == "PUT":

                if ("group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    group_id = json_data.get("group_id")
                    name = json_data.get("name")
                    description = json_data.get("description")
                    color = json_data.get("color")
                    #SQL UPDATE name, description, color
                    groupPUT = putGroup(group_id, name, description, color)
                    if groupPUT == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"PUT","message":f"Group {group_id} Successfully Updated"}
                        status = 200

            #--DELETE--
            # @json: group_id

            elif json_data.get("method") == "DELETE":

                if ("group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    group_id = json_data.get("group_id")
                    #SQL DELETE GROUP on group_id
                    groupDEL = deleteGroup(group_id)
                    print(groupDEL)
                    if groupDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"Group {group_id} Successfully Deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/group--

#--/api/group/search--
@app.route('/api/group/search', methods=['POST'])
def group_search():
    resp = {}
    cnt = 0
    status = 404

    #--GET--
    # @json: leader_id, returns {user_id, group_id, group_name}
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        else:
            #SQL SELECT --> name, description, color, leader_id
            searchGET = searchGroup()
            if searchGET == 0:
                resp = {"err": "Database could not perform action"}
                status = 418
            elif searchGET == None:
                resp = {"err": "No group found in Database"}
                status = 204
            else:
                for group in searchGET:
                    cnt += 1
                    resp[f"group{cnt}"] = {}
                    resp[f"group{cnt}"]["leader_id"] = group["LeaderID"]
                    resp[f"group{cnt}"]["color"] = group["GroupColor"]
                    resp[f"group{cnt}"]["description"] = group["GroupDescription"]
                    resp[f"group{cnt}"]["name"] = group["GroupName"]

                resp["count"] = str(cnt)
                status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/group/search--

#--/api/group/request--
@app.route('/api/group/request', methods=['POST'])
def member_request():
    resp = {}
    cnt = 0
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: leader_id, returns {user_id, group_id, group_name}

            if json_data.get("method") == "GET":
                if ("user_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    leader_id = json_data.get("user_id")
                    #SQL SELECT leader_id --> user_id, group_id, group_name
                    requestGET = getRequest(leader_id)
                    print(requestGET)
                    if requestGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif requestGET == None:
                        resp = {"err": "Request not found in Database"}
                        status = 204
                    else:
                        resp = {"request_type":"GET"}
                        for req in requestGET:
                            cnt += 1
                            resp[f"request{cnt}"] = {}
                            resp[f"request{cnt}"]["request_id"] = req["RequestID"]
                            resp[f"request{cnt}"]["user_id"] = req["UserID"]
                            resp[f"request{cnt}"]["group_id"] = req["GroupID"]
                            resp[f"request{cnt}"]["group_name"] = req["GroupName"]
                        status = 200

            #--POST--
            # @json: {user_id, group_id}

            elif json_data.get("method") == "POST":

                if ("user_id" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    group_id = json_data.get("group_id")
                    #SQL insert group_id, user_id, group_name
                    requestPOST = postRequest(user_id, group_id)
                    print(requestPOST)
                    if requestPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        request_id = requestPOST["RequestID"]
                        resp = {"request_type":"POST", "message":"Successfully created Request", "request_id":f"{request_id}"}
                        status = 200

            #--DELETE--
            # @json: {user_id, group_id}

            elif json_data.get("method") == "DELETE":

                if ("user_id" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    group_id = json_data.get("group_id")
                    #SQL delete on user_id, group_id
                    requestDEL = deleteRequest(user_id, group_id)
                    if requestDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE", "message":"Successfully deleted Request"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/group/request--

#--/api/event--
@app.route('/api/event', methods=['POST'])
def event():
    resp = {}
    status = 404

    #--GET--
    # @json: event_id , returns {DateAndTime, eventName, LeaderID, Location, Description, GroupID}
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: event_id , returns {DateAndTime, eventName, LeaderID, Location, Description, GroupID}

            if json_data.get("method") == "GET":

                if ("event_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    event_id = json_data.get("event_id")
                    #SQL SELECT event_id --> DateAndTime, eventName, LeaderID, Location, Description, GroupID
                    eventGET = getEvent(event_id)
                    print(eventGET)
                    if eventGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif eventGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        date_time = eventGET["DateAndTime"]
                        name = eventGET["eventName"]
                        leader_id = eventGET["LeaderID"]
                        location = eventGET["Location"]
                        description = eventGET["Description"]
                        group_id = eventGET["GroupID"]
                        resp = {"request_type":"GET", "date_time": f"{date_time}", "name": f"{name}", "leader_id": f"{leader_id}", "location": f"{location}", "description": f"{description}", "group_id": f"{group_id}"}
                        status = 200

            #--POST--
            # @json: {event_name, event_DateAndTime, leader_id, location, description, group_id} , returns event_id

            elif json_data.get("method") == "POST":

                if ("name" or "leader_id" or "location" or "description" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    name = json_data.get("name")
                    date_time = json_data.get("date_time")
                    leader_id = json_data.get("leader_id")
                    location = json_data.get("location")
                    description = json_data.get("description")
                    group_id = json_data.get("group_id")
                    #SQL INSERT event_name, event_DateAndTime, leader_id, location, description, group_id
                    eventPOST = postEvent(name, date_time, leader_id, location, description, group_id)
                    print(eventPOST)
                    if eventPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        event_id = eventPOST["EventID"]
                        resp = {"request_type":"POST", "message": f"Event {event_id} Successfully Created", "event_id": f"{event_id}"}
                        status = 200

            #--PUT--
            # @json: {group_id, name, description, color}

            elif json_data.get("method") == "PUT":

                if ("event_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    event_id = json_data.get("event_id")
                    date_time = json_data.get("date_time")
                    name = json_data.get("name")
                    leader_id = json_data.get("leader_id")
                    description = json_data.get("description")
                    location = json_data.get("location")
                    group_id = json_data.get("group_id")
                    #SQL UPDATE name, description, location
                    eventPUT = putEvent(event_id, date_time, name, leader_id, location, description, group_id)
                    if eventPUT == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"PUT","message":f"Event {event_id} Successfully Updated"}
                        status = 200

            #--DELETE--
            # @json: event_id

            elif json_data.get("method") == "DELETE":

                if ("event_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    event_id = json_data.get("event_id")
                    #SQL DELETE EVENT on event_id
                    eventDEL = deleteEvent(event_id)
                    print(eventDEL)
                    if eventDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"Event {event_id} Successfully Deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/event--

#--/api/announcement--
@app.route('/api/announcement', methods=['POST'])
def announcement():
    resp = {}
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: announcement_id , returns {UserID, DateAndTime, Content, GroupID}

            if json_data.get("method") == "GET":

                if ("announcement_id") not in json_data:
                        resp = {"err": "Missing required fields"}
                        status = 400
                else:
                    announcement_id = json_data.get("announcement_id")
                    #SQL SELECT announcement_id -> user_id, date_time, content, group_id
                    announcementGET = getAnnouncement(announcement_id)
                    print(announcementGET)
                    if announcementGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif announcementGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        user_id = announcementGET["LeaderID"]
                        date_time = announcementGET["DateAndTime"]
                        content = announcementGET["content"]
                        group_id = announcementGET["GroupID"]
                        resp = {"request_type":"GET", "user_id": f"{user_id}", "date_time": f"{date_time}", "content": f"{content}", "group_id": f"{group_id}"}
                        status = 200

            #--POST--
            # @json: {user_id, content, group_id}

            elif json_data.get("method") == "POST":

                if ("user_id" or "content" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    content = json_data.get("content")
                    group_id = json_data.get("group_id")
                    #SQL INSERT user_id, content_id, content, group_id
                    announcementPOST = postAnnouncement(user_id, content, group_id)
                    print(announcementPOST)
                    if announcementPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        announcement_id = announcementPOST["AnnouncementID"]
                        resp = {"request_type":"POST", "message": f"Announcement {announcement_id} Successfully Created", "announcement_id": f"{announcement_id}"}
                        status = 200

            #--PUT--
            # @json: {leader_id, content, group_id, announcement_id}

            elif json_data.get("method") == "PUT":

                if ("announcement_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    announcement_id = json_data.get("announcement_id")
                    leader_id = json_data.get("leader_id")
                    content = json_data.get("content")
                    group_id = json_data.get("group_id")
                    #SQL UPDATE leader_id, content, group_id, announcement_id
                    announcementPUT = putAnnouncement(leader_id, content, group_id, announcement_id)
                    if announcementPUT == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"PUT","message":f"Announcement {announcement_id} Successfully Updated"}
                        status = 200

            #--DELETE--
            # @json: event_id

            elif json_data.get("method") == "DELETE":

                if ("announcement_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    announcement_id = json_data.get("announcement_id")
                    #SQL DELETE Announcement on announcement_id
                    announcementDEL = deleteAnnouncement(announcement_id)
                    print(announcementDEL)
                    if announcementDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"Announcement {announcement_id} Successfully Deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/announcement--

#--/api/announcement/search--
@app.route('/api/announcement/search', methods=['POST'])
def announcementSearch():
    resp = {}
    cnt = 0
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: group_id , returns {UserID, DateAndTime, Content, GroupID}

            if json_data.get("method") == "GET":

                if ("group_id") not in json_data:
                        resp = {"err": "Missing required fields"}
                        status = 400
                else:
                    group_id = json_data.get("group_id")
                    #SQL SELECT announcement_id -> user_id, date_time, content, group_id
                    announcementSearchGET = getAllAnnouncements(group_id)
                    print(announcementSearchGET)
                    if announcementSearchGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif announcementSearchGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        resp = {"request_type":"GET"}
                        for announcement in announcementSearchGET:
                            cnt += 1
                            resp[f"announcement{cnt}"] = {}
                            resp[f"announcement{cnt}"]["leader_id"] = announcement["LeaderID"]
                            resp[f"announcement{cnt}"]["content"] = announcement["content"]
                            resp[f"announcement{cnt}"]["date_time"] = announcement["DateAndTime"].strftime("%m/%d/%Y %H:%M:%S")

                        resp["count"] = str(cnt)
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/announcement/search--

#--/api/comment--
@app.route('/api/comment', methods=['POST'])
def comment():
    resp = {}
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: comment_id , returns {UserID, AnnouncementID, Content}

            if json_data.get("method") == "GET":

                if ("comment_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    comment_id = json_data.get("comment_id")
                    #SQL SELECT comment_id -> user_id, date_time, content, group_id
                    commentGET = getComment(comment_id)
                    print(commentGET)
                    if commentGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif commentGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        user_id = commentGET["MemberID"]
                        date_time = commentGET["DateAndTime"]
                        announcement_id = commentGET["announcementID"]
                        content = commentGET["content"]
                        resp = {"request_type":"GET", "user_id": f"{user_id}", "date_time": f"{date_time}", "announcement_id": f"{announcement_id}", "content": f"{content}"}
                        status = 200

            #--POST--
            # @json: {user_id, announcement_id, content}

            elif json_data.get("method") == "POST":

                if ("user_id" or "content" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    user_id = json_data.get("user_id")
                    announcement_id = json_data.get("announcement_id")
                    content = json_data.get("content")
                    #SQL INSERT user_id, content_id, content, group_id
                    commentPOST = postComment(user_id, announcement_id, content)
                    print(commentPOST)
                    if commentPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        comment_id = commentPOST["commentID"]
                        resp = {"request_type":"POST", "message": f"Comment {comment_id} Successfully Created", "comment_id": f"{comment_id}"}
                        status = 200

            #--PUT--
            # @json: {content, announcement_id, comment_id}

            elif json_data.get("method") == "PUT":

                if ("comment_id" or "content") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    comment_id = json_data.get("comment_id")
                    announcement_id = json_data.get("announcement_id")
                    content = json_data.get("content")
                    #SQL UPDATE comment_id, announcement_id, content
                    commentPUT = putComment(content, announcement_id, comment_id)
                    if commentPUT == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"PUT","message":f"Comment {comment_id} Successfully Updated"}
                        status = 200

            #--DELETE--
            # @json: event_id

            elif json_data.get("method") == "DELETE":

                if ("comment_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    comment_id = json_data.get("comment_id")
                    #SQL DELETE Comment on comment_id
                    commentDEL = deleteComment(comment_id)
                    print(commentDEL)
                    if commentDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"Comment {comment_id} Successfully Deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/comment--

#--/api/poll--
@app.route('/api/poll', methods=['POST'])
def poll():
    resp = {}
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: poll_id , returns {LeaderID, pollQuestion, pollResponseOptions, pollDescription, group_id}

            if json_data.get("method") == "GET":

                if ("poll_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    poll_id = json_data.get("poll_id")
                    #SQL SELECT poll_id -> leader_id, poll_question, poll_response_options[], poll_description, group_id
                    pollGET = getPoll(poll_id)
                    print(pollGET)
                    if pollGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif pollGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        leader_id = pollGET["LeaderID"]
                        poll_question = pollGET["question"]
                        poll_response_options = pollGET["ResponseOptions"]
                        poll_description = pollGET["PollDescription"]
                        date_time = pollGET["DateAndTime"]
                        resp = {"request_type":"GET", "leader_id": f"{leader_id}", "poll_question": f"{poll_question}", "poll_response_options": f"{poll_response_options}", "poll_description": f"{poll_description}", "date_time": f"{date_time}"}
                        status = 200

            #--POST--
            # @json: {user_id, announcement_id, content}

            elif json_data.get("method") == "POST":

                if ("user_id" or "poll_question" or "poll_response_options" or "poll_description" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    leader_id = json_data.get("user_id")
                    poll_question = json_data.get("poll_question")
                    poll_response_options = json_data.get("poll_response_options")
                    poll_description = json_data.get("poll_description")
                    group_id = json_data.get("group_id")
                    #SQL INSERT leader_id, poll_question, poll_response_options, poll_description, group_id
                    pollPOST = postPoll(leader_id, poll_question, poll_response_options, poll_description, group_id)
                    print(pollPOST)
                    if pollPOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        poll_id = pollPOST["PollID"]
                        resp = {"request_type":"POST", "message": f"Poll {poll_id} Successfully Created", "poll_id": f"{poll_id}"}
                        status = 200

            #--DELETE--
            # @json: event_id

            elif json_data.get("method") == "DELETE":

                if ("poll_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    poll_id = json_data.get("poll_id")
                    #SQL DELETE Poll on poll_id
                    pollDEL = deletePoll(poll_id)
                    print(pollDEL)
                    if pollDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"Poll {poll_id} Successfully Deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/poll--

#--/api/poll/search--
@app.route('/api/poll/search', methods=['POST'])
def pollSearch():
    resp = {}
    cnt = 0
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: group_id , returns {LeaderID, pollQuestion, pollResponseOptions, pollDescription, group_id}

            if json_data.get("method") == "GET":

                if ("group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    group_id = json_data.get("group_id")
                    #SQL SELECT group_id -> leader_id, poll_question, poll_response_options[], poll_description, group_id
                    pollSearchGET = getAllPolls(group_id)
                    print(pollSearchGET)
                    if pollSearchGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif pollSearchGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        resp = {"request_type":"GET"}
                        for poll in pollSearchGET:
                            cnt += 1
                            resp[f"poll{cnt}"] = {}
                            resp[f"poll{cnt}"]["leader_id"] = poll["LeaderID"]
                            resp[f"poll{cnt}"]["question"] = poll["question"]
                            resp[f"poll{cnt}"]["poll_response_options"] = poll["ResponseOptions"]
                            resp[f"poll{cnt}"]["poll_description"] = poll["PollDescription"]
                            resp[f"poll{cnt}"]["date_time"] = poll["DateAndTime"].strftime("%m/%d/%Y %H:%M:%S")

                        resp["count"] = str(cnt)
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/poll/search--

#--/api/poll/response--
@app.route('/api/poll/response', methods=['POST'])
def poll_response():
    resp = {}
    status = 404

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            resp = {"err": "No data provided"}
            status = 400
        elif ("method") not in json_data:
            resp = {"err": "Missing required fields"}
            status = 400
        else:

            #--GET--
            # @json: poll_id , returns {MemberID, userResponse, groupID}

            if json_data.get("method") == "GET":

                if ("poll_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    poll_id = json_data.get("poll_id")
                    #SQL SELECT poll_id -> [member_id, userResponse, group_id, poll_response_id]
                    pollResponseGET = getPollResponse(poll_id)
                    print(pollResponseGET)
                    if pollResponseGET == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    elif pollResponseGET == None:
                        resp = {"err": "Event not found in Database"}
                        status = 204
                    else:
                        resp = {"request_type":"GET"}
                        for response in pollResponseGET:
                            cnt += 1
                            resp[f"response{cnt}"] = {}
                            resp[f"response{cnt}"]["user_id"] = response["MemberID"]
                            resp[f"response{cnt}"]["response"] = req["userResponse"]
                            resp[f"response{cnt}"]["date_time"] = req["DateAndTime"]
                        status = 200

            #--POST--
            # @json: {user_id, announcement_id, content}

            elif json_data.get("method") == "POST":

                if ("user_id" or "poll_question" or "poll_response_options" or "poll_description" or "group_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    member_id = json_data.get("user_id")
                    response = json_data.get("response")
                    group_id = json_data.get("group_id")
                    poll_id = json_data.get("poll_id")
                    #SQL INSERT member_id, response, group_id, poll_id
                    pollResponsePOST = postPollResponse(member_id, response, group_id, poll_id)
                    print(pollResponsePOST)
                    if pollResponsePOST == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        poll_response_id = pollResponsePOST["ReponseID"]
                        resp = {"request_type":"POST", "message": f"Poll Response {poll_response_id} Successfully Created", "poll_response_id": f"{poll_response_id}"}
                        status = 200

            #--DELETE--
            # @json: event_id

            elif json_data.get("method") == "DELETE":

                if ("poll_response_id") not in json_data:
                    resp = {"err": "Missing required fields"}
                    status = 400
                else:
                    poll_response_id = json_data.get("poll_response_id")
                    #SQL DELETE Poll Response on poll_response_id
                    pollResponseDEL = deletePollResponse(poll_response_id)
                    print(pollResponseDEL)
                    if pollResponseDEL == 0:
                        resp = {"err": "Database could not perform action"}
                        status = 418
                    else:
                        resp = {"request_type":"DELETE","message":f"Poll Response {poll_response_id} Successfully Deleted"}
                        status = 200

    return Response(dumps(resp),status=status,mimetype='application/json')
#END OF --/api/poll/response--

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

###------------###
### END OF FILE - if this is missing, the file is truncated ###
###------------###
