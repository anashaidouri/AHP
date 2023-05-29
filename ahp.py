import streamlit as st
import pandas as pd
import seaborn as sns
from scipy.spatial.distance import squareform
import numpy as np
import matplotlib.pyplot as plt

# Function: Make Matrix
def make_matrix(arr):
    """
    Goal:
    Transform the input to the appropriate format

    Input:
    arr: the array with the weight in the right order (w = [w1, w2, w3, w4, ...])

    Output:
    A: Transformed the w array to get the right format of the A matrix
    """
    X = squareform(arr).astype(float)
    row, col = np.diag_indices(X.shape[0])
    X[row, col] = np.ones(X.shape[0])
    for i in range(len(row)):
        for j in range(len(col)):
            if j < i:
                X[i, j] = 1 / X[i, j]
    A = np.asarray(X)
    return A

# Function: AHP - One participant
def AHP_1_Participant(arr):
    """
    Goal:
    Apply the AHP only on one participant to calculate the Consistency ratio, the weights,
    their standard deviation, and the rgmm

    Input:
    arr: the array with the weight in the right order (w = [w1, w2, w3, w4, ..., wi])

    Output:
    A: Transformed the w array to get the right format of the A matrix (using the make_matrix function)
    p: A dataframe with the normalized weights of the criteria and their standard deviation
    cr: The consistency ratio of the participant
    rggm: The RGMM values of the participant

    Plot:
    1. The A matrix with the answers to cross-validate it
    2. The Consistency Ratio Matrix to detect the "suspicious" weights
    3. The consistency ratio of each participant and the normalized one
    """
    alpha = 0.1
    A = make_matrix(arr)
    n = len(A)
    x_ticks = ['C{}'.format(i) for i in range(1, n + 1)]
    sums = np.array(pd.DataFrame(A).sum())
    ln_rgmm = np.log(A)
    rgmm_sum = np.array(np.exp(pd.DataFrame(ln_rgmm).sum(axis=1) / n))
    rgmm_sum_2 = rgmm_sum.sum()
    rggm = rgmm_sum / rgmm_sum_2
    errors = np.zeros(np.shape(A))

    size = np.shape(errors)[1]
    for i in range(size):
        for j in range(size):
            errors[i, j] = np.log(A[i, j] * rggm[j] / rggm[i]) ** 2

    errors_sum = np.sum(errors, 0)
    error_calc = np.sqrt(errors_sum / (size - 1))
    rggm_cosh = rggm * np.cosh(error_calc)
    rggm_cosh_sum = np.sum(rggm_cosh)
    rggm_final = rggm_cosh / rggm_cosh_sum
    rggm_matmul = np.matmul(sums, rggm)

    plus_minus = rggm * np.sinh(error_calc) / rggm_cosh_sum
    cr0 = (rggm_matmul - n) / ((2.7699 * n - 4.3513) - n)
    eig_val = np.linalg.eig(A)[0].max()
    eig_vec = np.linalg.eig(A)[1][:, 0]
    p = np.round(np.real(eig_vec / eig_vec.sum()), 3)
    cr = np.round(np.real((eig_val - n) / ((2.7699 * n - 4.3513) - n)), 3)
    evt = np.real(A * size / eig_val)

    for i in range(size):
        for j in range(size):
            evt[i, j] = evt[i, j] * rggm_final[j]

    pi_pi = np.zeros(np.shape(A))
    for i in range(size):
        for j in range(size):
            pi_pi[i, j] = rggm[j] / rggm[i]

    pi_pi_A = pi_pi * A
    pi_pi_A2 = np.zeros(np.shape(A))
    for i in range(size):
        for j in range(size):
            if 1 / 9 < pi_pi_A[i, j] < 9:
                if pi_pi_A[i, j] > 1:
                    pi_pi_A2[i, j] = A[i, j] * pi_pi[i, j]
                else:
                    pi_pi_A2[i, j] = 1 / (A[i, j] * pi_pi[i, j])
            else:
                pi_pi_A2[i, j] = 0
    Consistency_ratio = list(pi_pi_A2[np.triu_indices(n, k=1)])
    std = np.array(pd.DataFrame(evt).std(1))
    plt.title('A')
    g1 = sns.heatmap(pd.DataFrame(np.tril(A)), annot=True, cmap="viridis", cbar=False)
    g1.set_xticklabels(x_ticks)
    g1.set_yticklabels(x_ticks)
    plt.show()
    plt.title('Consistency Ratio Matrix')
    g2 = sns.heatmap(pd.DataFrame(np.tril(pi_pi_A2)), annot=True, cmap="viridis", cbar=False)
    g2.set_yticklabels(x_ticks)
    g2.set_xticklabels(x_ticks)
    plt.show()
    p = pd.DataFrame(p, columns=['Weights'])
    p.index = p.index + 1
    p.index = 'Crit-' + p.index.astype(str)
    p['Weights'] = p['Weights'].astype(float).map("{:.2%}".format)
    p['Weights +/-'] = std
    p['Weights +/-'] = p['Weights +/-'].astype(float).map("{:.2%}".format)
    p['RGMM'] = rggm_final
    p['RGMM'] = p['RGMM'].astype(float).map("{:.2%}".format)
    p['+/-'] = plus_minus
    p['+/-'] = p['+/-'].astype(float).map("{:.2%}".format)
    print(p)
    print('\nConsistency Ratio: {:.2%} & Consistency Ratio of Weighted: {:.2%}'.format(cr0, cr))
    return A, p, cr, rggm

