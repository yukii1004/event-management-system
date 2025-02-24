"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const AdminPanel = () => {
  const [users, setUsers] = useState([])
  const [events, setEvents] = useState([])

  useEffect(() => {
    // TODO: Fetch users from backend
    // setUsers(fetchedUsers);
    // TODO: Fetch events from backend
    // setEvents(fetchedEvents);
  }, [])

  const handleUserAction = (userId, action) => {
    // TODO: Implement user actions (e.g., suspend, delete)
  }

  const handleEventAction = (eventId, action) => {
    // TODO: Implement event actions (e.g., cancel, reschedule)
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Panel</h1>
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>User Management</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.role}</TableCell>
                  <TableCell>
                    <Button size="sm" onClick={() => handleUserAction(user.id, "suspend")}>
                      Suspend
                    </Button>
                    <Button size="sm" variant="destructive" onClick={() => handleUserAction(user.id, "delete")}>
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Event Management</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Organizer</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {events.map((event) => (
                <TableRow key={event.id}>
                  <TableCell>{event.title}</TableCell>
                  <TableCell>{event.date}</TableCell>
                  <TableCell>{event.organizer}</TableCell>
                  <TableCell>
                    <Button size="sm" onClick={() => handleEventAction(event.id, "cancel")}>
                      Cancel
                    </Button>
                    <Button size="sm" onClick={() => handleEventAction(event.id, "reschedule")}>
                      Reschedule
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

export default AdminPanel

