from flask import Flask, request, render_template_string
from itertools import permutations

app = Flask(__name__)
INF = float('inf')

def tsp_brute_force(cost, n):
    """Brute force TSP solver"""
    cities = list(range(1, n))
    best_cost = INF
    best_path = None
    for perm in permutations(cities):
        path = [0] + list(perm) + [0]
        c = sum(cost[path[i]][path[i+1]] for i in range(n))
        if c < best_cost:
            best_cost = c
            best_path = path
    return best_path, best_cost

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        # User input: comma-separated rows of matrix
        raw = request.form["matrix"].strip().split("\n")
        cost = []
        for row in raw:
            cost.append([INF if x.strip()=="INF" else int(x) for x in row.split(",")])
        n = len(cost)
        cities = [chr(65+i) for i in range(n)]  # A, B, C, ...

        best_path, best_cost = tsp_brute_force(cost, n)

        # Format output
        result += "TSP - Cost Matrix:<br>"
        result += "&nbsp;&nbsp;&nbsp;" + " ".join(f"{c:>5}" for c in cities) + "<br>"
        for i, row in enumerate(cost):
            r = ['INF' if x == INF else str(x) for x in row]
            result += f"{cities[i]:>4} " + " ".join(f"{v:>5}" for v in r) + "<br>"

        result += f"<br>Optimal Tour: {' -> '.join(cities[i] for i in best_path)}<br>"
        result += f"Minimum Cost: {best_cost}<br><br>Path verification:<br>"
        for i in range(n):
            u, v = best_path[i], best_path[i+1]
            result += f"&nbsp;&nbsp;{cities[u]} -> {cities[v]}: cost = {cost[u][v]}<br>"

    return render_template_string("""
        <h2>Traveling Salesman Problem Solver</h2>
        <form method="post">
            <label>Enter Cost Matrix (comma-separated, use INF for infinity):</label><br>
            <textarea name="matrix" rows="6" cols="40"></textarea><br><br>
            <input type="submit" value="Solve TSP">
        </form>
        <hr>
        <div>{{result|safe}}</div>
    """, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
