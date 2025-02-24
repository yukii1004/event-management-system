"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Calendar, Users, Award, Bell } from "lucide-react"

const Dashboard = () => {
  const [userRole, setUserRole] = useState("")
  const [upcomingEvents, setUpcomingEvents] = useState([])
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    // TODO: Fetch user role from backend
    // setUserRole(fetchedUserRole);
    // TODO: Fetch upcoming events from backend
    // setUpcomingEvents(fetchedUpcomingEvents);
    // TODO: Fetch notifications from backend
    // setNotifications(fetchedNotifications);
  }, [])

  return (
    <div className="p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Calendar className="mr-2" />
              Upcoming Events
            </CardTitle>
          </CardHeader>
          <CardContent>
            {/* TODO: Display upcoming events */}
            <ul>
              {upcomingEvents.map((event, index) => (
                <li key={index}>{/* Event details */}</li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card className='h-full '>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Bell className="mr-2" />
              Notifications
            </CardTitle>
          </CardHeader>
          <CardContent>
            {/* TODO: Display notifications */}
            <ul>
              {notifications.map((notification, index) => (
                <li key={index}>{/* Notification details */}</li>
              ))}
            </ul>
          </CardContent>
        </Card>

        {userRole === "club" && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="mr-2" />
                Club Management
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Button>Create Event</Button>
              <Button>Manage Members</Button>
            </CardContent>
          </Card>
        )}

        {userRole === "admin" && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Award className="mr-2" />
                Admin Actions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Button>Manage Users</Button>
              <Button>System Settings</Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Dashboard

