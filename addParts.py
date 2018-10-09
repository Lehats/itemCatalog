from sqlalchemy import create_engine, desc,asc, exists, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from setupDb import Parts, Base, Categories

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

# Deletes existing db entries to avoid double entries
countParts = session.query(Parts).order_by(Parts.id.desc()).first()
#print (countParts.id)
if countParts:
    for x in range(0, countParts.id):
        deletePart = session.query(Parts).first()
        if not deletePart:
            break
        session.delete(deletePart)
        session.commit()

# Deletes existing category entries to avoid double entries
#countParts = session.query(Parts.Categories).order_by(Parts.categories.id.desc()).first()
countParts = session.query(Categories).order_by(Categories.id.desc()).first()
#print (countParts.id)
if countParts:
    for x in range(0, countParts.id):
        deletePart = session.query(Categories).first()
        if not deletePart:
            break
        session.delete(deletePart)
        session.commit()

# Category 1
Category1 = Categories(name='Batteries, Starting and Charching')

session.add(Category1)
session.commit()

# Category 2
Category2 = Categories(name='Brakes and traction control')

session.add(Category2)
session.commit()

# Part 1
Part1 = Parts(name='Alternator', description = "Contrary to popular belief your battery isn't in charge of"
            "powering everything in your vehicle. Without an alternator, your car battery can't "
            "charge and nothing in your vehicle receives any power. If you've tried starting your "
            "vehicle and it just won't go, it may not be your battery's fault. Don't let a damaged "
            " alternator keep you stranded in the parking lot - AutoZone sells a variety of chrome " 
            "alternators for your make and model to get you back up and running.", 
             category = Category1 )

session.add(Part1)
session.commit()

# Part 2
Part2 = Parts(name='Starter', description = "Your engine starter is designed to utilize a 12-volt, "
"high-amperage electrical source (a battery) to turn your engine over and start it. The starter, obviously,"
"plays a significant role in starting your vehicle, so it's imperative that it remains in tip-top condition. ", 
            category = Category1)

session.add(Part2)
session.commit()

# Part 3
Part3 = Parts(name='Brakedisk', description = "Sometimes it is not good enough to just change your brake pads, "
"but when it comes to stopping power, your brakes are only as good as your brake rotors. Stop on a dime at a "
"price you can afford with new rotors from AutoZone. We carry a wide array of genuine OE and quality aftermarket "
"rotors, all designed to meet or exceed your vehicles original braking power.", 
            category = Category2)

session.add(Part3)
session.commit()


print "added parts to parts.db"