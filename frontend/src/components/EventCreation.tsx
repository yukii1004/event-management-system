"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"

const EventCreation = () => {
  const [eventDetails, setEventDetails] = useState({
    title: "",
    description: "",
    date: "",
    time: "",
    venue: "",
    capacity: "",
    isPaid: false,
    price: "",
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: Send event details to backend for creation
    // TODO: Handle venue allocation and conflicts
    // TODO: Set up Razorpay integration for paid events
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Create Event</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          placeholder="Event Title"
          value={eventDetails.title}
          onChange={(e) => setEventDetails({ ...eventDetails, title: e.target.value })}
        />
        <Textarea
          placeholder="Event Description"
          value={eventDetails.description}
          onChange={(e) => setEventDetails({ ...eventDetails, description: e.target.value })}
        />
        <Input
          type="date"
          value={eventDetails.date}
          onChange={(e) => setEventDetails({ ...eventDetails, date: e.target.value })}
        />
        <Input
          type="time"
          value={eventDetails.time}
          onChange={(e) => setEventDetails({ ...eventDetails, time: e.target.value })}
        />
        <Select onValueChange={(value) => setEventDetails({ ...eventDetails, venue: value })}>
          <SelectTrigger>
            <SelectValue placeholder="Select venue" />
          </SelectTrigger>
          <SelectContent>
            {/* TODO: Populate with actual venue options */}
            <SelectItem value="venue1">Venue 1</SelectItem>
            <SelectItem value="venue2">Venue 2</SelectItem>
          </SelectContent>
        </Select>
        <Input
          type="number"
          placeholder="Capacity"
          value={eventDetails.capacity}
          onChange={(e) => setEventDetails({ ...eventDetails, capacity: e.target.value })}
        />
        <div className="flex items-center space-x-2">
          <Switch
            checked={eventDetails.isPaid}
            onCheckedChange={(checked) => setEventDetails({ ...eventDetails, isPaid: checked })}
          />
          <span>Paid Event</span>
        </div>
        {eventDetails.isPaid && (
          <Input
            type="number"
            placeholder="Price"
            value={eventDetails.price}
            onChange={(e) => setEventDetails({ ...eventDetails, price: e.target.value })}
          />
        )}
        <Button type="submit">Create Event</Button>
      </form>
    </div>
  )
}

export default EventCreation

