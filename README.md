# AirBnB Clone v2 - MySQL

This is the second version of the AirBnB clone project, featuring MySQL database integration using SQLAlchemy ORM.

## Team Members
- Darlene Ayinkamiye

## Description

This project implements a command-line interface (CLI) for managing AirBnB-like objects with support for both file-based and database storage engines.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HBNB_ENV` | Running environment (`dev` or `test`) |
| `HBNB_MYSQL_USER` | MySQL username |
| `HBNB_MYSQL_PWD` | MySQL password |
| `HBNB_MYSQL_HOST` | MySQL hostname |
| `HBNB_MYSQL_DB` | MySQL database name |
| `HBNB_TYPE_STORAGE` | Storage type (`file` or `db`) |

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/alu-AirBnB_clone_v2.git
cd alu-AirBnB_clone_v2

# Install dependencies
pip install -r requirements.txt

# Set up MySQL databases
cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
cat setup_mysql_test.sql | mysql -hlocalhost -uroot -p
```

## Usage

### File Storage (default)
```bash
./console.py
```

### Database Storage
```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py
```

### Console Commands

| Command | Description |
|---------|-------------|
| `create <class> [params]` | Create a new object with optional parameters |
| `show <class> <id>` | Show an object |
| `destroy <class> <id>` | Delete an object |
| `all [class]` | Show all objects (optionally filtered by class) |
| `update <class> <id> <attr> <value>` | Update an object |
| `quit` | Exit the console |

### Parameter Syntax for Create
```bash
create State name="California"
create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 price_by_night=300 latitude=37.77 longitude=-122.43
```

## Testing

```bash
# Run all tests with FileStorage
python3 -m unittest discover tests

# Run all tests with DBStorage
HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db python3 -m unittest discover tests
```

## Project Structure

```
├── console.py              # Command-line interface
├── models/
│   ├── __init__.py         # Storage initialization
│   ├── base_model.py       # Base class for all models
│   ├── user.py             # User model
│   ├── state.py            # State model
│   ├── city.py             # City model
│   ├── place.py            # Place model
│   ├── amenity.py          # Amenity model
│   ├── review.py           # Review model
│   └── engine/
│       ├── __init__.py
│       ├── file_storage.py # File-based storage engine
│       └── db_storage.py   # Database storage engine
├── setup_mysql_dev.sql     # Development database setup
├── setup_mysql_test.sql    # Test database setup
└── tests/                  # Unit tests
```


Project Contributors:
-
- Teniola Olaleye
 Shakilla Uwamahoro