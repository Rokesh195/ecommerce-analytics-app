from flask import Flask, request, jsonify, send_file
from db_utils import run_query
from llm_utils import ask_ollama
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

SYSTEM_PROMPT = """
You are a helpful assistant that takes user questions about e-commerce data and writes SQL queries based on the following tables:

Table: total_sales(date TEXT, item_id INTEGER, total_sales REAL, total_units_ordered INTEGER)
Table: ad_sales(date TEXT, item_id INTEGER, ad_sales REAL, impressions INTEGER, ad_spend REAL, clicks INTEGER, units_sold INTEGER)
Table: eligibility(eligibility_datetime_utc TEXT, item_id INTEGER, eligibility INTEGER, message TEXT)

Return ONLY the SQL query, without explanation. Use the exact column names as shown.
"""



@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question', '')
    # Step 1: Rephrase the question into SQL using the LLM
    prompt = SYSTEM_PROMPT + f"\nUser question: {user_question}\nSQL:"
    # ask_ollama returns only the SQL
    sql_query = ask_ollama(prompt).strip()
    # Step 2: Run SQL on the database
    try:
        cols, rows = run_query(sql_query)
        # Step 3: Compose a user-friendly answer
        result = [dict(zip(cols, row)) for row in rows]
        human_readable = f"Answer: {result}"
        return jsonify({
            "question": user_question,
            "sql_query": sql_query,
            "result": result,
            "human_readable": human_readable
        })
    except Exception as e:
        return jsonify({"error": str(e), "sql_query": sql_query}), 400

# (Bonus) Visualization endpoint
@app.route('/ask/visual', methods=['POST'])
def ask_visual():
    user_question = request.json.get('question', '')
    prompt = SYSTEM_PROMPT + f"\nUser question: {user_question}\nWrite an SQL query to get the relevant data for plotting."
    sql_query = ask_ollama(prompt)
    cols, rows = run_query(sql_query)
    plt.figure()
    # Example: plotting the first two columns
    plt.bar([str(x[0]) for x in rows], [float(x[1]) for x in rows])
    plt.title(user_question)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
