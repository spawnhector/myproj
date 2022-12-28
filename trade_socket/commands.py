def commands():
    return (
        """
        CREATE TABLE pairs (
            pair_id SERIAL PRIMARY KEY,
            pair_symbol VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE signals (
                signal_id SERIAL PRIMARY KEY,
                trade_type VARCHAR(255) NOT NULL,
                trade_price VARCHAR(255) NOT NULL,
                take_profit VARCHAR(255) NOT NULL,
                trade_date VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE pair_signal (
                pair_id INTEGER NOT NULL,
                signal_id INTEGER NOT NULL,
                PRIMARY KEY (pair_id , signal_id),
                FOREIGN KEY (pair_id)
                    REFERENCES pairs (pair_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (signal_id)
                    REFERENCES signals (signal_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
