from django.db import models


class PaymentMethod(models.IntegerChoices):
    CREDIT_CARD = 1, 'Credit Card'
    DEBIT_CARD = 2, 'Debit Card'
    NET_BANKING = 3, 'Net Banking'
    UPI = 4, 'UPI'
    RAZORPAY = 5, 'Razorpay'


class PaymentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    COMPLETED = 2, 'Completed'
    FAILED = 3, 'Failed'


class RefundType(models.IntegerChoices):
    CANCEL = 1, 'Cancel'
    RETURN = 2, 'Return'


class RazorpayWebhookEventType(models.IntegerChoices):
    PAYMENT_CAPTURED = 1, 'Payment Captured'
    PAYMENT_FAILED = 2, 'Payment Failed'
    REFUND_INITIATED = 3, 'Refund Initiated'
    REFUND_FAILED = 4, 'Refund Failed'


class ReturnStatus(models.IntegerChoices):
    REQUESTED = 1, 'Requested'
    APPROVED = 2, 'Approved'
    REJECTED = 3, 'Rejected'
    RETURNED = 4, 'Returned'


class RefundStatus(models.IntegerChoices):
    INITIATED = 1, 'Initiated'
    PROCESSED = 2, 'Processed'
    COMPLETED = 3, 'Completed'
    FAILED = 4, 'Failed'
