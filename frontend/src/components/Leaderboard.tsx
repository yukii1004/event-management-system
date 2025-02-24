"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const LeaderBoard = () => {
  const [clubStats, setClubStats] = useState([])

  useEffect(() => {
    // TODO: Fetch club statistics from backend
    // setClubStats(fetchedClubStats);
  }, [])

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Club Leaderboard</h1>
      <Card>
        <CardHeader>
          <CardTitle>Club Performance (Last 6 Months)</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Rank</TableHead>
                <TableHead>Club Name</TableHead>
                <TableHead>Events Conducted</TableHead>
                <TableHead>Average Rating</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {clubStats.map((club, index) => (
                <TableRow key={index}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{club.name}</TableCell>
                  <TableCell>{club.eventsConducted}</TableCell>
                  <TableCell>{club.averageRating.toFixed(2)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

export default LeaderBoard