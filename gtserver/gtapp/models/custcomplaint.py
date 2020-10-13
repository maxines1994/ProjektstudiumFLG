from django.db import models
from . import Complaint

"""
This model contains some general information about Complaints from Customers.
The fields are inherited from the abstract Complaint-class.
"""

class CustComplaint(Complaint):
    pass