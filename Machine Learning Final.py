###############################################################################
#                                                                             #
#                                                                             #
#                      Importing       Libraries                              #
#                                                                             #
#             REQUIRED: CSV, SciPy, Sklearn, Numpy (Easiest to just           #
#                  download Anaconda distribution)                            #
###############################################################################

import csv                            #Necessary for reading from data table.
import numpy, scipy;                  #Required for proper use of sk-learn
import sklearn;                       #Machine Learning Library
import datetime;                      #Good for data processing / getting dates
import time;                          #Good for data processing
from sklearn import preprocessing     #Allows quick conversion of strings to
                                      #integers.
from sklearn.ensemble import RandomForestClassifier     
                                      #Required to run Random Forest.





###############################################################################
#                                                                             #
#                                                                             #
#                      Data       Processing                                  #
#                                                                             #
#             Note: for RandomForest, all data must be a float                #
#                                                                             #
###############################################################################

# Getting data from CSV:
csvfile = open('C:/Users/jriggs/Documents/Forest_FINAL_t2.csv', 'rb');
r = csv.reader(csvfile, delimiter=',')
lst = [rw for rw in r][0:]

#Transposing list to improve ease of SKLearn preprocessing
#(Casting to Numpy Array and indexing by columns is an 
#alternative strategy)
lst2 = [list(t) for t in zip(*lst)]

#Identifying Column Names (Good for Indexing into CSV):
col = {"UserId":0, "OId":1, "ThirtyDaysLate":2, "SixtyDaysLate":3, "NinetyDaysLate":4,
       "PaymentPattern":5, "PaymentPatternStartDate":6, "AccountOpenedDate":7,
       "AccountClosedDate":8, "AccountReportedDate":9, "LastActivityDate":10,
       "AccountStatusDate":11, "AccountOwnershipType":12, "AccountStatus": 13,
       "AccountType":14, "BusinessType":15, "LoanType":16, "MonthsReviewed":17,
       "CreditLimit":18, "HighestBalanceAmount":19, "MonthlyPayment":20, 
       "UnpaidBalance":21, "TermsDescription":22, "TermsMonthsCount":23, 
       "CurrentRatingCode":24, "CurrentRatingType":25, "HighestAdverseCode":26,
       "HighestAdverseDate":27, "HighestAdverseType":28, "RecentADverseCode":29,
       "RecentAdverseDate":30, "RecentAdverseType":31, "PriorAdverseCode":32, "PriorAdverseDate":33, "PriorAdverseType":34,
       "CreditScoreOne":35, "Reason1-1":36, "Reason1-2":37, "Reason1-3":38, "Reason1-4":39,
       "CreditScoreTwo":40, "Reason2-1":41, "Reason2-2":42, "Reason2-3":43, "Reason2-4":44,
       "InquiryDates_AVG":45, "InquiryDates_MED":46, "InquiryDatesLow":47, "InquiryDatesHigh":48,
       "InquiryDatesNum":49, "NumberOfCurrentEmployers":50, "NumberofSelfEmployment":51, "CurrentlyAtResidence":52,
       "CriminalRecords1":53, "DispositionType1":54, "CR2":55, "DT2":56, "CR3":57, "DT3":58, "CR4":59, "DT4":60, "CR5":61,
       "DT5":62, "CR6":63, "DT6":64, "CR7":65, "DT7":66, "CR8":67, "DT8":68, "MostRecentCriminalDate":69, "TotalFees":70,
       "CSC1":71, "CSC2":72, "CSC3":73, "CSC4":74, "CSC5":75, "CSC6":76, "CSC7":77, "CSC8":78, "Listof_TypeofOffense":79, 
       "Num_TypeofOffense":80}
       
#Identifying Different Operation Status IDs
_o_i_d = {"Prequalification succeed":213, "Qualification":215, "Documents":216, 
          "Payment":217, "Confirmation":218, "Paid Applicant":221, 
          "Background Check in Progress":222, "AutoCheck Completed":223,
          "Conditional Approval":224, "Contingent Approval":225, 
          "Missing Documents":226, "Approved Resident":231, "Denied":232,
          "NLI (No Longer Interested":233, "Disqualified":234, 
           "Insufficient Income":235, "FaultyApplication":236, "Dormant":237,
           "Unknown":261} 
       
       
       
