# Tier Census (v2 — synthetic overrides honored)

Config: target=50, T1=50%, T2=30%, T3=20%

Per-Situation targets: T1=25, T2=15, T3=10

Override hits: 701 synthetic rows re-tiered from intended labels


| Situation | Total | T1 now | T1 tgt | T1 gap | T2 now | T2 tgt | T2 gap | T3 now | T3 tgt | T3 gap | Total gap |
|-----------|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|-----------|
| Aggression | 50 | 26 | 25 | 0 | 16 | 15 | 0 | 8 | 10 | 2 | 2 |
| Buying | 54 | 14 | 25 | 11 | 28 | 15 | 0 | 12 | 10 | 0 | 11 |
| Capacity | 50 | 27 | 25 | 0 | 20 | 15 | 0 | 3 | 10 | 7 | 7 |
| Carrying | 50 | 19 | 25 | 6 | 21 | 15 | 0 | 10 | 10 | 0 | 6 |
| Cause_Change_of_State | 50 | 26 | 25 | 0 | 13 | 15 | 2 | 11 | 10 | 0 | 2 |
| Cause_Creation | 93 | 20 | 25 | 5 | 33 | 15 | 0 | 40 | 10 | 0 | 5 |
| Cause_Incremental | 50 | 15 | 25 | 10 | 19 | 15 | 0 | 16 | 10 | 0 | 10 |
| Cause_Membership | 50 | 25 | 25 | 0 | 15 | 15 | 0 | 10 | 10 | 0 | 0 |
| Cause_Participation | 76 | 3 | 25 | 22 | 55 | 15 | 0 | 18 | 10 | 0 | 22 |
| Cause_and_Effect | 88 | 7 | 25 | 18 | 71 | 15 | 0 | 10 | 10 | 0 | 18 |
| Change_of_State | 50 | 25 | 25 | 0 | 15 | 15 | 0 | 10 | 10 | 0 | 0 |
| Charge | 50 | 19 | 25 | 6 | 16 | 15 | 0 | 15 | 10 | 0 | 6 |
| Collective | 66 | 0 | 25 | 25 | 66 | 15 | 0 | 0 | 10 | 10 | 35 |
| Communicate | 71 | 20 | 25 | 5 | 36 | 15 | 0 | 15 | 10 | 0 | 5 |
| Concealment | 50 | 14 | 25 | 11 | 24 | 15 | 0 | 12 | 10 | 0 | 11 |
| Constrain | 71 | 1 | 25 | 24 | 65 | 15 | 0 | 5 | 10 | 5 | 29 |
| Contact | 50 | 10 | 25 | 15 | 18 | 15 | 0 | 22 | 10 | 0 | 15 |
| Counting | 58 | 12 | 25 | 13 | 46 | 15 | 0 | 0 | 10 | 10 | 23 |
| Desire | 50 | 7 | 25 | 18 | 36 | 15 | 0 | 7 | 10 | 3 | 21 |
| Discovery | 66 | 33 | 25 | 0 | 23 | 15 | 0 | 10 | 10 | 0 | 0 |
| Dynamic_Possession | 50 | 14 | 25 | 11 | 21 | 15 | 0 | 15 | 10 | 0 | 11 |
| Emission | 50 | 18 | 25 | 7 | 14 | 15 | 1 | 18 | 10 | 0 | 8 |
| Emotion_(exp. subj.) | 55 | 11 | 25 | 14 | 20 | 15 | 0 | 24 | 10 | 0 | 14 |
| Emotion_(stim. subj.) | 50 | 7 | 25 | 18 | 15 | 15 | 0 | 28 | 10 | 0 | 18 |
| Enforcement | 64 | 0 | 25 | 25 | 64 | 15 | 0 | 0 | 10 | 10 | 35 |
| Evaluation | 107 | 4 | 25 | 21 | 92 | 15 | 0 | 11 | 10 | 0 | 21 |
| Existence | 50 | 1 | 25 | 24 | 35 | 15 | 0 | 14 | 10 | 0 | 24 |
| Feeding | 65 | 0 | 25 | 25 | 30 | 15 | 0 | 35 | 10 | 0 | 25 |
| Form | 50 | 14 | 25 | 11 | 21 | 15 | 0 | 15 | 10 | 0 | 11 |
| Future_Having | 50 | 13 | 25 | 12 | 22 | 15 | 0 | 15 | 10 | 0 | 12 |
| Hurt | 50 | 13 | 25 | 12 | 24 | 15 | 0 | 13 | 10 | 0 | 12 |
| Image_Creation | 64 | 6 | 25 | 19 | 30 | 15 | 0 | 28 | 10 | 0 | 19 |
| Incremental | 50 | 14 | 25 | 11 | 16 | 15 | 0 | 20 | 10 | 0 | 11 |
| Induction | 50 | 19 | 25 | 6 | 17 | 15 | 0 | 14 | 10 | 0 | 6 |
| Ingestion | 73 | 1 | 25 | 24 | 59 | 15 | 0 | 13 | 10 | 0 | 24 |
| Intention | 177 | 24 | 25 | 1 | 81 | 15 | 0 | 72 | 10 | 0 | 1 |
| Joint_Statement | 93 | 0 | 25 | 25 | 76 | 15 | 0 | 17 | 10 | 0 | 25 |
| Learning | 63 | 41 | 25 | 0 | 15 | 15 | 0 | 7 | 10 | 3 | 3 |
| Limitation | 50 | 5 | 25 | 20 | 31 | 15 | 0 | 14 | 10 | 0 | 20 |
| Location | 50 | 17 | 25 | 8 | 17 | 15 | 0 | 16 | 10 | 0 | 8 |
| Manipulation | 50 | 36 | 25 | 0 | 12 | 15 | 3 | 2 | 10 | 8 | 11 |
| Measurement | 60 | 16 | 25 | 9 | 28 | 15 | 0 | 16 | 10 | 0 | 9 |
| Membership | 77 | 4 | 25 | 21 | 63 | 15 | 0 | 10 | 10 | 0 | 21 |
| Motion | 62 | 30 | 25 | 0 | 11 | 15 | 4 | 21 | 10 | 0 | 4 |
| Participation | 50 | 5 | 25 | 20 | 30 | 15 | 0 | 15 | 10 | 0 | 20 |
| Payment | 71 | 0 | 25 | 25 | 71 | 15 | 0 | 0 | 10 | 10 | 35 |
| Perception_(exp._subj.) | 71 | 20 | 25 | 5 | 35 | 15 | 0 | 16 | 10 | 0 | 5 |
| Perception_(stim._subj.) | 50 | 13 | 25 | 12 | 20 | 15 | 0 | 17 | 10 | 0 | 12 |
| Pick_Up_and_Drop_Off | 50 | 12 | 25 | 13 | 27 | 15 | 0 | 11 | 10 | 0 | 13 |
| Possession | 92 | 2 | 25 | 23 | 80 | 15 | 0 | 10 | 10 | 0 | 23 |
| Protection | 61 | 0 | 25 | 25 | 53 | 15 | 0 | 8 | 10 | 2 | 27 |
| Pursuit | 50 | 8 | 25 | 17 | 29 | 15 | 0 | 13 | 10 | 0 | 17 |
| Reciprocal | 64 | 2 | 25 | 23 | 47 | 15 | 0 | 15 | 10 | 0 | 23 |
| Replacement | 52 | 0 | 25 | 25 | 42 | 15 | 0 | 10 | 10 | 0 | 25 |
| Request | 85 | 43 | 25 | 0 | 11 | 15 | 4 | 31 | 10 | 0 | 4 |
| Response | 70 | 0 | 25 | 25 | 60 | 15 | 0 | 10 | 10 | 0 | 25 |
| Selling | 50 | 10 | 25 | 15 | 26 | 15 | 0 | 14 | 10 | 0 | 15 |
| Sending | 69 | 15 | 25 | 10 | 31 | 15 | 0 | 23 | 10 | 0 | 10 |
| Statement | 73 | 0 | 25 | 25 | 55 | 15 | 0 | 18 | 10 | 0 | 25 |
| Throwing | 51 | 0 | 25 | 25 | 41 | 15 | 0 | 10 | 10 | 0 | 25 |
| Transfer_of_Possession | 50 | 9 | 25 | 16 | 27 | 15 | 0 | 14 | 10 | 0 | 16 |
| Vehicular_Motion | 74 | 29 | 25 | 0 | 34 | 15 | 0 | 11 | 10 | 0 | 0 |

**Situations already balanced:** Cause_Membership, Change_of_State, Discovery, Vehicular_Motion (4 total)

**T1 deficit:**
Collective(-25), Enforcement(-25), Feeding(-25), Joint_Statement(-25), Payment(-25), Protection(-25), Replacement(-25), Response(-25), Statement(-25), Throwing(-25), Constrain(-24), Existence(-24), Ingestion(-24), Possession(-23), Reciprocal(-23), Cause_Participation(-22), Evaluation(-21), Membership(-21), Limitation(-20), Participation(-20)

**T2 deficit:**
Motion(-4), Request(-4), Manipulation(-3), Cause_Change_of_State(-2), Emission(-1)

**T3 deficit:**
Collective(-10), Counting(-10), Enforcement(-10), Payment(-10), Manipulation(-8), Capacity(-7), Constrain(-5), Desire(-3), Learning(-3), Aggression(-2), Protection(-2)
