import psycopg2
def get_connection():
    try:
        return psycopg2.connect(
            database="myproj",
            user="MPYzyNUJMZCyzCVdzvItYfIBzoXODgUT",
            password="rpc99B22yoHZJgHczZXxV5uyZDpekj0j6vVsx444xPEMUmJAXSieiGrhbSGVCino",
            host="postgres", port="5432"
        )
    except:
        return False
