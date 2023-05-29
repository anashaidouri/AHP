import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from IPython.display import display

def calculate_priorities(features, total_point):
    
    # There are n features, so an n*n 'ones' matrix is composed.
    # The elements on the diagonal are all one.
    n = len(features[0])
    ahp_matrix = np.ones([n,n])
    
    # The matrix is filled according to ahp calculations.
    for i in range(0,n):
        for j in range(0,n):
            # The element (j,i) equals 1/(i,j)
            if i<j:
                if i==0:
                    # The first row is the second row of the input list. 
                    ahp_matrix[i,j] = float(features[1][j-1])
                    # Then, the first column is filled.
                    ahp_matrix[j,i] = 1/float(ahp_matrix[i,j])
                else:
                    # The rest of the cells are filled according to firs row.
                    if ahp_matrix[0,j]>ahp_matrix[0,i]:
                        ahp_matrix[i,j] = ahp_matrix[0,j]-ahp_matrix[0,i]+1
                    else:
                        ahp_matrix[i,j] = 1/((ahp_matrix[0,i]-ahp_matrix[0,j])+1)
                    ahp_matrix[j,i] = 1/float(ahp_matrix[i,j])
    
    # The matrix is normalized according to axis 0
    normed_matrix = normalize(ahp_matrix, axis=0, norm='l1')
    
    # Weights are calculated
    weights = normed_matrix.mean(1)
    # The total point is distributed according to weights
    
    points = total_point*weights
    # Feature names and points are stored in a dataframe
    
    return dict(zip(features[0],points))

critetia = [['Experience','Education','Charisma','Age'],[4,3,7]]
total_point = 1
main_dict = calculate_priorities(critetia, total_point)

experience_feature = [['Dict','Tom','Harry'],[4,9]]
experience_dict = calculate_priorities(experience_feature, main_dict['Experience'])

education_feature = [['Harry','Tom','Dict'],[5,7]]
education_dict = calculate_priorities(education_feature, main_dict['Education'])

charisma_feature = [['Tom','Dict','Harry'],[5,9]]
charisma_dict = calculate_priorities(charisma_feature, main_dict['Charisma'])

age_feature = [['Dict','Tom','Harry'],[3,9]]
age_dict = calculate_priorities(age_feature, main_dict['Age'])

df = pd.DataFrame([experience_dict, education_dict, charisma_dict, age_dict])
df.index = main_dict.keys()
total = df.sum()
total.name = 'Total'
df = pd.concat([df,total.to_frame().T])
df
display(df)