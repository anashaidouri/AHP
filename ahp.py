import streamlit as st  #For building and sharing web apps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #For graphical comparison and analysis
from streamlit_option_menu import option_menu
from crud import *

W2 = []
W = []
subcriteria_dict = {}
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


def calculate_ahp(A, B, n, m, criterias, alternatives, subcriteria_dict):
    for i in range(0, n):
        for j in range(i, n):
            if i != j:
                A[j][i] = float(1/A[i][j])

    dfA = pd.DataFrame(A)
    st.markdown(" #### Criteria Table")
    st.table(dfA)

    W2 = get_weight(A, "Criteria Table")
    W3 = np.zeros((n, m))
    
    for i in range(0, n):
        for j in range(0, m):
            for k in range(j, m):
                if j != k:
                    B[i][k][j] = float(1 / B[i][j][k])

        dfB = pd.DataFrame(B[i])
        st.markdown(" #### Alternative Table for Criterion " + criterias[i])
        st.table(dfB)

        w3 = get_weight(B[i], "Alternatives Table for Criterion " + criterias[i])
        W3[i] = w3
        st.pyplot(plot_graph(w3, subcriteria_dict[criterias[i]], "Subcriteria", "Weights of Subcriteria for Criterion " + criterias[i]))

    W = np.dot(W2, W3)

    st.pyplot(plot_graph(W2, criterias, "Criteria", "Weights of Criteria"))

    st.pyplot(plot_graph(W, alternatives, "Alternatives", "Optimal Alternative for given Criteria"))

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
        options=["AHP-Calculator", "Dashboard", "About"],
        icons=["calculator-fill", "pencil-fill", "info-circle"], 
        orientation="horizontal",
    )
    n = 0 
    m = 0
    A = np.zeros((n, n))
    B = np.zeros((n, m, m))
    
    criterias = []
    alternatives = []
    if selected == "AHP-Calculator":
        st.header("AHP Calculator")
        st.title("Goal")
        goal = st.text_input("Enter Goal")
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
        
        if cri and alt :
            # expander for pairwise comparison for criteria
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

            # add expander for pairwise comparison for subcriteria
            with st.expander("Subcriteria Weights"):
                for criterion in criterias:
                    st.subheader(f"Pairwise comparison for Subcriteria of {criterion}")
                    subcriteria_weights = np.zeros((len(subcriteria_dict[criterion]), len(subcriteria_dict[criterion])))

                    for i in range(len(subcriteria_dict[criterion])):
                        for j in range(i, len(subcriteria_dict[criterion])):
                            if i == j:
                                subcriteria_weights[i][j] = 1
                            else:
                                weight = st.slider(f"How much higher is {subcriteria_dict[criterion][i]} in comparison with {subcriteria_dict[criterion][j]}?", 1, 9, 1)
                                subcriteria_weights[i][j] = weight
                                subcriteria_weights[j][i] = 1 / weight

                        st.table(pd.DataFrame(subcriteria_weights, index=subcriteria_dict[criterion], columns=subcriteria_dict[criterion]))                   
            # expander for pairwise comparison for alternatives        
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
 
            st.header("click the button below to get your decision")
            btn = st.button("Calculate AHP")
            st.write("##")
            if btn:
                calculate_ahp(A, B, n, m, criterias, alternatives, subcriteria_dict)


# dashboard
    if selected == "Dashboard":
        st.header("Previous Decisions:")
        goals = all_goals()
        for goal in goals:
            goal_id = goal[0]
            goal_name = goal[1]
            with st.expander(goal_name):
                st.subheader("Modify or Delete Criteria")
                criteria_list = all_criteria(goal_id)
                for criteria in criteria_list:
                    criteria_id = criteria["criteria_id"]  # Update the key to match the correct field name
                    criteria_name = criteria["criteria_name"]  # Update the key to match the correct field name
                    st.write(criteria_name)
                    subcriteria_list = all_subcriteria(criteria_id)  # Updated call for subcriteria
                    alternatives_list = all_alternatives(goal_id)  # Updated call for alternatives

                    for subcriteria in subcriteria_list:
                        st.write(subcriteria[1])
                        st.button(f"Delete {subcriteria[1]}", key=f"delete_subcriteria_{subcriteria[0]}")

                    st.subheader("Modify or Delete Alternatives")
                    for alternative in alternatives_list:
                        st.write(alternative[1])
                        st.button(f"Delete {alternative[1]}", key=f"delete_alternative_{criteria_id}_{alternative[0]}")

            button_col13, button_col14 = st.columns(2)
            with button_col13:
                st.button("Edit Goal", key=f"edit_goal_{goal_id}")
            with button_col14:
                st.button("Delete Result", key=f"delete_result_{goal_id}")
                
    if selected == "About":
        st.header("MCDM")
        with st.expander(' ##### Multi-Criteria Decision Making '):
            st.write("It is a process used to make decisions when there are multiple conflicting criteria that must be considered. MCDM methods use mathematical models to evaluate the different options and their potential outcomes, considering various factors.")

        st.write("---")
        st.write("##")

        with st.expander(' ##### MCDM Techniques '):
            st.write(" - Analytic Hierarchy Process (AHP)")
            st.write(" - Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)")
            st.write(" - Elimination and Choice Expressing Reality (ELECTRE)")
            st.write(" - Simple Additive Weighting (SAW)")
            st.write(" - VlseKriterijumska Optimizacija I Kompromisno Resenje (VIKOR)")

        st.write("---")
        st.write("##")

        with st.expander(' ##### Applications of MCDM '):
            st.markdown(" ##### Applications of MCDM")
            st.write(" - Business decision making")
            st.write(" - Engineering design")
            st.write(" - Environmental management")
            st.write(" - Medical decision making")

        st.write("---")
        st.write("##")

        with st.expander(" ##### Future of MCDM"):
            st.write("Multi-Criteria Decision Making (MCDM) technology is already transforming the way complex decisions are made. In the future, MCDM is likely to become even more powerful and influential due to the increasing availability of big data, advances in machine learning and artificial intelligence, and improvements in computer hardware and software. These factors will allow for more sophisticated decision-making tools that can adapt and learn over time, making real-time decision making possible in complex environments.")
            st.write("One of the most promising areas for the application of MCDM technology is in the field of sustainability. As the world faces growing concerns about climate change and environmental degradation, MCDM techniques can be used to help organizations and governments make decisions that balance economic, social, and environmental factors. By using MCDM to analyze large amounts of data and identify the most sustainable options, decision makers can ensure that their decisions are not only financially sound, but also environmentally responsible and socially equitable. The future of MCDM technology is bright, and its potential to transform decision-making processes will likely have far-reaching implications for a wide range of industries and sectors.")

               
        
if __name__ == '__main__':
    main()