###############################################################################
#                                                                             #
#             Functions for Data Processing                                   #       
#                                                                             #
###############################################################################       
       
       
# date_conv: Takes a list of columns and for each element of a column, converts
# the string of this element into a value in seconds since 1910
def date_conv(column_list):
    for i in column_list:
        date_acc = 0;
        for j in lst2[col[i]]:
            tmp_b = 0;
            if ((j != 'NULL') & (j != '')):
                l = [int(a) for a in j.split('-')]
                tmp_b = time.mktime( (datetime.datetime(l[0], l[1], l[2]) +datetime.timedelta(seconds=((365.25)*(24)*(60)*(60)*(60)))).timetuple())
                lst2[col[i]][date_acc] = float(tmp_b);
            else:
                lst2[col[i]][date_acc] = 'NULL'
            date_acc = date_acc + 1;
            
#Takes a string input and returns a float or a 'NULL' based on whether or not
# useful data is contained within the string:
#
#       unknown: the string being evaluated
#       
#
#                   / if 0 =============> Returns actual value
#       _count: ---- 
#                   \ if NOT 0 =============> Returns sum of digits
#######################################################
def int_conv(unknown, _count):
    if (unknown == ''):
        return 'NULL';
    if (unknown[0] == '\xef'):
        unknown = unknown[3:]
    if (unknown == ''):
        return 'NULL';
    if (unknown == 'NULL'):
        return 'NULL';
    else:
        tmp = float(unknown)
        #tmp = int(unknown,base)
        #if (is_int):
        #    tmp = int(unknown, base)
        if (_count):
            #The below line is only useful for calculating # of 1s in a binary string
            # generalizing the implementation may require its removal. 
            tmp = sum([int(a) for a in unknown])       
#        else:
#            tmp = unknown
        return float(tmp)
        
        
        
        
#takes a single cell containing multiple elements of information:
#           ie) [element1][char][element2][char][element3] in one cell
#       and moves the first few elements up until the len_ element
#       elements to subsequent cells seperated from the original
#       cell by a factor of "mult"
#        
#       For example: [element1]_[element2]_[element3] | EmptyCell --> [element_1]  | [element_2]
#
#       via a call of folding_func([i st col[i] is the column containing [element1]_[element2]], 1, '_', 2)
#
#      NO
#########################################################################################
def folding_func(i, mult, char, len_):
    temp = [(['0','0','0','0'],sub_lst.split(char))[sub_lst != 'NULL'] for sub_lst in lst2[col[i]]]
    row_acc = 0;
    for k in temp:
        len_tot = min(len(k),len_)
        col_acc = 0;
        while(col_acc < len_tot):
            lst2[col[i]+mult*col_acc][row_acc] = k[col_acc]
            col_acc = col_acc + 1;
        row_acc = row_acc+1;
        
        
        
# Checks if unknown is a number (float or int)
#
#  if so: return 1
#    if not: return 0
###############################################        
def t_f(unknown):
    if (isinstance(unknown, int)):
        return 1;
    elif (isinstance(unknown, float)):
        return 1;
    else:
        return 0;


#
#     float_s:
#           takes a "thing" and an "avg" you desire to replace it with
#           when "thing" is not a float value
#           
#           This is used to eliminate missing or 'NULL' values in the
#           script.
#################################################
def float_s(thing, avg):
    if (t_f(thing)):
        return float(a)
    else:
        return temp_avg

###############################################################################
#                                                                             #
#                     Basic Data Processing                                   #       
#                                                                             #
###############################################################################


#Step 1: Split columns containing multiple values 

folding_func("Reason1-1", 1, ' ', 4)
folding_func("Reason2-1", 1, ' ', 4)
folding_func("CriminalRecords1", 2, '_', 8)
folding_func("DispositionType1", 2, '_', 8)
folding_func("CSC1", 1, '_', 8)

#Step 2: Deal with computations involving columns containing multiple values; 
# In particular, those that you do not wish to be represented in the larger 
# data set in their raw form.

#Example: InquiryDates_AVG is a column containing all inquiry dates of a
#         customer.  The code below takes this long list, and applies basic
#         operations on it to calculate both the average and median of this
#         list.  The average goes back into InquiryDates_AVG while the median
#         is moved into the subsequent column.

        
folding3 = ["InquiryDates_AVG"]
date_acc = 0;
for k in lst2[col[folding3[0]]]:
    tmp_a = 0;
    tmp_b = 0;
    tmp_c = []
    if (k != 'NULL'):
        for j in k.split(' '):
           l = [int(a) for a in j.split('-')]
           tmp_c = tmp_c + [time.mktime(datetime.datetime(l[0], l[1], l[2]).timetuple())]
        l_l = len(tmp_c)
        l_2 = (l_l)/2
        tmp_c_sorted = sorted(tmp_c)
        tmp_a = ((tmp_c_sorted[l_2] + tmp_c_sorted[l_2-1])/2, tmp_c[(l_l-1)/2] )[l_l % 2]
        tmp_b = (sum(tmp_c))/(l_l)
    lst2[col[folding3[0]]][date_acc] = tmp_b;  
    lst2[col[folding3[0]] + 1][date_acc] = tmp_a;  
    date_acc = date_acc + 1;


# Step 3: Convert Dates to Float Values:

date_change = ["AccountOpenedDate", "AccountClosedDate", "AccountReportedDate", "LastActivityDate",
                "AccountStatusDate", "PaymentPatternStartDate",
               "HighestAdverseDate", "RecentAdverseDate", "PriorAdverseDate", "InquiryDatesLow", 
               "InquiryDatesHigh", "MostRecentCriminalDate"]
date_conv(date_change)

#  Step 4: Convert labels to numbers.  If using SK-Learn Preprocessing it is 
#          VERY important that you are inputting complete columns when engaging
#          in these operations.
#

#               STEP 4A: List what you want to be processed.
codify_list = ["PaymentPattern", "AccountOwnershipType", "AccountStatus", "AccountType", "BusinessType", "PriorAdverseType",
               "HighestAdverseCode", "HighestAdverseType", "RecentADverseCode", "RecentAdverseType", "PriorAdverseCode",
               "LoanType", "TermsDescription", "CurrentRatingCode", "CurrentRatingType", "CriminalRecords1", "DispositionType1",
               "CR2", "DT2", "CR3", "DT3", "CR4", "DT4", "CR5", "DT5", "CR6", "DT6", "CR7", "DT7", "CR8", "LoanType",
               "DT8", "CSC1", "CSC2", "CSC3", "CSC4", "CSC5", "CSC6", "CSC7", "CSC8", "Listof_TypeofOffense"]
               
               
#               STEP 4B: Process the data that was listed!
number = preprocessing.LabelEncoder()
for i in codify_list: 
    tmp = number.fit_transform(lst2[col[i]]);
    tmp2 = [int(a) for a in tmp]
    lst2[col[i]] = tmp2;
    

# Step 5: Process columns containing integer data.  Conversion here is simpler,
# but 'NULL' values need to be accounted for.  For now 'NULL' values are not 
# converted but remain 'NULL'.  This is managed by the int_conv function.
# 
#
    
#Currently at residence has unique representation in my data table as a binary
#string, so is handled differently.
tmp = [int_conv(i,1) for i in lst2[col["CurrentlyAtResidence"]]]
lst2[col["CurrentlyAtResidence"]] = tmp

