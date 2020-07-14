import sqlite3

def connect(city):
    conn = sqlite3.connect("property_data.db")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {city} (id INTEGER PRIMARY KEY, date_listed text, price integer, address integer, beds integer, bathrooms integer, reception_rooms integer, agent_name text, agent_tel text, website text, acquire_time text)")
    conn.commit()
    conn.close()

def check(city, address):
    conn=sqlite3.connect("property_data.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

    print(f"\nENTRY CHECK - Searching tables for: {address}")
    for tablerow in cur.fetchall():
        table = tablerow[0]
        cur.execute(f"SELECT * FROM {table} where address=?", (address,))
        result = cur.fetchall()
        if result:
            print(f"Already exists in {table.upper()}")
            return True

    if not result:
        print("Does not exist")
        return False
    else:
        return True


def insert(city, date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time):
    if check(city, address) == False:
        conn=sqlite3.connect("property_data.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {city} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time))
        conn.commit()
        conn.close()
        return "new"
    else:
        # print(f"Entry already exists for: {address}")
        return "existing"

def view(city):    
    conn=sqlite3.connect("property_data.db")
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM {city}")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(city, date_listed="", price="", address="", beds="", bathrooms="", reception_rooms="", website="", acquire_time=""):
    conn=sqlite3.connect("property_data.db")
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM {city} WHERE date_listed=? OR price=? OR address=? OR beds=? OR bathrooms=? OR reception_rooms=? OR website=? OR acquire_time=?", (date_listed, price, address, beds, bathrooms, reception_rooms, website, acquire_time))
    rows = cur.fetchall()
    conn.close()
    return rows

def update(city, date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time):
    conn=sqlite3.connect("property_data.db")
    cur=conn.cursor()
    cur.execute(f"UPDATE {city} SET date_listed=?, price=?, beds=?, bathrooms=?, reception_rooms=?, agent_name=?, agent_tel=? WHERE address=?, WHERE website=?, WHERE acquire_time=?", (date_listed, price, beds, bathrooms, reception_rooms, agent_name, agent_tel, address, website, acquire_time)) 
    conn.commit()
    conn.close()
