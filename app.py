from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


def doolittle_lu(A):
    n = len(A)

    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        L[i][i] = 1

    for j in range(n):

        # Upper Triangular
        for i in range(j + 1):
            sum1 = 0
            for k in range(i):
                sum1 += U[k][j] * L[i][k]

            U[i][j] = A[i][j] - sum1

        # Lower Triangular
        for i in range(j, n):
            sum1 = 0
            for k in range(j):
                sum1 += U[k][j] * L[i][k]

            if U[j][j] == 0:
                raise ValueError("Division by zero encountered!")

            L[i][j] = (A[i][j] - sum1) / U[j][j]

    return L, U


@app.route("/", methods=["GET", "POST"])
def index():
    L = None
    U = None
    matrix = None
    error = None

    if request.method == "POST":
        try:
            size = int(request.form["size"])

            matrix = []

            for i in range(size):
                row = []
                for j in range(size):
                    value = float(request.form[f"cell_{i}_{j}"])
                    row.append(value)
                matrix.append(row)

            A = np.array(matrix)

            L, U = doolittle_lu(A)

            L = np.round(L, 4).tolist()
            U = np.round(U, 4).tolist()

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        L=L,
        U=U,
        matrix=matrix,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)