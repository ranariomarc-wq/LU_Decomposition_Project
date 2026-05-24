from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


def lu_doolittle(A):
    n = len(A)

    L = np.zeros((n, n))
    U = np.zeros((n, n))

    steps = []

    for i in range(n):
        L[i][i] = 1

    for j in range(n):

        # Compute U
        for i in range(j + 1):

            sum_val = 0

            for k in range(i):
                sum_val += L[i][k] * U[k][j]

            U[i][j] = A[i][j] - sum_val

            steps.append(
                f"U[{i+1}][{j+1}] = {A[i][j]} - {round(sum_val,4)} = {round(U[i][j],4)}"
            )

        # Compute L
        for i in range(j, n):

            sum_val = 0

            for k in range(j):
                sum_val += L[i][k] * U[k][j]

            L[i][j] = (A[i][j] - sum_val) / U[j][j]

            steps.append(
                f"L[{i+1}][{j+1}] = ({A[i][j]} - {round(sum_val,4)}) / {round(U[j][j],4)} = {round(L[i][j],4)}"
            )

    return L, U, steps


@app.route("/", methods=["GET", "POST"])
def index():

    size = 3
    matrix = None
    L = None
    U = None
    steps = []
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

            L, U, steps = lu_doolittle(A)

            L = np.round(L, 4)
            U = np.round(U, 4)

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        size=size,
        matrix=matrix,
        L=L,
        U=U,
        steps=steps,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