# Function: AHP - Consolidated
def AHP_Consolidated(A, rggm, w=1):
    """
    Goal:
    Apply the AHP to multiple participants to calculate the Consistency ratio, the weights,
    their standard deviation, and the consolidated A

    Input:
    A: a list containing the different A matrices (A = [A1, A2, A3, A4, ..., Ai])
       (came from the AHP_1_Participant function)
    rggm: a list containing the different rgmm matrices (rggm = [rgmm1, rgmm2, rgmm3, rgmm, ..., rgmmi])
          (came from the AHP_1_Participant function)
    w: the weight of the different stakeholders - Not yet implemented

    Output:
    cons_exp: The consolidated A matrix of the multiple participants
    p: A dataframe with the normalized weights of the criteria and their st. deviation
    cr: The consolidated consistency ratio

    Plot:
    1. The A matrix with the consolidated answers to cross-validate it
    2. The consolidated Consistency ratio and the consensus value
    """
    n = len(A)
    logs = []
    for i in A:
        logs.append(np.array(np.log(i)))
    cons = np.zeros(np.shape(logs[0]))
    table_rggm = pd.DataFrame(rggm)
    table_rggm_ln = -table_rggm * np.log(table_rggm)
    alphas = table_rggm_ln.sum(1)
    alpha = np.exp(np.sum(alphas) / n)
    Da = np.exp(alpha)
    gammas0 = table_rggm.sum(0) / n
    gammas = -gammas0 * np.log(gammas0)
    gamma = np.exp(np.sum(gammas))
    beta = gamma / alpha
    for i in logs:
        cons += i
    cons = cons / n
    cons_exp = np.exp(cons)
    size = np.shape(cons_exp)[1]
    x_ticks = ['C{}'.format(i) for i in range(1, size + 1)]
    ahp_cor1 = np.exp((-9 / (size + 8) * np.log(9 / (size + 8))) - (size - 1) * (1 / (size + 8) * np.log(1 / (size + 8))))
    ahp_cor2 = np.exp((size - n) * (-1 / (size + 8) * np.log(1 / (size + 8))) + n * (-(n + 8) / (size + 8) / n * np.log((n + 8) / (size + 8) / n)))
    ahp_cor3 = size / ahp_cor1
    it0 = (cons_exp.sum(1) / 10)
    it = np.matmul(cons_exp, it0)
    scale0 = it0 / np.max(it0)
    scale = it / np.max(it)
    for _ in range(20):
        it = np.matmul(cons_exp, scale)
        scale = it / np.max(it)

    norm = np.zeros(len(scale))
    for i in range(len(scale)):
        norm[i] = scale[i] / sum(scale)
    p = pd.DataFrame(norm, columns=['Cons Weights'])
    sum_cols = cons_exp.sum(0)
    lamda = (sum(sum_cols * norm))
    evt = np.real(size / lamda * cons_exp)
    for i in range(size):
        for j in range(size):
            evt[i, j] = evt[i, j] * norm[j]
    std = np.array(pd.DataFrame(evt).std(1))
    cr = (lamda - len(sum_cols)) / ((2.7699 * len(sum_cols) - 4.3513) - len(sum_cols))
    consensus = (1 / beta - 1 / ahp_cor3) / (1 - 1 / ahp_cor3)
    plt.title('Consolidated A Matrix')
    g = sns.heatmap(pd.DataFrame(cons_exp), annot=True, cmap="viridis", cbar=False)
    g.set_xticklabels(x_ticks)
    g.set_yticklabels(x_ticks)
    plt.show()
    print(p)
    print('\nConsolidated Consistency Ratio: {:.2%}'.format(cr))
    print('Consensus value: {:.2%}'.format(consensus))
    return cons_exp, p, cr

arr = [1, 1, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 6, 6, 3, 6, 3, 3, 1, 3, 1, 1, 3, 1, 1, 1, 1, 3, 3, 1, 0.333, 1, 1, 1, 1, 1, 0.333, 1, 0.333, 0.333, 1, 1, 1, 3]
A1, weights, cr, rgmm1 = AHP_1_Participant(arr)

# def main():
#     # Set the app title and sidebar options
#     st.title("Analytic Hierarchy Process (AHP) App")
#     st.sidebar.title("Configuration")

#     # Get user input for goal, criteria, and alternatives
#     goal = st.sidebar.text_input("Goal")
#     criteria = st.sidebar.text_input("Criteria (comma-separated)")
#     alternatives = st.sidebar.text_input("Alternatives (comma-separated)")

#     # Process the user input
#     criteria_list = [c.strip() for c in criteria.split(",")]
#     alternatives_list = [a.strip() for a in alternatives.split(",")]

#     # Display the input summary
#     st.sidebar.subheader("Input Summary")
#     st.sidebar.write("Goal:", goal)
#     st.sidebar.write("Criteria:", criteria_list)
#     st.sidebar.write("Alternatives:", alternatives_list)

#     # Perform AHP calculations when the user clicks a button
#     if st.sidebar.button("Run AHP"):
#         # Perform AHP calculations here
#         # ...

#         # Display the results
#         st.subheader("Results")
#         # Display the A matrix heatmap
#         st.pyplot(plt.figure(figsize=(10, 8)))
#         sns.heatmap(A, annot=True, fmt=".2f", cmap="Blues", xticklabels=criteria_list, yticklabels=criteria_list)
#         st.pyplot(plt)

#         # Display other results as desired
#         # ...


# if __name__ == "__main__":
#     main()

# Example usage:
# A = [np.array([[1, 1/2, 3], [2, 1, 5], [1/3, 1/5, 1]]),
#      np.array([[1, 2, 3], [1/2, 1, 2], [1/3, 1/2, 1]]),
#      np.array([[1, 1/3, 1/4], [3, 1, 1/2], [4, 2, 1]])]

# rggm = [np.array([0.3, 0.5, 0.2]),
#         np.array([0.2, 0.4, 0.4]),
#         np.array([0.4, 0.3, 0.3])]

# AHP_Consolidated(A, rggm)