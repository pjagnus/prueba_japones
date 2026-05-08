import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn(): 
    print(DATABASE_URL)	
    URL = "postgresql://postgres.uwnzamzijsbtkikioavg:xQq7psf5A98LYYT1@aws-1-us-west-2.pooler.supabase.com:6543/postgres"
    #URL_OLD="postgresql://postgres:xQq7psf5A98LYYT1@db.uwnzamzijsbtkikioavg.supabase.co:5432/postgres", sslmode="require"
    return psycopg2.connect(URL)
    
