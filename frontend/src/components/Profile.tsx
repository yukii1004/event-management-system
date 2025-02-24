"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const Profile = () => {
  const [user, setUser] = useState(null)
  const [registeredEvents, setRegisteredEvents] = useState([])

  useEffect(() => {
    // TODO: Fetch user profile from backend
    // setUser(fetchedUser);
    // TODO: Fetch registered events from backend
    // setRegisteredEvents(fetchedEvents);
  }, [])

  if (!user) return <div>Loading...</div>

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Profile</h1>
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>{user.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Email: {user.email}</p>
          <p>Role: {user.role}</p>
          {user.role === "student" && <p>Batch: {user.batch}</p>}
          {user.role === "club" && <p>Club: {user.clubName}</p>}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Registered Events</CardTitle>
        </CardHeader>
        <CardContent>
          {registeredEvents.map((event, index) => (
            <div key={index} className="mb-2">
              <p>{event.title}</p>
              <p>Date: {event.date}</p>
              <Button variant="outline" size="sm">
                View Details
              </Button>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}

export default Profile

