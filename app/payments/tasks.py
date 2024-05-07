# tasks.py
from celery import shared_task
from django.core.files.base import ContentFile

from app.orders.models import Order
from app.utils.helpers import generate_invoice_pdf


@shared_task
def generate_and_store_invoice_pdf(order, razorpay_invoice_details):
    pdf_content = generate_invoice_pdf(razorpay_invoice_details)
    # Store the PDF in a file storage system
    invoice_filename = f"Order_{order.id}_Invoice.pdf"
    order.invoice_file.save(invoice_filename, ContentFile(pdf_content))
    order.save()
