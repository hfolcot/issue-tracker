#Choices for priority and status
CRITICAL = 'Critical'
HIGH = 'High'
MEDIUM = 'Medium'
LOW = 'Low'
PENDING = 'Pending'
INPROGRESS = 'In Progress'
FIXED = 'Fixed'
AWAITINGQUOTE = 'Awaiting Quote'
IMPLEMENTED = 'Implemented'
AWAITINGFUNDS = 'Awaiting Funds'

UNASSIGNED = 1 # ID of record in DeveloperProfile objects named 'Unassigned'

PRIORITY_CHOICES = ((CRITICAL, 'Critical'), 
	(HIGH, 'High'), 
	(MEDIUM, 'Medium'), 
	(LOW, 'Low'))

STATUS_CHOICES = ((PENDING,'Pending'),
	(INPROGRESS, 'In Progress'),
	(FIXED, 'Fixed'))

FEATURE_STATUS_CHOICES = ((AWAITINGQUOTE,'Awaiting Quote'),
	(INPROGRESS, 'In Progress'),
	(IMPLEMENTED, 'Implemented'),
	(AWAITINGFUNDS, 'Awaiting Funds'))