#The other ints are handled pretty normally.
int_lst = ["UserId", "OId", "ThirtyDaysLate", "SixtyDaysLate", "NinetyDaysLate", "CreditLimit", "HighestBalanceAmount", 
           "MonthlyPayment", "UnpaidBalance", "CreditScoreOne", "Reason1-1", "Reason1-2", "Reason1-3",
           "Reason1-4", "CreditScoreTwo", "Reason2-1", "Reason2-2", "Reason2-3", "Reason2-4", "NumberOfCurrentEmployers",
           "NumberofSelfEmployment", "InquiryDatesNum", "Num_TypeofOffense", "TotalFees", "TermsMonthsCount", "MonthsReviewed"]
for i in int_lst:
    #originally (j,10,0) below
    tmp = [int_conv(j,0) for j in lst2[col[i]]]
    lst2[col[i]] = tmp
    
    
    
        
# Step 6: Replace NULL values with the average values for that column.        
for i in col:
    l_temp = lst2[col[i]]
    fltrd = filter(t_f, l_temp)
    temp_avg = sum(fltrd)/(len(fltrd))
    temp_new = [float_s(a, temp_avg) for a in l_temp]
    lst2[col[i]] = temp_new


# Step 7: Transpose the table once again to return it to its original format.
lst_fin = [list(t) for t in zip(*lst2)]


#########################################################
#                                                       #
#                                                       #
#                                                       #
############   More Data Processing:      ####################
##########   Collapsing Multiple Rows   ##################
#                                                       #
#                                                       #
#                                                       #
#########################################################

# Convert (almost entirely) processed data into a Numpy Array
a = numpy.array(lst_fin)

#Construct Unique List of User IDs:
ls = numpy.unique(a[:,0])

# bad_list: the list of values for operation status ID that signify a negative response.
#oids for this will be 232, 234, 235, 236
bad_list = [_o_i_d[name] for name in ["Denied", "Disqualified", "Insufficient Income", "Dormant"]]

# neut_list: the list of values for operation status ID that signify a neutral
# response.
# NOTE: It is unlikely there will be enough data points with the status IDs in 
#neut_list for points to be grouped into that category after randomforest runs.  
# NOTE: IF set to [] no neutral_categories will be attempted.
#
# Potential Choices for Neutral:
#neut_list = _o_i_d[name] for name in ["Conditional Approval" "Contingent Approval"]
#
neut_list = []


# Anything IN datatable but NOT in neut_list or bad_list: in good_list


# user_expand(relevant_list)
#      
#      Input: A list of rows in the data table that share the same user ID.
#       These rows represent different credit history records on the user's part.
#
#      Output: A single row that combines the data from up to 7 credit 
#      history records: arranged by Last Activity Date: the first two, middle
#      three, and the last two. In addition, it includes maximum and average 
#      values for several differnet types of criteria accross those records.
#       
#       IF: There are less than 7 credit history records, empty spots will be
#       filled by the medium record.
##############################################################################
def user_expand(relevant_list):
    #BELOW: Combines raw data from the 7 Credit History Records
    new_sorted = relevant_list[relevant_list[:,col["LastActivityDate"]].argsort()]
    dealing_with = len(new_sorted)
    indices_list = range(col["ThirtyDaysLate"], col["CreditScoreOne"])
    n_list = indices_list[:col["PaymentPattern"]] + indices_list[col["PaymentPattern"]+1:col["TermsDescription"]] + indices_list[col["TermsDescription"]+1:]
    left_most_half = new_sorted[:,n_list]
    mid = round(numpy.median(range(0,dealing_with)))    
    index_list = [0,1,mid-1,mid,mid+1,dealing_with-2,dealing_with-1]
    safe_index_list = [(mid,int(check))[check in range(0,dealing_with)] for check in index_list]
    correct_portion = relevant_list[[0],[0,1] + range(col["CreditScoreOne"], 81)]
    cur = correct_portion[1]
    correct_portion[1] = (2.0,0.0,1.0)[(cur in bad_list) + (cur in neut_list)]
    for i in safe_index_list:
        correct_portion = numpy.append(correct_portion, left_most_half[i])
    
    #BELOW: Calculates combined data from the 7 Credit History Records
    leng_left = len(left_most_half)
    thirty_late = sum(left_most_half[:,0]) 
    sixty_late = sum (left_most_half[:,1]) 
    ninety_late = sum(left_most_half[:,2])
    high_credit_lim_sum = sum(left_most_half[:,col["CreditLimit"]-3])
    high_credit_lim_avg = high_credit_lim_sum/float(leng_left)
    high_bal_sum =  sum(left_most_half[:,col["HighestBalanceAmount"]-3])
    high_bal_avg = high_bal_sum/float(leng_left)
    monthly_pay_sum = sum(left_most_half[:,col["MonthlyPayment"]-3])
    monthly_pay_avg = monthly_pay_sum/float(leng_left)
    terms_months_count_sum = sum(left_most_half[:,col["TermsMonthsCount"]-4])
    terms_months_count_avg = terms_months_count_sum/float(leng_left)    
    prior_adv = max(left_most_half[:,col["PriorAdverseDate"]-4])    
    high_adv = max(left_most_half[:,col["HighestAdverseDate"]-4])
    rec_adv = max(left_most_half[:,col["RecentAdverseDate"]-4])
    back_portion = numpy.array([leng_left, thirty_late, sixty_late, ninety_late, high_credit_lim_sum,
                                high_credit_lim_avg, high_bal_sum, high_bal_avg, monthly_pay_sum,
                                monthly_pay_avg, terms_months_count_sum, terms_months_count_avg,
                                prior_adv, high_adv, rec_adv])
    #Returns combined records:
    correct_portion = numpy.append(correct_portion, back_portion)
    return correct_portion
    
    

