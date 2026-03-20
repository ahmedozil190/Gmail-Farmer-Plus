import random
import string

# Extensive list of common first names
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Alexander", "Debra",
    "Frank", "Rachel", "Patrick", "Carolyn", "Raymond", "Janet", "Jack", "Catherine",
    "Dennis", "Maria", "Jerry", "Heather", "Tyler", "Diane", "Aaron", "Ruth",
    "Jose", "Julie", "Adam", "Olivia", "Nathan", "Joyce", "Henry", "Virginia",
    "Douglas", "Victoria", "Zachary", "Kelly", "Peter", "Lauren", "Kyle", "Christina",
    "Ethan", "Joan", "Walter", "Evelyn", "Noah", "Judith", "Jeremy", "Megan",
    "Christian", "Andrea", "Keith", "Cheryl", "Roger", "Hannah", "Terry", "Jacqueline",
    "Gerald", "Martha", "Sean", "Gloria", "Lucille", "Arthur", "Ann", "Lawrence", "Teresa"
]

# Extensive list of common last names
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzales", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennet", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez"
]

def generate_strong_password(length=12):
    """Generate a strong random alphanumeric password."""
    # Ensure there's at least one lowercase, one uppercase, one digit
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits

    all_chars = lower + upper + digits
    
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits)
    ]
    
    # Fill the rest
    for _ in range(length - 3):
        password.append(random.choice(all_chars))
        
    random.shuffle(password)
    return ''.join(password)

def generate_account_data():
    """Generates realistic pseudo-random human account data."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    # Random number to append (e.g. birth year or random 3-4 digit string)
    rnd_num = random.randint(1975, 9999)
    
    # Mix email formats to look natural
    formats = [
        f"{first_name.lower()}.{last_name.lower()}{rnd_num}",
        f"{first_name.lower()}{last_name.lower()}{rnd_num}",
        f"{first_name.lower()[0]}{last_name.lower()}{rnd_num}",  # Initial + last name
        f"{first_name.lower()}_{last_name.lower()}{rnd_num}",
    ]
    
    email_user = random.choice(formats)
    email = f"{email_user}@gmail.com"
    
    password = generate_strong_password()
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }
