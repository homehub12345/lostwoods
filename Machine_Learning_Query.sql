/* Query Generates the CSV table for use with the Python script*/
SELECT  
	 tbl.u_id
			, tbl.o_id
			, crh.ThirtyDaysLate
			, crh.SixtyDaysLate
			, crh.NinetyDaysLate
			, crh.PaymentPattern
			, crh.PaymentPatternStartDate
			, crh.AccountOpenedDate
			, crh.AccountClosedDate
			, crh.AccountReportedDate
			, crh.LastActivityDate
			, crh.AccountStatusDate
			, crh.AccountOwnershipType
			, crh.AccountStatus
			, crh.AccountType
			, crh.BusinessType
			, crh.LoanType
			, crh.MonthsReviewed
			, crh.CreditLimit
			, crh.HighestBalanceAmount
			, crh.MonthlyPayment
			, crh.UnpaidBalance
			, crh.TermsDescription
			, crh.TermsMonthsCount
			, crh.CurrentRatingCode
			, crh.CurrentRatingType
			, crh.HighestAdverseCode
			, crh.HighestAdverseDate
			, crh.HighestAdverseType
			, crh.RecentAdverseCode
			, crh.RecentAdverseDate
			, crh.RecentAdverseType
			, crh.PriorAdverseCode
			, crh.PriorAdverseDate
			, crh.PriorAdverseType 

	

		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), cs.Score)
					FROM RawData.dbo.ArCreditScore cs
					WHERE (crh.ArReportId=cs.ArReportId) AND (cs.ArScoreId = 'SCORE01')
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS CreditScoreOne


	


		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), asf.ReasonCode)
					FROM RawData.dbo.ArScoreFactor asf
					WHERE (asf.ArReportId=crh.ArReportId) AND (asf.ArScoreId = 'SCORE01')
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS ReasonCodes11

			, 0 as ReasonCodes12
			, 0 as ReasonCodes13
			, 0 as ReasonCodes14

		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), cs.Score)
					FROM RawData.dbo.ArCreditScore cs
					WHERE (crh.ArReportId=cs.ArReportId) AND (cs.ArScoreId = 'SCORE02')
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS CreditScoreTwo

		


		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), asf.ReasonCode)
					FROM RawData.dbo.ArScoreFactor asf
					WHERE (asf.ArReportId=crh.ArReportId) AND (asf.ArScoreId = 'SCORE02')
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS ReasonCodesTwo

				, 0 as ReasonCodes22
			, 0 as ReasonCodes23
			, 0 as ReasonCodes24
		



		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), ai.InquiryDate)
					FROM RawData.dbo.ArInquiry ai
					WHERE (ai.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS InquiryDates_AVG

		, 0 as InquiryDates_MED

		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), MIN(ai.InquiryDate))
					FROM RawData.dbo.ArInquiry ai
					WHERE (ai.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS InquiryDatesLow


		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), MAX(ai.InquiryDate))
					FROM RawData.dbo.ArInquiry ai
					WHERE (ai.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS InquiryDatesHigh


		, STUFF(
				(SELECT ' ' + CONVERT(varchar(16), COUNT(ai.InquiryDate))
					FROM RawData.dbo.ArInquiry ai
					WHERE (ai.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS InquiryDatesNum







		, STUFF(
				(SELECT CONVERT(varchar(16),ae.CurrentEmployer)
					FROM RawData.dbo.ArEmployer ae
					WHERE (ae.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS NumberOfCurrentEmployers
				
		, STUFF(
				(SELECT CONVERT(varchar(16),ae.SelfEmployed)
					FROM RawData.dbo.ArEmployer ae
					WHERE (ae.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS NumberOfSelfEmployment 

			, STUFF(
				(SELECT CONVERT(varchar(16),r.CurrentResidence)
					FROM RawData.dbo.ArResidence r
					WHERE (r.ArReportId=crh.ArReportId) 
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS CurrentlyAtResidence
				

			, STUFF(
					(SELECT '_' + CONVERT(varchar(16),pr.FiledDate)
						+ ': ' + CONVERT(varchar(16),pr.RecordTypeOther)
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					ORDER BY pr.FiledDate DESC, pr.SettledDate DESC, pr.ReportedDate DESC
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS CriminalRecords1

			, STUFF(
					(SELECT '_' + CONVERT(varchar(16),pr.DispositionType)
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					ORDER BY pr.FiledDate, pr.SettledDate, pr.ReportedDate DESC
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS DispositionType1

			, 'NULL' as CR2
			, 'NULL' as DT2
			, 'NULL' as CR3
			, 'NULL' as DT3
			, 'NULL' as CR4
			, 'NULL' as DT4
			, 'NULL' as CR5
			, 'NULL' as DT5
			, 'NULL' as CR6
			, 'NULL' as DT6
			, 'NULL' as CR7
			, 'NULL' as DT7
			, 'NULL' as CR8
			, 'NULL' as DT8



			, STUFF(
					(SELECT ' ' + CONVERT(varchar(16),MAX(pr.ReportedDate))
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS MostRecentCriminalDate


			, STUFF(
					(SELECT ' ' + CONVERT(varchar(16),SUM(pr.LegalObligationAmount))
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS TotalFees


			, STUFF(
					(SELECT '_' + CONVERT(varchar(16),pr.CrimTypeSourceCode)
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS CSC1
			, 'NULL' as CSC2
			, 'NULL' as CSC3
			, 'NULL' as CSC4
			, 'NULL' as CSC5
			, 'NULL' as CSC6
			, 'NULL' as CSC7
			, 'NULL' as CSC8


			, STUFF(
					(SELECT ' ' + CONVERT(varchar(16),pr.TypeOfOffense)
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS Listof_TypeofOffense


		  , STUFF(
					(SELECT ' ' + CONVERT(varchar(16),COUNT(pr.TypeOfOffense))
					FROM RawData.dbo.ArPublicRecord pr
					WHERE (pr.ArReportId=crh.ArReportId)
					FOR XML PATH(''))
				, 1
				, 1
				, ''
				) AS Num_TypeofOffense
		 
		 
				

FROM 
	 RawData.dbo.ArContact ar 
	 JOIN RawData.dbo.ArCreditHistory crh ON ar.ArReportId = crh.ArReportId
	 JOIN 
	     (SELECT a.UserId as u_id, a.OperationStatusId as o_id, a.SalesforceContactId as s_id
		  FROM AdHoc.dbo.MC_SfContact_AppStatus a
		  /*WHERE a.OperationStatusID IN (224, 225, 231, 232)*/
		  GROUP BY a.SalesforceContactId, a.UserId, a.OperationStatusId
		  ) tbl
		  ON Left(s_id,15) /*AdHoc.dbo.MC_SfContact_AppStatus.SalesForceContactId*/ COLLATE DATABASE_DEFAULT = Left(ar.SalesforceContactId,15)
		  WHERE tbl.o_ID IN (213, 215, 216, 217, 218, 231, 236, 232, 234, 235, 236, 224, 225)
		  /* Example categorization into categories of good, bad, and neutral Operation Status IDs included below: */
		  /* GOOD: 213, 215, 216, 217, 218,	231, 236					*/
		  /* BAD: 232, 234, 235. 236.						*/
		  /* NEUT: 224, 225						*/
		
	ORDER BY tbl.o_id