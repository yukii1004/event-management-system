import datetime
import time
from typing import List, Optional

import sqlalchemy as db
from sqlalchemy import Column, ForeignKey, Table, create_engine, func
from sqlalchemy.orm import Session

from api.service.assets import unique_id


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # we make this a singleton class
        # we don't want two instances of the database class
        if Database._instance is None:
            Database._instance = object.__new__(cls)
            Database._instance.__init__(*args, **kwargs)
        return Database._instance

    def __init__(self, dbfile: str = "database.db"):
        # here we create the database, and the tables used.
        self.engine = create_engine(f"sqlite:///{dbfile}")
        self.engine.connect()
        self.meta = db.MetaData()

        self._events = Table(
            "events",
            self.meta,
            Column("event_id", db.Integer, unique=True, nullable=False, primary_key=True),
            Column("event_name", db.String, unique=True, nullable=False),
            Column("event_location", db.String),
            Column("categories", db.String),
            Column("start_time", db.Integer),
            Column("end_time", db.Integer),
            Column("limit", db.Integer),
            Column("price", db.Float),
            Column("on_duty", db.Boolean, default=False),
            Column("rating", db.Float),
            Column("club_id", db.Integer, ForeignKey("clubs.club_id")),
        )

        self._users = Table(
            "users",
            self.meta,
            Column("user_id", db.Integer, unique=True, nullable=False, primary_key=True),
            Column("username", db.String, unique=True, nullable=False),
            Column("user_type", db.Integer),
            Column("interests", db.String),
            Column("creation_time", db.DateTime),
        )

        self._venues = Table(
            "venues",
            self.meta,
            Column("venue_id", db.Integer, unique=True, nullable=False, primary_key=True),
            Column("venue_name", db.String, unique=True, nullable=False),
            Column("capacity", db.Integer),
        )

        self._clubs = Table(
            "clubs",
            self.meta,
            Column("club_id", db.Integer, ForeignKey("users.user_id"), unique=True, nullable=False, primary_key=True),
            Column("club_name", db.String, unique=True, nullable=False),
            Column("club_email", db.String),
            Column("upi_id", db.String),
        )

        self._registrations = Table(
            "registrations",
            self.meta,
            Column("registration_id", db.Integer, unique=True, nullable=False, primary_key=True),
            Column("user_id", db.Integer, ForeignKey("users.user_id")),
            Column("event_name", db.String),
            Column("event_id", db.Integer, ForeignKey("events.event_id")),
        )

        self._waitlist = Table(
            "waitlist",
            self.meta,
            Column("user_id", db.Integer, ForeignKey("users.user_id")),
            Column("event_id", db.Integer, ForeignKey("events.event_id")),
            Column("registration_timestamp", db.Integer),
            Column("registration_id", db.Integer, unique=True, nullable=False, primary_key=True),
        )

        self._pendinglist = Table(
            "pendinglist",
            self.meta,
            Column("user_id", db.Integer, ForeignKey("users.user_id")),
            Column("event_id", db.Integer, ForeignKey("events.event_id")),
            Column("registration_timestamp", db.Integer),
            Column("registration_id", db.Integer, unique=True, nullable=False, primary_key=True),
        )

        self.meta.create_all(self.engine)

        self.event_map = {}
        self.user_map = {}
        self.registration_map = {}

        self.populate_venues()

    def populate_venues(self):
        with Session(self.engine) as session:
            # Check if venues table is already populated
            if session.query(self._venues).count() == 0:
                # Static venue data
                venues = [
                    {"venue_name": "Main Auditorium", "capacity": 500},
                    {"venue_name": "Lecture Hall 1", "capacity": 100},
                    {"venue_name": "Lecture Hall 2", "capacity": 100},
                    {"venue_name": "Conference Room", "capacity": 50},
                ]

                # Insert venues into the table
                for venue in venues:
                    venue_id = unique_id()
                    insert_stmt = self._venues.insert().values(
                        venue_id=venue_id,
                        venue_name=venue["venue_name"],
                        capacity=venue["capacity"],
                    )
                    session.execute(insert_stmt)

                session.commit()

    def get_user_ids(self):
        with Session(self.engine) as session:
            command = self._users.select()
            result = session.execute(command)
            res = result.fetchall()
        # return the first element of each tuple, which is the user id
        return {x[0] for x in res}

    def get_usernames(self):
        with Session(self.engine) as session:
            command = self._users.select()
            result = session.execute(command)
            res = result.fetchall()
        # return the first element of each tuple, which is the user name
        return [x[1] for x in res]

    def add_user(self, username: str, user_type: int, interests: List[str]):
        existing_user = self.get_user(username=username)
        if existing_user:
            raise ValueError("Username already exists")
        str_interests = ",".join(interests)
        user_ids = self.get_user_ids()

        new_id = unique_id()

        while new_id in user_ids:
            new_id = unique_id()

        with Session(self.engine) as session:
            command = self._users.insert().values(
                user_id=new_id, username=username, user_type=user_type, interests=str_interests, creation_time=db.func.now()
            )
            session.execute(command)
            session.commit()
        return new_id

    def add_club(self, club_id: int, club_name: str, club_email: str = None, upi_id: str = None):
        with Session(self.engine) as session:
            command = self._clubs.insert().values(
                club_id=club_id,
                club_name=club_name,
                club_email=club_email,
                upi_id=upi_id,
            )
            session.execute(command)
            session.commit()

    def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None):
        with Session(self.engine) as session:
            if username:
                command = self._users.select().where(self._users.c.username == username)
            elif user_id:
                command = self._users.select().where(self._users.c.user_id == user_id)

            result = session.execute(command)
            res = result.fetchone()
            if not res:
                return {}

            ans = {
                "user_id": res[0],
                "username": res[1],
                "user_type": res[2],
                "interests": res[3].split(","),
            }
            return ans

    def search_event(
        self,
        club_id: int,
        event_id: Optional[int] = None,
        event_name: Optional[str] = None,
        event_location: Optional[str] = None,
        categories: Optional[list] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        limit: Optional[int] = None,
    ):
        with Session(self.engine) as session:
            command = self._events.select()

            if event_id:
                command = command.filter(self._events.c.event_id == event_id)
            if event_name:
                command = command.filter(self._events.c.event_name.like(f"%{event_name}%"))
            if event_location:
                command = command.filter(self._events.c.event_location == event_location)
            if start_time:
                command = command.filter(self._events.c.start_time >= start_time)
            if end_time:
                command = command.filter(self._events.c.end_time <= end_time)
            if categories:
                for category in categories:
                    command = command.filter(self._events.c.categories.like(f"%{category}%"))
            if limit:
                command = command.filter(self._events.c.limit == limit)
            if club_id:
                command = command.filter(self._events.c.club_id == club_id)

            result = session.execute(command)
            res = result.fetchall()

        ans = []
        for event in res:
            ans.append(
                {
                    "event_id": event[0],
                    "event_name": event[1],
                    "event_location": event[2],
                    "categories": event[3].split(","),
                    "start_time": event[4],
                    "end_time": event[5],
                    "limit": event[6],
                    "price": event[7],
                    "on_duty": event[8],
                    "rating": event[9],
                    "club_id": event[10],
                }
            )
        return ans

    def get_event_ids(self):
        with Session(self.engine) as session:
            command = self._events.select()
            result = session.execute(command)
            res = result.fetchall()
        return {x[0] for x in res}

    def add_event(
        self,
        event_name: str,
        event_location: str,
        categories: List[str],
        start_time: int,
        end_time: int,
        limit: int,
        club_id: int,
        price: Optional[float] = 0.0
    ):
        event_ids = self.get_event_ids()
        new_id = unique_id()

        while new_id in event_ids:
            new_id = unique_id()

        with Session(self.engine) as session:
            command = self._events.insert().values(
                event_id=new_id,
                event_name=event_name,
                event_location=event_location,
                categories=",".join(categories),
                start_time=start_time,
                end_time=end_time,
                limit=limit,
                price=price,
                club_id=club_id,
            )
            session.execute(command)
            session.commit()

        return new_id

    def get_registered_events(self, user_id: int):
        with Session(self.engine) as session:
            command = self._registrations.select().where(self._registrations.c.user_id == user_id)
            result = session.execute(command)
            res = result.fetchall()
        ans = []
        for entry in res:
            ans.append(
                {
                    "registration_id": entry[0],
                    "user_id": entry[1],
                    "event_name": entry[2],
                    "event_id": entry[3],
                    "status": "confirmed",
                }
            )
        with Session(self.engine) as session:
            # check waiting and pending lists
            command = self._waitlist.select().where(self._waitlist.c.user_id == user_id)
            result = session.execute(command)
            res = result.fetchall()
        for entry in res:
            ans.append({"registration_id": entry[3], "user_id": entry[0], "event_id": entry[1], "status": "waiting"})

        with Session(self.engine) as session:
            command = self._pendinglist.select().where(self._pendinglist.c.user_id == user_id)
            result = session.execute(command)
            res = result.fetchall()
        for entry in res:
            ans.append({"registration_id": entry[3], "user_id": entry[0], "event_id": entry[1], "status": "pending"})
        return ans

    def get_registrations(self, event_id: Optional[int] = None):
        ans = []

        # Get confirmed registrations
        with Session(self.engine) as session:
            command = self._registrations.select()
            if event_id:
                command = command.where(self._registrations.c.event_id == event_id)
            result = session.execute(command)
            res = result.fetchall()

            for entry in res:
                ans.append(
                    {
                        "registration_id": entry[0],
                        "user_id": entry[1],
                        "event_name": entry[2],
                        "event_id": entry[3],
                        "status": "confirmed",
                    }
                )

        # Get waitlist registrations
        with Session(self.engine) as session:
            command = self._waitlist.select()
            if event_id:
                command = command.where(self._waitlist.c.event_id == event_id)
            result = session.execute(command)
            res = result.fetchall()

            for entry in res:
                ans.append(
                    {
                        "registration_id": entry[3],
                        "user_id": entry[0],
                        "event_id": entry[1],
                        "registration_timestamp": entry[2],
                        "status": "waiting",
                    }
                )

        # Get pending registrations
        with Session(self.engine) as session:
            command = self._pendinglist.select()
            if event_id:
                command = command.where(self._pendinglist.c.event_id == event_id)
            result = session.execute(command)
            res = result.fetchall()

            for entry in res:
                ans.append(
                    {
                        "registration_id": entry[3],
                        "user_id": entry[0],
                        "event_id": entry[1],
                        "registration_timestamp": entry[2],
                        "status": "pending",
                    }
                )

        return ans

    def get_registration(self, registration_id: int):
        if registration_id in self.registration_map:
            return self.registration_map[registration_id]

        with Session(self.engine) as session:
            command = self._registrations.select().where(self._registrations.c.registration_id == registration_id)
            result = session.execute(command)
            res = result.fetchone()
        if not res:
            raise ValueError("Registration not found")

        return {"registration_id": res[0], "user_id": res[1], "event_name": res[2], "event_id": res[3]}

    def get_waiting_entry(self, registration_id: int):
        with Session(self.engine) as session:
            command = self._waitlist.select().where(self._waitlist.c.registration_id == registration_id)
            result = session.execute(command)
            res = result.fetchone()
        if not res:
            raise ValueError("Registration not found")
        return {
            "user_id": res[0],
            "event_id": res[1],
            "registration_timestamp": res[2],
            "registration_id": res[3],
        }

    def get_waiting_list(self):
        with Session(self.engine) as session:
            command = self._waitlist.select().order_by(self._waitlist.c.registration_timestamp)
            result = session.execute(command)
            res = result.fetchall()
        ans = []
        for entry in res:
            ans.append(
                {
                    "user_id": entry[0],
                    "event_id": entry[1],
                    "registration_timestamp": entry[2],
                    "registration_id": entry[3],
                }
            )
        return ans

    def get_pending_list(self):
        with Session(self.engine) as session:
            command = self._pendinglist.select().order_by(self._pendinglist.c.registration_timestamp)
            result = session.execute(command)
            res = result.fetchall()
        ans = []
        for entry in res:
            ans.append(
                {
                    "user_id": entry[0],
                    "event_id": entry[1],
                    "registration_timestamp": entry[2],
                    "registration_id": entry[3],
                }
            )
        return ans

    def register_event(self, event_name: str, user_id: int):
        self.remove_from_pending()
        existing_events = self.search_event(event_name=event_name)
        print(existing_events)
        if not existing_events:
            print("Event not found")
            raise ValueError("Event not found")
        existing_users = self.get_user(user_id=user_id)
        if not existing_users:
            print("User not found")
            raise ValueError("User not found")

        new_id = unique_id()
        existing = self.get_registrations()
        while new_id in existing:
            new_id = unique_id()

        print("New ID", new_id)

        limit = existing_events[0]["limit"]
        current = len(self.search_event(event_id=existing_events[0]["event_id"]))

        # if we need to push to the waiting list:
        if current >= limit:
            print("Adding to waitlist")
            with Session(self.engine) as session:
                command = self._waitlist.insert().values(
                    user_id=user_id,
                    event_id=existing_events[0]["event_id"],
                    registration_timestamp=int(time.time()),
                    registration_id=new_id,
                )
                session.execute(command)
                session.commit()
        else:
            print("Adding to registration")
            # there are seats available
            with Session(self.engine) as session:
                command = self._registrations.insert().values(
                    registration_id=new_id,
                    user_id=user_id,
                    event_name=event_name,
                    event_id=existing_events[0]["event_id"],  # first entry of the first result of the event name lookup
                )
                # todo: implement limit to registrations
                session.execute(command)
                session.commit()

        return new_id

    def add_to_pending(self):
        waiting_list = self.get_waiting_list()
        if not waiting_list:
            return
        entry = waiting_list[0]
        with Session(self.engine) as session:
            command = self._pendinglist.insert().values(
                user_id=entry["user_id"],
                event_id=entry["event_id"],
                registration_timestamp=int(time.time()),
                registration_id=entry["registration_id"],
            )
            session.execute(command)
            session.commit()

    def add_to_waiting(self, user_id, event_id, registration_timestamp, registration_id):
        with Session(self.engine) as session:
            command = self._waitlist.insert().values(
                user_id=user_id,
                event_id=event_id,
                registration_timestamp=registration_timestamp,
                registration_id=registration_id,
            )
            session.execute(command)
            session.commit()

    def remove_from_pending(self):
        pending_list = self.get_pending_list()
        for ele in pending_list:
            if ele["registration_timestamp"] + 3600 < int(time.time()):
                with Session(self.engine) as session:
                    command = self._pendinglist.delete().where(
                        self._pendinglist.c.registration_id == ele["registration_id"]
                    )
                    session.execute(command)
                    session.commit()
                self.add_to_waiting(ele["user_id"], ele["event_id"], int(time.time()), ele["registration_id"])

    def cancel_registration(self, registration_id):
        try:
            self.get_waiting_entry(registration_id)
            with Session(self.engine) as session:
                command = self._waitlist.delete().where(self._waitlist.c.registration_id == registration_id)
                session.execute(command)
                session.commit()

            with Session(self.engine) as session:
                command = self._pendinglist.delete().where(self._pendinglist.c.registration_id == registration_id)
                session.execute(command)
                session.commit()

        except ValueError:
            # it is not in the waiting list, so it raised a ValueError
            with Session(self.engine) as session:
                command = self._registrations.delete().where(self._registrations.c.registration_id == registration_id)
                session.execute(command)
                session.commit()

            # add a waitlist member to the pending list
            self.add_to_pending()

        return True

    def approve_registration(self, registration_id):
        self.remove_from_pending()
        # check if its in the pending table
        # if its not, raise error
        # if it is, and if the registration time is more than an hour ago, raise an error and remove from table
        # else, add to registration table
        with Session(self.engine) as session:
            command = self._pendinglist.select().where(self._pendinglist.c.registration_id == registration_id)
            result = session.execute(command)
            res = result.fetchone()
        if not res:
            raise ValueError("Registration not found")

        if int(time.time()) - res[2] > 3600:
            with Session(self.engine) as session:
                command = self._pendinglist.delete().where(self._pendinglist.c.registration_id == registration_id)
                session.execute(command)
                session.commit()
            raise ValueError("Registration expired")

        with Session(self.engine) as session:
            command = self._registrations.insert().values(
                registration_id=registration_id, user_id=res[0], event_id=res[1]
            )
            session.execute(command)
            session.commit()

            # Remove from pending list after successful registration
            command = self._pendinglist.delete().where(self._pendinglist.c.registration_id == registration_id)
            session.execute(command)
            session.commit()

        return {"registration_id": registration_id, "user_id": res[0], "event_id": res[1], "status": "confirmed"}

    def registration_status(self, registration_id):
        with Session(self.engine) as session:
            command = self._registrations.select().where(self._registrations.c.registration_id == registration_id)
            result = session.execute(command)
            res = result.fetchone()
        if res:
            return "confirmed"
        with Session(self.engine) as session:
            command = self._pendinglist.select().where(self._pendinglist.c.registration_id == registration_id)
            result = session.execute(command)
            res = result.fetchone()
        if res:
            return "pending"
        with Session(self.engine) as session:
            command = self._waitlist.select().where(self._waitlist.c.registration_id == registration_id)
            result = session.execute(command)
            res = result.fetchone()
        if res:
            return "waiting"
        return "not found"

    def update_club_upi(self, club_id: int, upi_id: str):
        with Session(self.engine) as session:
            command = self._clubs.update().where(self._clubs.c.club_id == club_id).values(upi_id=upi_id)
            session.execute(command)
            session.commit()

    def update_event_rating(self, event_id: int, new_rating: float):
        with Session(self.engine) as session:
            event = session.query(self._events).filter(self._events.c.event_id == event_id).first()
            if not event:
                raise ValueError("Event not found")

            if event.rating is None:
                event.rating = new_rating
            else:
                event.rating = (event.rating + new_rating) / 2

            session.commit()

    def get_leaderboard(self, limit: int = 10):
        with Session(self.engine) as session:
            # Subquery to calculate the average rating for each club
            subquery = (
                session.query(
                    self._events.c.club_id,
                    func.avg(self._events.c.rating).label("avg_rating"),
                )
                .group_by(self._events.c.club_id)
                .subquery()
            )

            # Query to retrieve club information and their average rating
            command = (
                session.query(
                    self._clubs.c.club_id,
                    self._clubs.c.club_name,
                    subquery.c.avg_rating,
                )
                .outerjoin(self._clubs, self._clubs.c.club_id == subquery.c.club_id)
                .order_by(subquery.c.avg_rating.desc())
                .limit(limit)
            )

            result = session.execute(command)
            res = result.fetchall()

        ans = []
        for club_id, club_name, avg_rating in res:
            ans.append(
                {
                    "club_id": club_id,
                    "club_name": club_name,
                    "average_rating": avg_rating if avg_rating is not None else 0.0,
                }
            )
        return ans
