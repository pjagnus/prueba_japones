from supabase import create_client, Client

url = "https://uwnzamzijsbtkikioavg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3bnphbXppanNidGtpa2lvYXZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwMTQzMzgsImV4cCI6MjA5MzU5MDMzOH0.Zy7QQ2ULv2ak5Xj5medfFPjyg4w9-YqYtnb6oXexF40"

supabase: Client = create_client(url, key)

response = supabase.table("usuarios").select("*").execute()

data = response.data
print(data)

response = supabase.table("usuarios").insert({
    "nombre": "Juan",
    "activo": True
}).execute()