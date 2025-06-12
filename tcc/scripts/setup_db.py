from db.connect import connect_db


def run_ddl():
    print("Running DDL to create tables...")
    queries = [
        """CREATE TABLE users (
        id UUID PRIMARY KEY,
        email VARCHAR NOT NULL UNIQUE,
        password VARCHAR NOT NULL,
        identification VARCHAR NOT NULL
    );""",
        """CREATE TABLE contracts_contents (
        id UUID PRIMARY KEY,
        address VARCHAR NOT NULL UNIQUE,
        content_index VARCHAR NOT NULL UNIQUE,
        content BYTEA NOT NULL
    );
    """,
    ]

    conn = connect_db()

    for query in queries:
        with conn.cursor() as cursor:
            cursor.execute(query)
            print(f"Executed query: {query.strip()}")

    conn.commit()
    print("DDL executed successfully.")
    conn.close()

def run_dml():
    print("Running DML to insert initial data...")
    # todo: when pre-seeding the test_password, make sure to hash it first.
    queries = [
        """
        INSERT INTO users (id, email, password, identification)
        VALUES
            ('00000000-0000-0000-0000-000000000001', 'test@user.com', '$2b$14$pov3fzaIZPy53dJD8Lg80OZM3FT5Fwg0qlZB2ardAwF3LJS8YA5Ze', 'Test User')
        ;
        """
    ]
    conn = connect_db()
    for query in queries:
        with conn.cursor() as cursor:
            cursor.execute(query)
            print(f"Executed query: {query.strip()}")
    conn.commit()
    print("DML executed successfully.")
    conn.close()


if __name__ == "__main__":
    run_ddl()
    run_dml()
    print("Database setup completed successfully.")
