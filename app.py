Ибрагим, [06/05/2025  19:07]
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# Database connection
try:
    conn = psycopg2.connect(
        host='db-ibrohimjon.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com',
        database='mydatabase',
        user='postgres',
        password='postgres',
        port=5432
    )
    logging.info("Successfully connected to the database")
except Exception as e:
    logging.error(f"Failed to connect to the database: {str(e)}")
    raise Exception(f"Database connection failed: {str(e)}")

# Helper to clean/convert data
def clean_value(value):
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in ['nan', '', '__', 'hello']:
            return None
        return value.replace(',', '') if ',' in value else value
    return value

# Root route (for debugging or status)
@app.route('/')
def home():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, movie_name, year_of_release, category, run_time, 
                   genre, imdb_rating, votes, gross_total 
            FROM "tbl_ibrohim_data"
        """)
        movies = cur.fetchall()
        logging.info(f"Fetched {len(movies)} movies from tbl_ibrohim_data: {movies}")

        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'tbl_ibrohim_data'")
        columns = [row[0] for row in cur.fetchall()]
        logging.info(f"Table columns: {columns}")

        cur.close()
        return jsonify({'status': 'API is running, HTML served from S3'})
    except Exception as e:
        logging.error(f"Error in home route: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Endpoint to provide JSON data
@app.route('/data', methods=['GET'])def get_data():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, movie_name, year_of_release, category, run_time, 
                   genre, imdb_rating, votes, gross_total 
            FROM "tbl_ibrohim_data"
        """)
        movies = cur.fetchall()
        logging.info(f"Fetched {len(movies)} movies for /data endpoint")
        cur.close()
        return jsonify([{
            'id': movie[0],
            'movie_name': movie[1],
            'year_of_release': movie[2],
            'category': movie[3],
            'run_time': movie[4],
            'genre': movie[5],
            'imdb_rating': movie[6],
            'votes': movie[7],
            'gross_total': movie[8]
        } for movie in movies])
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return jsonify({'error': f"Error fetching data: {str(e)}"}), 500

Ибрагим, [06/05/2025  19:07]
# Endpoint to add a new movie
@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    logging.info(f"Received add request: {data}")
    movie_name = clean_value(data.get('movie_name'))
    year_of_release = clean_value(data.get('year_of_release'))
    category = clean_value(data.get('category'))
    run_time = clean_value(data.get('run_time'))
    genre = clean_value(data.get('genre'))
    imdb_rating = clean_value(data.get('imdb_rating'))
    votes = clean_value(data.get('votes'))
    gross_total = clean_value(data.get('gross_total'))
    if not all([movie_name, year_of_release, category, run_time, genre, imdb_rating, votes, gross_total]):
        logging.error("Missing required fields")
        return jsonify({'error': 'All fields (movie_name, year_of_release, category, run_time, genre, imdb_rating, votes, gross_total) are required'}), 400
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO "tbl_ibrohim_data" (movie_name, year_of_release, category, run_time, genre, imdb_rating, votes, gross_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (movie_name, year_of_release, category, run_time, genre, imdb_rating, votes, gross_total))
        movie_id = cur.fetchone()[0]
        conn.commit()
        logging.info(f"Inserted movie with id: {movie_id}")
        cur.close()
        return jsonify({'status': 'Data inserted successfully', 'id': movie_id})
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data: {str(e)}")
        return jsonify({'error': f"Error inserting data: {str(e)}"}), 500

# Endpoint to delete a movie
@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    movie_id = data.get('id')
    logging.info(f"Received delete request for id: {movie_id}")
    if not movie_id or movie_id is None:
        logging.error("Missing or null id field")
        return jsonify({'error': 'A valid integer id is required'}), 400
    try:
        movie_id = int(movie_id)  # Ensure id is an integer
        cur = conn.cursor()
        cur.execute("""DELETE FROM "tbl_ibrohim_data" WHERE id = %s""", (movie_id,))
        if cur.rowcount == 0:
            logging.warning(f"No movie found with id: {movie_id}")
            return jsonify({'error': 'No movie found with the specified id'}), 404
        conn.commit()
        logging.info(f"Deleted movie with id: {movie_id}")
        cur.close()
        return jsonify({'status': 'Data deleted successfully'})
    except ValueError:
        logging.error(f"Invalid id format: {movie_id}")
        return jsonify({'error': 'id must be a valid integer'}), 400
    except Exception as e:
        conn.rollback()
        logging.error(f"Error deleting data: {str(e)}")
        return jsonify({'error': f"Error deleting data: {str(e)}"}), 500

# Close connection when app exits
import atexit
atexit.register(lambda: conn.close() or logging.info("Database connection closed"))

if name == '__main__':
    app.run(host='0.0.0.0', port=8000)
