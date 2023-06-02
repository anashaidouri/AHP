import streamlit as st  #For build and share web apps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #For graphical comparison and analysis
from streamlit_option_menu import option_menu



@st.cache_data
def get_weight(A, str):
    n = A.shape[0]
    e_vals, e_vecs = np.linalg.eig(A)
    lamb = max(e_vals)
    w = e_vecs[:, e_vals.argmax()]
    w = w / np.sum(w)  # Normalization
    # Consistency Checking
    ri = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24,
          7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51}
    ci = (lamb - n) / (n - 1)
    cr = ci / ri[n]
    print("The normalized eigen vector:")
    print(w)
    print('CR = %f' % cr)
    if cr >= 0.1:
        print("Failed Consistency check of "+str)
        st.error("Failed Consistency check of "+str)

    return w


def plot_graph(x, y, ylabel, title):
    # Create a horizontal bar chart
    fig, ax = plt.subplots()
    ax.bar(y, x, color='#FF4B4B')
    ax.set_facecolor('#F0F2F6')
    # Set title and axis labels
    ax.set_title(title)
    ax.set_xlabel(ylabel)
    ax.set_ylabel("Values")
    return fig

def welcome_page():
    st.title("Welcome to AHP Calculator")
    st.write("This app allows you to perform Analytic Hierarchy Process (AHP) calculations.")
    st.write("Please enter the necessary information to proceed.")

    user_input = st.text_input("Enter your goal:")
    proceed_button = st.button("Proceed")

    if proceed_button:
        return user_input

@st.cache_data
def calculate_ahp(A, B, n, m, criterias, alternatives, subcriteria_dict):


    for i in range(0, n):
        for j in range(i, n):
            if i != j:
                A[j][i] = float(1/A[i][j])
    # print("A : ")
    # print(str(A))
    dfA = pd.DataFrame(A)
    # Use tabel instead of dataframe because dataframe are interactable
    st.markdown(" #### Criteria Table")
    st.table(dfA)
    for k in range(0, n):
        for i in range(0, m):
            for j in range(i, m):
                if i != j:
                    B[k][j][i] = float(1/B[k][i][j])
    # print("B : ")
    # print(str(B))
    st.write("---")
    for i in range(0, n):
        dfB = pd.DataFrame(B[i])
        # Use tabel instead of dataframe because dataframe are interactable
        st.markdown(" #### Alternative Table for Criterion " + criterias[i])
        st.table(dfB)
    W2 = get_weight(A, "Criteria Table")
    W3 = np.zeros((n, m))
    for i in range(0, n):
        w3 = get_weight(B[i], "Alternatives Table for Criterion "+ criterias[i])
        W3[i] = w3
    W = np.dot(W2, W3)

    st.pyplot(plot_graph(W2, criterias, "Criteria", "Weights of Criteria"))

    st.pyplot(plot_graph(W, alternatives, "Alternatives", "Optimal Alternative for given Criteria"))
    st.balloons()


def main():
    st.set_page_config(page_title="AHP Calculator", page_icon=":bar_chart:")

    # hide default streamlit page style
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["AHP-Calculator", "Dashboard"],
        icons=["calculator-fill", "bar-chart-fill"], 
        orientation="horizontal",
    )
    if selected == "AHP-Calculator":
        st.header("AHP Calculator")
        st.title("Goal")
        goal = st.text_input("Enter Goal")

        subcriteria_dict = {}

        st.title("Criteria & Alternatives")
        cri = st.text_input("Enter Criteria")
        criterias = cri.split(",")

        # Add subcriteria for each criterion
        for criterion in criterias:
            subcriteria = st.text_input(f"Enter Subcriteria for {criterion}")
            subcriteria_list = subcriteria.split(",")
            subcriteria_dict[criterion] = subcriteria_list

        alt = st.text_input("Enter Alternatives")
        alternatives = alt.split(",")
        st.info("Enter multiple values of fields, separated by comma without any spaces.")
        st.info("Example: first_value, second_value, ...")
        
        if cri and alt and subcriteria:
            with st.expander("Criteria Weights"):
                st.subheader("Pairwise comparision for Criteria")
                st.write("---")
                n = len(criterias)
                A = np.zeros((n, n))
                Aradio = np.zeros((n,n))
                for i in range(0, n):
                    for j in range(i, n):
                        if i == j:
                            A[i][j] = 1
                        else:
                            st.markdown(" ##### Criterion " + criterias[i] + " comparison with Criterion " + criterias[j])
                            criteriaradio = st.radio("Select higher priority criterion ", (criterias[i], criterias[j],), horizontal=True)
                            if criteriaradio == criterias[i]:
                                A[i][j] = st.slider(label="How much higher " + criterias[i] + " is in comparison with " + criterias[j] + "?", min_value=1, max_value=9, value=1)
                                A[j][i] = float(1/A[i][j])
                            else:
                                A[j][i] = st.slider(label="How much higher " + criterias[j] + " is in comparison with " + criterias[i] + "?", min_value=1, max_value=9, value=1)
                                A[i][j] = float(1/A[j][i])
                    
            with st.expander("Alternative Weights"):
                st.subheader("Pairwise comparision for Alternatives")
                m = len(alternatives)
                B = np.zeros((n, m, m))

                for k in range(0, n):
                    st.write("---")
                    st.markdown(" ##### Alternative comparison for Criterion " + criterias[k])
                    for i in range(0, m):
                        for j in range(i, m):
                            if i == j:
                                B[k][i][j] = 1
                            else:
                                alternativeradio = st.radio("Select higher priority alternative for criteria " + criterias[k], (alternatives[i], alternatives[j],), horizontal=True)
                                if alternativeradio == alternatives[i]:
                                    B[k][i][j] = st.slider("Considering Criterion " + criterias[k] + ", how much higher " + alternatives[i] + " is in comparison with " + alternatives[j] + "?", 1, 9, 1)
                                    B[k][j][i] = float(1/B[k][i][j])
                                else:
                                    B[k][j][i] = st.slider("Considering Criterion " + criterias[k] + ", how much higher " + alternatives[j] + " is in comparison with " + alternatives[i] + "?", 1, 9, 1)
                                    B[k][i][j] = float(1/B[k][j][i])


                    
            btn = st.button("Calculate AHP")
            st.write("##")
            if btn:
                calculate_ahp(A, B, n, m, criterias, alternatives, subcriteria_dict)
    if selected == "Dashboard":
        st.write("dashboard")



if __name__ == '__main__':
    main()
