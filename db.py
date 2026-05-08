import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn(): 
    print(DATABASE_URL)	
    return psycopg2.connect("postgresql://postgres:xQq7psf5A98LYYT1@db.uwnzamzijsbtkikioavg.supabase.co:5432/postgres", sslmode="require")