"""
    1. Meeting System - Google calendar System
    2. Add meeting
    3. Update meeting
    3. Delete meeting
    4. If overlap - Dont create a meeting
    5. Get all events - Date range
    6. Get an event - event ID

    1. Book an event
        1.1 Time range [ start time, end time]
        1.2 Invite meeting guests
        1.3 Description
        1.4 Meeting link
        1.5 Title
    2. Set reminder - TODO
    3. Notification - TODO

"""

import collections
from datetime import datetime

class User:
    def __init__(self, name, email):
        self.name = name 
        self.email = email 

    def getName(self):
        return self.name 

    def getEmailAddress(self):
        return self.email
    
class Meeting:

    def __init__(self, id, summary, start_time, end_time, users):
        self.id = id
        self.summary = summary
        self.start_time = start_time
        self.end_time = end_time
        self.users = users

    def getSummary(self): 
        return self.summary
    
    def getStartTime(self):
        return self.start_time
    
    def getEndTime(self):
        return self.end_time
    
    def getUsers(self):
        return self.users
    
    def __repr__(self):
        return f'{self.summary} - {self.start_time}, {self.end_time} - {self.users}'
    
class MeetingSystem:

    def __init__(self):
        self.users = collections.defaultdict()
        self.users_meeting = collections.defaultdict(list) # key: user_id, value: list of meetings -> set
        self.meetings = collections.defaultdict()
        self.id_count = 1

    def addUsers(self, name, email):
        if self.meetings.get(email, None) == None:
            self.users[email] = User(name, email)
            print("User is added to the system.")
            return
        else:
            print("User is already existing in the system.")
            return

    def createMeeting(self, summary, start_time, end_time, users):
        print("Function to create a meeting - ", summary)
        start_time = datetime.strptime(start_time, '%b %d %Y %I:%M %p')
        end_time = datetime.strptime(end_time, '%b %d %Y %I:%M %p')
        for email in users:
            if self.users.get(email, None) == None:
                print("Invalid user!")
                return

            for mid, mst in self.users_meeting[email]:
                meeting = self.meetings[mid]
                if  (meeting.start_time <= start_time <= meeting.end_time): # and (meeting.start_time <= end_time <= meeting.end_time):
                    print( "Meeting overlap")
                    return
        
        meeting = Meeting(self.id_count, summary, start_time, end_time, users)
        for email in users:
            self.users_meeting[email].append((meeting.id, meeting.start_time))
        self.meetings[meeting.id] = meeting
        self.id_count += 1
        return meeting
    
    def updateMeeting(self, mid, summary, start_time, end_time, users):
        print("Function to update the meeting with the meeting - ",mid)

        if self.meetings.get(mid, None) == None:
            print("Invalid meeting!")
            return

        meeting = self.meetings[mid]
        if summary:
            meeting.summary = summary
        if start_time:
            start_time = datetime.strptime(start_time, '%b %d %Y %I:%M %p')
            meeting.start_time = start_time
        if end_time:
            end_time = datetime.strptime(end_time, '%b %d %Y %I:%M %p')
            meeting.end_time = end_time
        if users:
            for email in users:
                for index, value in enumerate(self.users_meeting[email]):
                    mid, mst = value
                    user_meeting = self.meetings[mid]
                    if (user_meeting.id != meeting.id) and (user_meeting.start_time <= start_time <= user_meeting.end_time): # and (meeting.start_time <= end_time <= meeting.end_time):
                        print("Meeting overlap")
                        return
                    if meeting.id == user_meeting.id:
                        self.users_meeting[email].pop(index)
                        self.users_meeting[email].append((meeting.id,  meeting.start_time))
        self.meetings[meeting.id] = meeting
        return meeting

    def getMeeting(self, mid):
        if self.meetings.get(mid, None) == None:
            print("Invalid meeting ID.")
            return
        return self.meetings[mid]

    def deleteMeeting(self, mid):
        print("Function to delete the meeting - ", mid)

        if self.meetings.get(mid, None) == None:
            print("Invalid meeting.")
            return
        meeting = self.meetings[mid]
        for email in meeting.users:
            for index, value in enumerate(self.users_meeting[email]):
                m_id, start_time = value
                if mid == meeting.id:
                    self.users_meeting[email].pop(index)
        del self.meetings[mid]
        print("Deleted the meeting!")
        return


    def getAllMeetings(self, email, start_time = "", end_time = ""):
        print("Function to get all meetings for the user -", email)
        if self.users_meeting.get(email, None) == None:
            return "No meeting is found!"
        
        self.users_meeting[email].sort(key = lambda x: x[1])
        if start_time == "":
            return self.users_meeting[email]
        
        # print("Within the time range: ", start_time, end_time)
        #TODO: Based on start time and end time
    
    def displayUsers(self):
        return self.users



if __name__ == "__main__":
    ms = MeetingSystem()
    ms.addUsers("Sneha", "Sneha@gmail.com")
    ms.addUsers("Kiran", "Kiran@gmail.com")
    ms.addUsers("Ravi", "Ravi@gmail.com")
    ms.createMeeting("1 on 1", "Apr 12 2024 9:00 PM", "Apr 12 2024 10:00 PM", ["Sneha@gmail.com", "Kiran@gmail.com"])
    ms.createMeeting("Team meetup", "Apr 10 2024 10:30 AM", "Apr 10 2024 11:00 AM", ["Kiran@gmail.com", "Ravi@gmail.com"])
    meeting = ms.createMeeting("General Discussion", "Apr 11 2024 11:30 AM", "Apr 11 2024 11:30 AM", ["Sneha@gmail.com", "Kiran@gmail.com"])
    ms.updateMeeting(meeting.id, "General Discussion", "Apr 13 2024 5:00 PM", "Apr 13 2024 5:30 PM",["Sneha@gmail.com", "Kiran@gmail.com"])
    print(ms.getAllMeetings("Sneha@gmail.com"))
    ms.deleteMeeting(meeting.id)
    print(ms.getAllMeetings("Kiran@gmail.com"))
    print(ms.getAllMeetings("Ravi@gmail.com"))