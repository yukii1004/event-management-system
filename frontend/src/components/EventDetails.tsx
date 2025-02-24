"use client"

import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const EventDetails = () => {
  const { id } = useParams()
  const [event, setEvent] = useState(null)
  const [isRegistered, setIsRegistered] = useState(false)

  useEffect(() => {
    // TODO: Fetch event details from backend
    // setEvent(fetchedEvent);
    // TODO: Check if user is registered for the event
    // setIsRegistered(checkRegistrationStatus);
  }, [])

  const handleRegister = () => {
    // TODO: Send registration request to backend
    // TODO: Handle payment for paid events
    // TODO: Update registration status
  }

  if (!event) return <div>Loading...</div>

  return (
    <div className="p-6">
      <Card>
        <CardHeader>
          <CardTitle>{event.title}</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{event.description}</p>
          <p>Date: {event.date}</p>
          <p>Time: {event.time}</p>
          <p>Venue: {event.venue}</p>
          <p>Capacity: {event.capacity}</p>
          {event.isPaid && <p>Price: ${event.price}</p>}
          {!isRegistered ? (
            <Button onClick={handleRegister}>Register</Button>
          ) : (
            <p>You are registered for this event</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default EventDetails

