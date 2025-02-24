import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom"
import Base from "./components/Base"
import Dashboard from "./components/Dashboard"
import EventCalendar from "./components/EventCalendar"
import EventCreation from "./components/EventCreation"
import EventDetails from "./components/EventDetails"
import Profile from "./components/Profile"
import LeaderBoard from "./components/Leaderboard"
import AdminPanel from "./components/AdminPanel"

function App() {
  return (
    <Router>
      <Base>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/calendar" element={<EventCalendar />} />
          <Route path="/create-event" element={<EventCreation />} />
          <Route path="/event/:id" element={<EventDetails />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/leaderboard" element={<LeaderBoard />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Base>
    </Router>
  )
}

export default App