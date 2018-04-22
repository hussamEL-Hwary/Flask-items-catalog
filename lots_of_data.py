from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User, Category, Item


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# user
usr = User(username="hussam", email="hos@hos.com")
usr.hash_password("123456")
session.add(usr)
session.commit()

# categories
cat = Category(name="Action")
session.add(cat)
session.commit()

cat1 = Category(name="Adventure")
session.add(cat1)
session.commit()

cat2 = Category(name="Animation")
session.add(cat2)
session.commit()


cat3 = Category(name="Comedy")
session.add(cat3)
session.commit()


cat4 = Category(name="Crime")
session.add(cat4)
session.commit()


cat5 = Category(name="Drama")
session.add(cat5)
session.commit()


cat2 = Category(name="Family")
session.add(cat2)
session.commit()


cat6 = Category(name="Fantasy")
session.add(cat6)
session.commit()


cat7 = Category(name="Musical")
session.add(cat7)
session.commit()


cat8 = Category(name="War")
session.add(cat8)
session.commit()

cat9 = Category(name="Sport")
session.add(cat9)
session.commit()


# items
item = Item(title="Bomb City",
            description="Bomb City is a crime-drama, about the "
                        "cultural aversion of a "
                        "group of punk rockers in a conservative Texas town."
                        " Their ongoing "
                        "battle with a rival, more-affluent clique"
                        " leads to a controversial "
                        "hate crime that questions the morality of"
                        " American justice. Based "
                        "on the true story of Brian Deneke.",
            user_id=1,
            category_id=1)
session.add(item)
session.commit()

item = Item(title="Paris, Texas",
            description="A man wanders out of the desert after"
                        " a four year absence."
                        " His brother finds him, and together "
                        "they return to L.A. to "
                        "reunite the man with his young son. "
                        "Soon after, he and the "
                        "boy set out to locate the mother of "
                        "the child, who left shortly "
                        "after the man disappeared.",
            user_id=1,
            category_id=1)
session.add(item)
session.commit()

item = Item(title="Den of Thieves",
            description="A gritty L.A crime saga which "
                        "follows the intersecting "
                        "and often personally connected "
                        "lives of an elite unit "
                        "of the LA County Sheriff's Dept. "
                        "and the state's most "
                        "successful bank robbery crew as the outlaws "
                        "plan a seemingly "
                        "impossible heist on the Federal Reserve Bank "
                        "of downtown Los Angeles.",
            user_id=1,
            category_id=1)
session.add(item)
session.commit()


item = Item(title="Coco",
            description="Despite his family's baffling generations-old "
                        "ban on music,"
                        " Miguel dreams of becoming an accomplished "
                        "musician like his idol, "
                        "Ernesto de la Cruz. Desperate to prove "
                        "his talent, Miguel finds "
                        "himself in the stunning and colorful Land "
                        "of the Dead following "
                        "a mysterious chain of events. Along the way, "
                        "he meets charming "
                        "trickster Hector, and together, they set off "
                        "on an extraordinary "
                        "journey to unlock the real story behind Miguel's "
                        "family history.",
            user_id=1,
            category_id=3)
session.add(item)
session.commit()


item = Item(title="Paddington 2",
            description="Paddington is happily settled with the Brown "
                        "family in Windsor Gardens, "
                        "where he has become a popular member of the "
                        "community, spreading joy and "
                        "marmalade wherever he goes. While searching "
                        " the perfect present for "
                        "his beloved Aunt Lucy's 100th birthday, "
                        "Paddington spots a unique pop-up "
                        "book in Mr. Gruber's antique shop, and "
                        "embarks upon a series of odd jobs "
                        "to buy it. But when the book is stolen, it's up "
                        "to Paddington and the Browns "
                        "to unmask the thief.",
            user_id=1,
            category_id=3)
session.add(item)
session.commit()

item = Item(title="Your Name",
            description="Mitsuha is the daughter of the mayor of a "
                        "small mountain town. She's a "
                        "straightforward high school girl who lives "
                        "with her sister and her "
                        "grandmother and has no qualms about letting it "
                        "be known that she's "
                        "uninterested in Shinto rituals or helping her "
                        "father's electoral campaign. "
                        "Instead she dreams of leaving the boring town and "
                        "trying her luck in Tokyo. "
                        "Taki is a high school boy in Tokyo who "
                        "works part-time "
                        "in an Italian restaurant "
                        "and aspires to become an architect "
                        "or an artist. Every "
                        "night he has a strange "
                        "dream where he becomes...a high school girl in "
                        "a small mountain town.",
            user_id=1,
            category_id=3)
session.add(item)
session.commit()

item = Item(title="Loving",
            description="The story of Richard and Mildred Loving, "
                        "a couple whose arrest for interracial "
                        "marriage in 1960s "
                        "Virginia began a legal battle that would "
                        "end with the Supreme "
                        "Court's historic 1967 decision.",
            user_id=1,
            category_id=6)
session.add(item)
session.commit()

item = Item(title="The Foster Boy",
            description="The illegitimate orphan child, 12-year-old Max, "
                        "is sold by the local minister "
                        "for a basket of food "
                        "to the Bosiger family, who own a mountain "
                        "farm. Max "
                        "initial hope of finally finding a "
                        "loving home is "
                        "brutally shattered: The farmer and "
                        "his wife treat Max "
                        "like livestock, and their son Jacob "
                        "humiliates and abuses him."
                        " Only the local teacher notices the "
                        "child suffering on the farm.",
            user_id=1,
            category_id=6)
session.add(item)
session.commit()

item = Item(title="Silent Night",
            description="Adam unexpectedly visits his family house at "
                        "Christmas after a few years of working abroad. "
                        "No family member knows about his secret plans and "
                        "the real reasons of his visit.",
            user_id=1,
            category_id=6)
session.add(item)
session.commit()

item = Item(title="Dunkirk",
            description="Evacuation of Allied soldiers from the "
                        "British Empire, "
                        "and France, who were cut off and "
                        "surrounded by the German "
                        "army from the beaches and "
                        "harbor of Dunkirk, France, between "
                        "May 26- June 04, 1940, during Battle of "
                        "France in World War II.",
            user_id=1,
            category_id=10)
session.add(item)
session.commit()

item = Item(title="Threads",
            description="Documentary style account of a nuclear "
                        "holocaust and its effect on the working class "
                        "city of Sheffield, England; and the eventual "
                        "long running effects of nuclear"
                        " war on civilization.",
            user_id=1,
            category_id=10)
session.add(item)
session.commit()

item = Item(title="Glory",
            description="Shaw was an officer in the Federal Army during the "
                        "American Civil War who "
                        "volunteered to lead the first "
                        "company of black soldiers. Shaw was forced to deal "
                        "with the prejudices of both the enemy "
                        "(who had orders "
                        "to kill commanding officers of blacks), and of his "
                        "own fellow officers.",
            user_id=1,
            category_id=10)
session.add(item)
session.commit()


print "done!"
