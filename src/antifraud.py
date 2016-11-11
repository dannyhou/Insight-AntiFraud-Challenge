# The following program reads csv files and establishes 
import csv
# Import pandas to import csv files
# Using pandas because it's currently the only way for me to multiple rows
import pandas as pd
accountMax = 0
# Import csv file of past transactions
pastDF = pd.read_csv("digital-wallet-master/paymo_input/batch_payment.txt", delimiter=',', usecols=(1,2), lineterminator='\n')
# Convert to list to save processing time
pastList = pastDF.values.tolist()
# Get the maximum index
accountMax = 0
for row in pastList:
    if row[0] > accountMax:
        accountMax = row[0]
    if row[1] > accountMax:
        accountMax = row[1]
# Construct transaction overview
# This list will be the same number of accounts in the system
# where the index is the account number, and the list at each index will
# have all of the account numbers that the current account has done
# transactions with
transactionList1 = [[] for _ in range(accountMax+1)]
for row in pastList:
    # Add transaction to list but avoid duplicates
    if row[1] not in transactionList1[row[0]]:
        transactionList1[row[0]].append(row[1])
    if row[0] not in transactionList1[row[1]]:
        transactionList1[row[1]].append(row[0])
# Generate csv file with transactionList1
#myfile = open('transactionList1.txt', 'wb')
#writer = csv.writer(myfile)
#writer.writerow(transactionList1)

# Build output list
# Import csv file of future transactions
futureDF = pd.read_csv("digital-wallet-master/paymo_input/stream_payment.txt", delimiter=',', usecols=(1,2), lineterminator='\n')
# Convert to list to save processing time
futureList = futureDF.values.tolist()
# Write feature 1 output file
with open('digital-wallet-master/paymo_output/output1.txt', 'wb') as out1:
    writer = csv.writer(out1)
    for row in futureList:
        # row[0] is id1 from csv file
        # Check to see if the current account is part of the records
        # If not, the transaction is unverified
        if row[0] > accountMax:
            writer.writerow(["unverified"])
        # row[1] is id2 from csv file
        elif row[1] > accountMax:
            writer.writerow(["unverified"])
        # Check if id2 is part of id1's list
        elif row[1] in transactionList1[row[0]]:
            writer.writerow(["trusted"])
        # Check if id1 is part of id2's list
        elif row[0] in transactionList1[row[1]]:
            writer.writerow(["trusted"])
        # If no condition is true, then the transaction is
        # automatically unverified
        else:
            writer.writerow(["unverified"])
print('Feature 1 finished!')

# Write feature 2 output file
with open('digital-wallet-master/paymo_output/output2.txt', 'wb') as out2:
    writer = csv.writer(out2)
    for row in futureList:
        # row[0] is id1 from csv file
        # Check to see if the current account is part of the records
        # If not, the transaction is unverified
        if row[0] > accountMax:
            writer.writerow(["unverified"])
        # row[1] is id2 from csv file
        elif row[1] > accountMax:
            writer.writerow(["unverified"])
        # Check if id2 is part of id1's list
        elif row[1] in transactionList1[row[0]]:
            writer.writerow(["trusted"])
        # Check if id1 is part of id2's list
        elif row[0] in transactionList1[row[1]]:
            writer.writerow(["trusted"])
        # Unique to feature 2:
        # Compare the two account numbers and see if they have a common
        # account number that both have done transactions with
        elif list(set(transactionList1[row[0]]) & set(transactionList1[row[1]])):
            writer.writerow(["trusted"])
        else:
        # If no condition is true, then the transaction is
        # automatically unverified
            writer.writerow(["unverified"])
print('Feature 2 finished!')

# Write feature 3 output file
# For feature 3, we will construct a new transaction list
# Where we add all second degree connections to each account's list
# To do this, we run a double for loop, where the outer loop runs through
# every account in the list, and the inner loop through each item in
# every account's transaction list

# Create new list, a copy of the original
transactionList2 = [x[:] for x in transactionList1]
# Dummy  index variable
index = 0
# Outer for loop gets every transaction list from list 1
for items in transactionList1:
    # For each account number in the transaction list, we
    # append that account's list to the index account
    for account in items:
        transactionList2[index].extend(transactionList1[account])
    index = index+1
# Generate csv file for feature 3
with open('digital-wallet-master/paymo_output/output3.txt', 'wb') as out3:
    writer = csv.writer(out3)
    for row in futureList:
        # row[0] is id1 from csv file
        # Check to see if the current account is part of the records
        # If not, the transaction is unverified
        if row[0] > accountMax:
            writer.writerow(["unverified"])
        # row[1] is id2 from csv file
        elif row[1] > accountMax:
            writer.writerow(["unverified"])
        # Check if id2 is part of id1's list
        elif row[1] in transactionList2[row[0]]:
            writer.writerow(["trusted"])
        # Check if id1 is part of id2's list
        elif row[0] in transactionList2[row[1]]:
            writer.writerow(["trusted"])
        # Compare fourth degree connections
        elif list(set(transactionList2[row[0]]) & set(transactionList2[row[1]])):
            writer.writerow(["trusted"])
        else:
        # If no condition is true, then the transaction is
        # automatically unverified
            writer.writerow(["unverified"])
print('Feature 3 finished!')
