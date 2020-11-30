#All global status-constants will be defined in this file.
#DO NOT CHANGE THE STATUS MIGRATION FILE
#All changes made in this constants-file will automatically
#be taken into account by the existing migration file 0002_init_statuses.py.

#Customer Status
CUSTOMER_ACTIVE                     = 'A'
CUSTOMER_INACTIVE                   = 'I'

#User Status
USER_ACTIVE                         = 'A'
USER_INACTIVE                       = 'I'

#CustOrderDet Status
CUSTORDERDET_BEING_ORDERED          = '8'
CUSTORDERDET_ACCEPTED               = 'A'
CUSTORDERDET_BEING_PROCESSED        = 'B'
CUSTORDERDET_PROCESSING_COMPLETE    = 'D'
CUSTORDERDET_BEING_PRODUCED         = 'E'
CUSTORDERDET_FINISHED               = 'F'
CUSTORDERDET_DELIVERED              = 'L'
CUSTORDERDET_COMPLAINED             = 'M'
CUSTORDERDET_APPROVED               = 'T'

#Article Status
ARTICLE_ACTIVE                      = 'A'
ARTICLE_INACTIVE                    = 'I'

#Part Status
PART_ACTIVE                         = 'A'
PART_INACTIVE                       = 'I'

#Supplier Status
SUPPLIER_ACTIVE                     = 'A'
SUPPLIER_INACTIVE                   = 'I'

#SuppOrder Status
SUPPORDER_BEING_ORDERED             = '8'
SUPPORDER_ORDERED                   = 'B'
SUPPORDER_DELIVERED                 = 'L'

#SuppOrderDet Status
SUPPORDERDET_ORDERED                = 'B'
SUPPORDERDET_DELIVERED              = 'L'

#Complaint Status
COMPLAINT_BEING_CREATED             = '8'
COMPLAINT_RECEIVED                  = 'E'
COMPLAINT_DONE                      = 'T'

#ComplaintDet Status
COMPLAINTDET_RECEIVED               = 'E'
COMPLAINTDET_DONE                   = 'T'

#Todo Status
TODO_TO_BE_DONE                     = 'B'
TODO_DONE                           = 'T'

#Message Status
MESSAGE_BEING_COMPOSED              = '8'
MESSAGE_SENT                        = 'G'
MESSAGE_RECEIVED                    = 'L'
MESSAGE_READ                        = 'R'