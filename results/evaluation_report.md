# ASC Cross-Encoder Evaluation Report

## Overall Metrics

| Metric | Value |
|--------|-------|
| accuracy | 0.9534 |
| precision_macro | 0.9441 |
| recall_macro | 0.9438 |
| f1_macro | 0.9440 |
| f1_weighted | 0.9534 |

## Per-Tier Negative Accuracy

| Tier | Accuracy |
|------|----------|
| T1 | 0.9440 |
| T2 | 0.9737 |
| T3 | 0.9300 |

## Candidate-Constrained Evaluation

- Constrained accuracy: **0.9671** (3758/3886)
- Unseen verbs (fell back to all 62): 0
- Random baseline accuracy: **0.9076**
- Lift over random: **+0.0594**

## Corpus vs. Synthetic

| Source | F1 | Count |
|--------|-----|-------|
| corpus | 0.9099 | 11959 |
| synthetic | 0.9713 | 1227 |

## Per-Situation F1

| Situation | F1 | Precision | Recall | Support |
|-----------|-----|-----------|--------|---------|
| Aggression | 0.898 | 0.917 | 0.880 | 200 |
| Buying | 0.982 | 0.964 | 1.000 | 204 |
| Capacity | 0.971 | 0.943 | 1.000 | 200 |
| Carrying | 0.869 | 0.878 | 0.860 | 200 |
| Cause_Change_of_State | 0.854 | 0.891 | 0.820 | 200 |
| Cause_Creation | 0.795 | 0.843 | 0.753 | 243 |
| Cause_Incremental | 0.911 | 0.902 | 0.920 | 200 |
| Cause_Membership | 0.900 | 0.900 | 0.900 | 200 |
| Cause_Participation | 0.917 | 0.971 | 0.868 | 226 |
| Cause_and_Effect | 1.000 | 1.000 | 1.000 | 238 |
| Change_of_State | 0.804 | 0.788 | 0.820 | 200 |
| Charge | 1.000 | 1.000 | 1.000 | 200 |
| Collective | 0.992 | 0.985 | 1.000 | 216 |
| Communicate | 0.881 | 0.875 | 0.887 | 221 |
| Concealment | 0.949 | 0.959 | 0.940 | 200 |
| Constrain | 0.986 | 0.986 | 0.986 | 221 |
| Contact | 0.929 | 0.939 | 0.920 | 200 |
| Counting | 0.991 | 0.983 | 1.000 | 208 |
| Desire | 0.932 | 0.906 | 0.960 | 200 |
| Discovery | 0.833 | 0.833 | 0.833 | 216 |
| Dynamic_Possession | 0.833 | 0.870 | 0.800 | 200 |
| Emission | 0.900 | 0.900 | 0.900 | 200 |
| Emotion_(exp. subj.) | 0.783 | 0.750 | 0.818 | 205 |
| Emotion_(stim. subj.) | 0.714 | 0.729 | 0.700 | 200 |
| Enforcement | 0.992 | 0.985 | 1.000 | 214 |
| Evaluation | 0.977 | 0.964 | 0.991 | 257 |
| Existence | 0.747 | 0.829 | 0.680 | 200 |
| Feeding | 0.985 | 0.970 | 1.000 | 215 |
| Form | 0.971 | 0.943 | 1.000 | 200 |
| Future_Having | 0.851 | 0.909 | 0.800 | 200 |
| Hurt | 0.889 | 0.898 | 0.880 | 200 |
| Image_Creation | 0.894 | 0.932 | 0.859 | 214 |
| Incremental | 0.783 | 0.857 | 0.720 | 200 |
| Induction | 0.911 | 0.902 | 0.920 | 200 |
| Ingestion | 0.986 | 0.986 | 0.986 | 223 |
| Intention | 0.905 | 0.874 | 0.938 | 327 |
| Joint_Statement | 0.957 | 0.947 | 0.968 | 243 |
| Learning | 0.930 | 0.909 | 0.952 | 213 |
| Limitation | 0.980 | 0.962 | 1.000 | 200 |
| Location | 0.869 | 0.878 | 0.860 | 200 |
| Manipulation | 0.951 | 0.925 | 0.980 | 200 |
| Measurement | 0.904 | 0.945 | 0.867 | 210 |
| Membership | 0.954 | 0.973 | 0.935 | 227 |
| Motion | 0.831 | 0.875 | 0.790 | 212 |
| Participation | 0.889 | 0.898 | 0.880 | 200 |
| Payment | 0.965 | 0.971 | 0.958 | 221 |
| Perception_(exp._subj.) | 0.925 | 0.895 | 0.958 | 221 |
| Perception_(stim._subj.) | 0.970 | 0.961 | 0.980 | 200 |
| Pick_Up_and_Drop_Off | 0.939 | 0.958 | 0.920 | 200 |
| Possession | 1.000 | 1.000 | 1.000 | 242 |
| Protection | 0.984 | 0.984 | 0.984 | 211 |
| Pursuit | 0.893 | 0.868 | 0.920 | 200 |
| Reciprocal | 0.875 | 0.875 | 0.875 | 214 |
| Replacement | 1.000 | 1.000 | 1.000 | 202 |
| Request | 0.927 | 0.891 | 0.965 | 235 |
| Response | 0.979 | 0.972 | 0.986 | 220 |
| Selling | 0.971 | 0.943 | 1.000 | 200 |
| Sending | 0.978 | 0.971 | 0.986 | 219 |
| Statement | 0.842 | 0.810 | 0.877 | 223 |
| Throwing | 0.961 | 0.961 | 0.961 | 201 |
| Transfer_of_Possession | 0.920 | 0.920 | 0.920 | 200 |
| Vehicular_Motion | 0.945 | 0.958 | 0.932 | 224 |

## Situations Needing Attention (F1 < 0.7)

None — all Situations above 0.7 threshold.
