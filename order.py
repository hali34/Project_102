from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "orders.db"

# Only these database columns are permitted for sorting.
SORT_COLUMNS = {
    "date": "created_at",
    "total": "order_total",
    "status": "status"
}

SORT_DIRECTIONS = {
    "asc": "ASC",
    "desc": "DESC"
}


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/orders", methods=["GET"])
def get_orders():

    # Values supplied by the user
    status = request.args.get("status", "OPEN")
    requested_sort = request.args.get("sort", "date").lower()
    requested_direction = request.args.get("direction", "desc").lower()

    # Convert requested sort values to database values
    sort_column = SORT_COLUMNS.get(
        requested_sort,
        SORT_COLUMNS["date"]
    )

    sort_direction = SORT_DIRECTIONS.get(
        requested_direction,
        "DESC"
    )

    sql = f"""
        SELECT
            id,
            customer_name,
            order_total,
            status,
            created_at
        FROM orders
        WHERE status = ?
        ORDER BY {sort_column} {sort_direction}
        LIMIT 100
    """

    with get_connection() as conn:
        results = conn.execute(
            sql,
            (status,)
        ).fetchall()

    return jsonify([
        dict(row)
        for row in results
    ])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
