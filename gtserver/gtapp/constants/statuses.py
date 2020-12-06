"""
Alle Status werden hier definiert.
NICHT DIE STATUS-MIGRATION-DATEI VERAENDERN!
Aenderungen werden nur in dieser Konstanten-Datei vorgenommen und bei der naechsten
Migration von der Migration-Datei beruecksichtig.
"""

#Kunden-Status
CUSTOMER_ACTIVE                     = 'A'
CUSTOMER_INACTIVE                   = 'I'

#User-Status
USER_ACTIVE                         = 'A'
USER_INACTIVE                       = 'I'

#Auftragspositions-Status
CUSTORDERDET_BEING_ORDERED          = '8'
CUSTORDERDET_APPROVED               = 'A'
CUSTORDERDET_IN_PROGRESS            = 'B'
CUSTORDERDET_PROCESSING_COMPLETE    = 'D'
CUSTORDERDET_BEING_PRODUCED         = 'E'
CUSTORDERDET_DONE                   = 'F'
CUSTORDERDET_DELIVERED              = 'L'
CUSTORDERDET_COMPLAINED             = 'M'
CUSTORDERDET_ACCEPTED               = 'T'

#Artikel-Status
ARTICLE_ACTIVE                      = 'A'
ARTICLE_INACTIVE                    = 'I'

#Teile-Status
PART_ACTIVE                         = 'A'
PART_INACTIVE                       = 'I'

#Lieferanten-Status
SUPPLIER_ACTIVE                     = 'A'
SUPPLIER_INACTIVE                   = 'I'

#Bestellungskopf-Status
SUPPORDER_BEING_ORDERED             = '8'
SUPPORDER_ORDERED                   = 'B'
SUPPORDER_DELIVERED                 = 'L'

#Bestellpositions-Status
SUPPORDERDET_ORDERED                = 'B'
SUPPORDERDET_DELIVERED              = 'L'

#Reklamationskopf-Status
COMPLAINT_BEING_CREATED             = '8'
COMPLAINT_RECEIVED                  = 'E'
COMPLAINT_DONE                      = 'T'

#Reklamationspositions-Status
COMPLAINTDET_RECEIVED               = 'E'
COMPLAINTDET_DONE                   = 'T'

#Todo-Status
TODO_UNASSIGNED                     = '8'
TODO_ASSIGNED                       = 'A'
TODO_IN_PROGRESS                    = 'B'
TODO_DONE                           = 'T'

#Nachrichten-Status
MESSAGE_BEING_COMPOSED              = 'C'
MESSAGE_SENT                        = 'G'
MESSAGE_RECEIVED                    = 'P'
MESSAGE_READ                        = 'R'