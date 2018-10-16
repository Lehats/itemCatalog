from sqlalchemy import create_engine, desc, asc, exists, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from setupDb import Parts, Base, Categories, Users

engine = create_engine('sqlite:///parts.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# #####*************** delete db entries ****************#####################

# Deletes existing db entries to avoid double entries
countParts = session.query(Parts).order_by(Parts.id.desc()).first()
if countParts:
    for x in range(0, countParts.id):
        deletePart = session.query(Parts).first()
        if not deletePart:
            break
        session.delete(deletePart)
        session.commit()

# Deletes existing category entries to avoid double entries
countCategories = session.query(Categories).order_by(
    Categories.id.desc()).first()

if countCategories:
    for x in range(0, countCategories.id):
        deleteCategory = session.query(Categories).first()
        if not deleteCategory:
            break
        session.delete(deleteCategory)
        session.commit()

# Deletes existing category entries to avoid double entries
countUsers = session.query(Users).order_by(Users.id.desc()).first()
if countUsers:
    for x in range(0, countUsers.id):
        deleteUser = session.query(Users).first()
        if not deleteUser:
            break
        session.delete(deleteUser)
        session.commit()

# #####*************** create db entries ****************#####################
# User 1
User1 = Users(username="Jean12")
User1.hashThePassword("hello")

session.add(User1)
session.commit()

# User 2
User2 = Users(username="Max")
User2.hashThePassword("gugus")

session.add(User2)
session.commit()

# Category 1
Category1 = Categories(name='Batteries,Starting,Charching')

session.add(Category1)
session.commit()

# Category 2
Category2 = Categories(name='Brakes')

session.add(Category2)
session.commit()

# Category 3
Category3 = Categories(name='Drivetrain')

session.add(Category3)
session.commit()

# Category 4
Category4 = Categories(name='Belt-drive')

session.add(Category4)
session.commit()

# Category 5
Category5 = Categories(name='Ignition')

session.add(Category5)
session.commit()

# Part 1
Part1 = Parts(
    name='Alternator', description="Contrary to popular belief your "
    "battery isn't in charge of powering everything in your vehicle. "
    "Without an alternator, your car battery can't "
    "charge and nothing in your vehicle receives any power. If "
    "you've tried starting your vehicle and it just won't go, "
    "it may not be your battery's fault. Don't let a damaged "
    " alternator keep you stranded in the parking lot - AutoZone "
    "sells a variety of chrome alternators for your make and model "
    "to get you back up and running.",
    category=Category1, user=User1)

session.add(Part1)
session.commit()

# Part 2
Part2 = Parts(
    name='Starter', description="Your engine starter is designed to "
    "utilize a 12-volt, high-amperage electrical source (a battery) "
    "to turn your engine over and start it. The starter, obviously,"
    "plays a significant role in starting your vehicle, so it's "
    "imperative that it remains in tip-top condition. ",
    category=Category1, user=User1)

session.add(Part2)
session.commit()

# Part 3
Part3 = Parts(
    name='Brakedisk', description="Sometimes it is not good "
    "enough to just change your brake pads, "
    "but when it comes to stopping power, your brakes are "
    "only as good as your brake rotors. Stop on a dime at a "
    "price you can afford with new rotors from AutoZone. "
    "We carry a wide array of genuine OE and quality "
    "aftermarket rotors, all designed to meet or exceed "
    "your vehicles original braking power.",
    category=Category2, user=User1)

session.add(Part3)
session.commit()

# Part 4
Part4 = Parts(
    name='CV axle', description="If you're tired of hearing "
    "loud noises as you accelerate down the freeway, it's "
    "probably time to replace that CV (constant velocity) "
    "axle, which is primarily used in front-wheel drive "
    "vehicles. Without a properly functioning CV axle, "
    "your ride can have problems "
    "turning and can even become undrivable.",
    category=Category3, user=User1)

session.add(Part4)
session.commit()

# Part 5
Part5 = Parts(
    name='Automatic transmission', description="Your automatic "
    "transmission frees you from "
    "having to shift gears manually while you're cruising in "
    "your ride, so it should always be as easy as that.",
    category=Category3, user=User1)

session.add(Part5)
session.commit()

# Part 6
Part6 = Parts(
    name='Belt', description="This belt is designed to provide "
    "better belt-to-pulley contact. The specialized rubber compound"
    "incorporates a high temperature polymer formulated to maximize"
    "load carrying requirements and belt life. This Drive Rite"
    "belt is made with specially treated polyester cords to ensure"
    "length and tension stability. This belt has been constructed "
    "and engineered to meet the stringent demands of today's "
    "automotive drive systems. The Drive Rite v-ribbed "
    "belt delivers long-lasting dependable belt life.",
    category=Category4, user=User2)

session.add(Part6)
session.commit()

# Part 7
Part7 = Parts(
    name='Pulley', description="Pulleys are made from either thermoplastic"
    "or steel,depending upon the OEM application demands. The pulleys are"
    "grooved, flat, or flat with flanges to meet OEM standards. A dust cover"
    "is used to eliminate the possibility of dirt and other contaminates"
    "from harming the bearing.",
    category=Category4, user=User2)

session.add(Part7)
session.commit()

# Part 8
Part8 = Parts(
    name='Spark plug', description="Guaranteed to deliver quick starts,"
    "good fuel economy and smooth acceleration."
    "The copper core increases the rate of heat"
    "conduction in the sparkplug tip and improves"
    "resistance to all types of fouling.",
    category=Category5, user=User2)

session.add(Part8)
session.commit()
print "added parts to parts.db"
