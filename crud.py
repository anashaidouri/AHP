import mysql.connector
import streamlit as st


# connection
conn = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    db = "ahp"
)

c = conn.cursor()

# fetch
def all_goals():
    c.execute('select * from goal')
    data = c.fetchall()
    return data

def all_subcriteria(criteria_id):
    c.execute("SELECT * FROM subcriteria WHERE c_ID = %s", (criteria_id,))
    data = c.fetchall()
    return data


def all_alternatives(goal_id):
    c.execute("SELECT * FROM alternative WHERE g_ID = %s", (goal_id,))
    data = c.fetchall()
    return data

def all_criteria(goal_id):
    c.execute("SELECT * FROM criteria WHERE g_ID = %s", (goal_id,))
    criteria_data = c.fetchall()

    criteria_list = []
    for criteria_row in criteria_data:
        criteria_id = criteria_row[0]
        criteria_name = criteria_row[1]

        # Fetch subcriteria for the current criteria
        c.execute("SELECT sc_name FROM subcriteria WHERE c_ID = %s", (criteria_id,))
        subcriteria_data = c.fetchall()
        subcriteria_list = [subcriteria_row[0] for subcriteria_row in subcriteria_data]

        # Fetch alternatives for the current criteria
        c.execute("SELECT a_name FROM alternative WHERE g_ID = %s", (goal_id,))
        alternatives_data = c.fetchall()
        alternatives_list = [alternative_row[0] for alternative_row in alternatives_data]

        criteria_list.append({
            "criteria_id": criteria_id,
            "criteria_name": criteria_name,
            "subcriteria_list": subcriteria_list,
            "alternatives_list": alternatives_list
        })

    return criteria_list