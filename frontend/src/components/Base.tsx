import React from 'react'
import { Link } from "react-router-dom"
import { CgProfile } from "react-icons/cg";

const Base = ({ children }: { children: React.ReactNode }) => {
  // TODO: Fetch user role from backend or context
  const userRole = "admin"; // Placeholder, replace with actual user role

  return (
    <div className="flex flex-col h-[100vh] w-full">
      <nav className="flex items-center justify-between h-16 w-full bg-black text-white">
        <div className="flex justify-center items-center h-full w-[10%] p-4">
          <img src="/snuc.png" alt="Logo" />
        </div>
        <div className="flex text-xl items-center justify-evenly h-full w-[80%]">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/calendar">Calendar</Link>
          {userRole === "club" && <Link to="/create-event">Create Event</Link>}
          {userRole === "admin" && <Link to="/admin">Admin Panel</Link>}
          <Link to="/leaderboard">Leaderboard</Link>
        </div>
        <div className="flex justify-center items-center h-full w-[10%] p-4">
          <Link to="/profile"><CgProfile className='h-12 w-12'/></Link>
        </div>
      </nav>
      <div className="flex items-center justify-center p-4 h-[calc(100vh-8rem)] w-full">
        {children}
      </div>
      <footer className="flex items-center justify-between p-4 h-16 w-full bg-black text-white">
        <a
          href="https://github.com/yukii1004/SnucHack"
          target="_blank"
          className="font-bold text-2xl bg-gradient-to-r from-violet-600 via-green-600 to-red-500 bg-clip-text text-transparent"
        >
          Harbingers
        </a>
        <p>
          Made with ❤️ by Team{" "}
          <a
            href="https://www.linkedin.com/in/b-aditya20/"
            target="_blank"
            className="text-blue-500 active:text-blue-800 visited:text-purple-500 font-semibold"
          >
            Daddy B
          </a>
        </p>
      </footer>
    </div>
  );
};

export default Base;