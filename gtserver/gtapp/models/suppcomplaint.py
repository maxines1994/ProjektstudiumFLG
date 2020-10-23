from django.db import models
from .complaint import Complaint

class SuppComplaint(Complaint):
    """
    This model contains some general information about Complaints towards Suppliers.
    The fields are inherited from the abstract Complaint-class.
    """
    
    pass