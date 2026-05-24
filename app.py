from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


# --------------------------------
# MATRIX MULTIPLICATION
# --------------------------------
def mult_matrix(M, N):

    tuple_N = list(zip(*N))

    return [[sum(el_m * el_n for el_m, el_n in zip(row_m, col_n))
             for col_n in tuple_N] for row_m in M]


# --------------------------------
# PIVOT MATRIX
# --------------------------------
def pivot_matrix(M):

    m = len(M)

    identity = [[float(i == j) for i in range(m)] for j in range(m)]

    for j in range(m):

        row = max(range(j, m), key=lambda i: abs(M[i][j]))

        if j != row:
            identity[j], identity[row] = identity[row], identity[j]

    return identity


# --------------------------------
# LU DECOMPOSITION
# --------------------------------
def lu_decomposition(A):

    n = len(A)

    L = [[0.0] * n for i in range(n)]
    U = [[0.0] * n for i in range(n)]

    steps = []

    # Pivot Matrix
    P = pivot_matrix(A)

    # PA
    PA = mult_matrix(P, A)

    # Decomposition
    for j in range(n):

        L[j][j] = 1.0

        # Upper Matrix
        for i in range(j + 1):

            s1 = sum(U[k][j] * L[i][k] for k in range(i))

            U[i][j] = PA[i][j] - s1

            steps.append(
                f"U[{i+1}][{j+1}] = {PA[i][j]} - {round(s1,4)} = {round(U[i][j],4)}"
            )

        # Lower Matrix
        for i in range(j, n):

            s2 = sum(U[k][j] * L[i][k] for k in range(j))

            L[i][j] = (PA[i][j] - s2) / U[j][j]

            steps.append(
                f"L[{i+1}][{j+1}] = ({PA[i][j]} - {round(s2,4)}) / {round(U[j][j],4)} = {round(L[i][j],4)}"
            )

    return P, L, U, PA, steps


# --------------------------------
# HOME ROUTE
# --------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    size = 3

    P = None
    L = None
    U = None
    PA = None
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

            P, L, U, PA, steps = lu_decomposition(matrix)

            P = np.round(np.array(P), 4)
            L = np.round(np.array(L), 4)
            U = np.round(np.array(U), 4)
            PA = np.round(np.array(PA), 4)

        except Exception as e:

            error = str(e)

    return render_template(
        "index.html",
        size=size,
        P=P,
        L=L,
        U=U,
        PA=PA,
        steps=steps,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
