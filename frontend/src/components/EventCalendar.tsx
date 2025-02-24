"use client"

import { useState, useEffect } from "react"
import { Calendar } from "@/components/ui/calendar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const EventCalendar = () => {
  const [events, setEvents] = useState([])
  const [selectedBatch, setSelectedBatch] = useState("")
  const [freeSlots, setFreeSlots] = useState([])

  useEffect(() => {
    // TODO: Fetch events from backend
    // setEvents(fetchedEvents);
    // TODO: Fetch free slots for selected batch from backend
    // setFreeSlots(fetchedFreeSlots);
  }, [selectedBatch])

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Event Calendar</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Events</CardTitle>
          </CardHeader>
          <CardContent>
            <Calendar
              mode="multiple"
              selected={events.map((event) => new Date(event.date))}
              // TODO: Handle date selection and show event details
            />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Free Slots</CardTitle>
          </CardHeader>
          <CardContent>
            <Select onValueChange={setSelectedBatch}>
              <SelectTrigger>
                <SelectValue placeholder="Select batch" />
              </SelectTrigger>
              <SelectContent>
                {/* TODO: Populate with actual batch options */}
                <SelectItem value="batch1">Batch 1</SelectItem>
                <SelectItem value="batch2">Batch 2</SelectItem>
              </SelectContent>
            </Select>
            {/* TODO: Display free slots for selected batch */}
            <ul>
              {freeSlots.map((slot, index) => (
                <li key={index}>{/* Slot details */}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default EventCalendar

