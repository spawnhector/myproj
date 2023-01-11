def createTables(get_connection,psycopg2,commands):
    conn = get_connection()
    cur = conn.cursor()
    try:
        for command in commands:
            cur.execute(command)
        print("tables created.")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertPairs(get_connection,psycopg2,pair_list):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "INSERT INTO pairs(pair_symbol) VALUES(%s)"
        for pair in pair_list:
            row = getPair(get_connection,psycopg2,pair)
            if row is None:
                cur.execute(sql,pair)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertSignals(get_connection,psycopg2,pair_id,result):
    conn = get_connection()
    cur = conn.cursor()
    try:
        signal_query = "INSERT INTO signals(trade_type,trade_price,take_profit,trade_date) VALUES(%s,%s,%s,%s) RETURNING signal_id;"
        assign_pair = "INSERT INTO pair_signal(pair_id,signal_id) VALUES(%s,%s);"
        cur.execute(signal_query,(
            result['trade_type'],
            result['trade_price'],
            result['take_profit'],
            result['trade_date']
            ))
        # get the signal id
        signal_id = cur.fetchone()[0]
        cur.execute(assign_pair, (pair_id, signal_id))
        # commit changes
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getPair(get_connection,psycopg2,pair):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT * FROM pairs WHERE pair_symbol = (%s);"
        cur.execute(sql,(pair,))
        row = cur.fetchone()
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
