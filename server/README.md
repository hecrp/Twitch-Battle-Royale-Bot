# Twitch Battle Royale Server

This server module is part of the Twitch Battle Royale project, which allows users to participate in a Battle Royale game through Twitch chat. The server handles the backend operations, including database management, API endpoints, and serving the web interface.

## Installation

To install the required dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Configuration

This application requires PostgreSQL, which is not included in the 'requirements.txt' file and needs to be installed manually.

For information on how to install PostgreSQL, you can refer to the official documentation: https://www.postgresql.org/download/

Once PostgreSQL is installed, configure the database connection in the 'config.py' file:

```python
DATABASE_CONFIG={
    'dbname': 'twitch_battle_royale',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost'
}
``` 

## Database Setup

Before running the server, you need to set up the database and create the necessary tables. Follow these steps:

1. Ensure that PostgreSQL is installed and running.

2. Run the following script to create the required database and tables:

   ```bash
   python create_tables.py
   ```

    This script will create the necessary database and tables.

3. Activate the database flag in the bot.py file. Look for a line similar to:

   ```python
   USE_DATABASE = False
   ```

   Change it to:

   ```python
   USE_DATABASE = True
   ```

4. (Optional) If you want to load sample data to test the dashboard, you can use the fill_db.py script:

   ```bash
   python fill_db.py
   ```

   This will **reset** and repopulate your database with sample users, games, and statistics.


By following these steps, you'll have a fully set up database ready for use with the Twitch Battle Royale server.

## Usage

To start the server, run the following command:
```bash
python app.py
```

## Docker (testing)

To run the server in a Docker container, run the following command:
```bash
docker build -t twitch_battle_royale_server .
docker run -p 8050:8050 twitch_battle_royale_server
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.    