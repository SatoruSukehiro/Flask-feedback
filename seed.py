from app import app
from models import db, User,Feedback


db.drop_all()
db.create_all()
#SEEDEDUSERS
user1 = User.register(username="zacharysmith8",password="weber123",email="PollyWantACracker@yahoo.com", first_name="Mikey",last_name="Triskitallian")

user2 = User.register(username="BigBecca",password="BlabberJaw",email="MasonMargiela227@yahoo.com", first_name="Rebecca",last_name="Stiltsworth") 

user3 = User.register(username="trapdobando",password="alldayeveryday",email="CatchMeIfYouCanr@yahoo.com", first_name="Trap",last_name="Price")

user4 = User.register(username="DirtyDaniella",password="HBIC101",email="CrackerJacks@yahoo.com", first_name="Dani",last_name="PurrPURR")

user5 = User.register(username="MansonFanatic",password="Hellurrr",email="DangerZone@yahoo.com", first_name="Marty",last_name="McFly")
db.session.add_all([user1,user2,user3,user4,user5])
db.session.commit()

#SEEDEDFEEDBACK
feedback1 = Feedback(title="Bigger Cups",content="I think you would benifit with bigger cups",username='zacharysmith8')

feedback2 = Feedback(title="Smaller Cups",content="I think you would benifit with smaller cups",username='zacharysmith8')

feedback3= Feedback(title="DO AS YOU PLEASE",content="YOURE DOING GREAT",username='MansonFanatic')

feedback4= Feedback(title="drop the title",content="I think if you changed the stores name you would do better",username='DirtyDaniella')

db.session.add_all([feedback1,feedback2,feedback3,feedback4])
db.session.commit()