import psycopg2
import os


DATABASE_URL = "postgresql://postgres:xQq7psf5A98LYYT1@db.uwnzamzijsbtkikioavg.supabase.co:5432/postgres"
def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

a = get_conn()

ac = a.cursor()

#sql = "insert into parentesco values (2,'3xxx')"
sql = "delete  from grupos"
ac.execute(sql)

sql = "delete  from socios"
ac.execute(sql)
a.commit()