# Put data from the table into a list of lists of entries for each user so that
# the user_expand function can be applied.
tot_users = len(ls)
access_name = dict([(str(key),num) for key,num in zip(ls, range(0,tot_users))])
expand_over = 0
expand_over = []
expand_over = [[] for val in range(0,tot_users)]
for val in a:
    stor = str(float(val[0]))
    cur = []
    v = access_name[stor]
    cur = expand_over[v]
    cur.append(val)
    expand_over[v] = cur
    stor = 0

true_array = numpy.array([user_expand(numpy.array(ar)) for ar in expand_over])

###############################################################################
#                                                                             #
#                                                                             #
#                      Random       Forest                                    #
#                                                                             #
#                      (Required: Scikit-Learn)                               #
#                                                                             #
###############################################################################


# Randomly Generate the test and train data sets.
def rand_gen():
    choice = numpy.random.choice(range(0,len(true_array)), 3 * round((len(ls)+1)/5),False)
    train = true_array[choice]
    test_choice = [i for i in range(0,len(true_array)) if (i not in choice)]
    test = true_array[test_choice]
    return (test, train)
    
    
eee = rand_gen()
test = eee[0]
train = eee[1]


#Describe the classifier object.
forest = RandomForestClassifier(n_estimators = 900, oob_score = True, warm_start=False)
#Fit your training set over the classifier.
forest = forest.fit(train[0::, 2::], train[0::,1])
#Use your classifier to predict the output of the test dataset.
output = forest.predict(test[0::,2::])

# Below: Calculate the accuracy rate on your test data set.
acc_list = [(t1 == t2[1]) for t1,t2 in zip(output, test)]
good = len([q for q in acc_list if (q == True)])
total = len(acc_list)
rate = float(good)/total

#Note: Accuracy Rate on the training data set is estimated
# by the activity of fitting, and stored in: 
#
#
#                       forest.oob_score_
#
#
#


#
#   Checks for a value v1 in the output what percent of
#   outputted values are actually v2 in the test set.
#
#  Where:
#
#           0.0     =       Bad Result
#           1.0     =       Neutral Result
#           2.0     =       Good Result
#
##########################################################
def output_accuracy(v1, v2):
    acc_list_ = [((t1 == v1) and (t2[1] == v2))  for t1,t2 in zip(output, test)]
    good_ = len([q for q in acc_list_ if (q == True)])
    total_ = len([q for q in output if (q==v1)])
    return float(good_)/total_