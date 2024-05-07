import re
import uuid
from datetime import datetime
from decimal import Decimal
from urllib import request, parse
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.units import mm

from app.utils.constants import CacheKeys, SMS
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Company Details
    company_name = "Your Company Name"
    company_address_line1 = "123 Company Street"
    company_address_line2 = "City, State, Zipcode"
    company_contact = "Phone: 123-456-7890"

    # Invoice Header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30*mm, height - 30*mm, company_name)
    p.setFont("Helvetica", 10)
    p.drawString(30*mm, height - 40*mm, company_address_line1)
    p.drawString(30*mm, height - 45*mm, company_address_line2)
    p.drawString(30*mm, height - 50*mm, company_contact)

    # Add a company logo
    # p.drawImage(path_to_logo, 15*mm, height - 60*mm, width=40*mm, height=20*mm)

    # Invoice Details Header
    p.setFont("Helvetica-Bold", 10)
    p.drawString(140*mm, height - 30*mm, "Invoice")
    p.setFont("Helvetica", 9)
    p.drawString(140*mm, height - 35*mm, f"Invoice Number: {invoice['invoice_number']}")
    p.drawString(140*mm, height - 40*mm, f"Date: {datetime.utcfromtimestamp(invoice['date']).strftime('%Y-%m-%d')}")

    # Customer Details
    customer_details = invoice['customer_details']
    p.drawString(30*mm, height - 60*mm, "Bill To:")
    p.drawString(30*mm, height - 65*mm, customer_details['name'])

    billing_address = customer_details['billing_address']
    p.drawString(30*mm, height - 70*mm, billing_address['line1'])
    if billing_address.get('line2'):
        p.drawString(30*mm, height - 75*mm, billing_address['line2'])
    p.drawString(30*mm, height - 80*mm,
                 f"{billing_address['city']}, tamilNadu, {billing_address['pincode']}")

    # If shipping address exists, print it, else skip
    shipping_address = customer_details.get('shipping_address')
    shipping_address = shipping_address or billing_address
    if shipping_address:
        p.drawString(100*mm, height - 60*mm, "Ship To:")
        p.drawString(100*mm, height - 65*mm, customer_details['name'])
        p.drawString(100*mm, height - 70*mm, shipping_address['line1'])
        if shipping_address.get('line2'):
            p.drawString(100*mm, height - 75*mm, shipping_address['line2'])
        p.drawString(100*mm, height - 80*mm,
                     f"{shipping_address['city']}, tamilNadu, {shipping_address['pincode']}")

    # Invoice Line Items Header
    p.setFont("Helvetica-Bold", 9)
    p.drawString(30*mm, height - 100*mm, "Description")
    p.drawString(110*mm, height - 100*mm, "Quantity")
    p.drawString(140*mm, height - 100*mm, "Price")
    p.drawString(170*mm, height - 100*mm, "Amount")

    p.setFont("Helvetica", 9)
    y_position = height - 105*mm
    for item in invoice['line_items']:
        p.drawString(30*mm, y_position, item['name'])
        p.drawString(110*mm, y_position, str(item['quantity']))
        p.drawString(140*mm, y_position, f"{invoice['currency_symbol']}{item['unit_amount']}")
        p.drawString(170*mm, y_position, f"{invoice['currency_symbol']}{item['amount']}")
        y_position -= 5*mm

    # Invoice Summary
    p.drawString(140*mm, y_position - 10*mm, "Total:")
    p.drawString(170*mm, y_position - 10*mm, f"{invoice['currency_symbol']}{invoice['amount']}")

    # Draw a line to separate the summary section
    p.setStrokeColor(colors.black)
    p.line(30*mm, y_position - 12*mm, 180*mm, y_position - 12*mm)

    # Footer
    p.setFont("Helvetica", 8)
    footer_text = "Thank you for your business!"
    p.drawString(30*mm, 20*mm, footer_text)

    # Close the PDF object cleanly
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and return it
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# def get_data_for_field(field, locale):
#     mapping = {
#         'Designation': Designation,
#         'WeightUnit': WeightUnit,
#         'RecordType': RecordType,
#         'PlaceType': PlaceType,
#         'PayType': PayType,
#
#     }
#     translation.activate(locale)
#     enum_class = mapping.get(field)
#     data = EnumValueSerializer(enum_class.choices, many=True, context={'field': field, 'enum_class': enum_class}).data
#     data = {
#         "display_data": {
#             "name": field,
#             "name_vernacular": field,
#         },
#         "values": data
#     }
#     translation.deactivate()
#     return data


def allow_string_rep_of_enum(x):
    """Convert string representation of enum to integer."""
    return int(x) if isinstance(x, str) else x


def convert_to_list(v):
    if v is None:
        return None
    return [v] if not isinstance(v, list) else v


def convert_to_decimal(x):
    """Convert value to decimal."""
    if x is not None:
        return Decimal(x)
    return x


def trim_mobile_no(x):
    """Trim mobile number to last 10 digits if longer than 10 digits."""
    return x[-10:]


def send_sms(numbers, message):
    """Send SMS to given numbers with the specified message."""
    data = parse.urlencode({
        'apikey': settings.TEXT_LOCAL_API_KEY,
        'numbers': numbers,
        'message': message,
        'sender': settings.SMS_SENDER,
        'test': settings.DEBUG
    }).encode('utf-8')

    with request.urlopen(request.Request(SMS.TEXTLOCAL_HOST), data) as f:
        return f.read()


def qdict_to_dict(qdict):
    """Convert a QueryDict to a Python dict."""
    return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}


def get_serialized_exception(e):
    """Serialize exception data into a dictionary."""
    return {
        'error_message': str(e),
        'error_code': e.args[0] if e.args else None,
    }, None


def mobile_number_validation_check(mobile_no):
    """Validate mobile number format."""
    return (
        "Enter mobile number" if mobile_no is None else
        "Invalid mobile number" if re.match(r"\d{10}$", mobile_no) is None else
        None
    )


def generate_random_username():
    """Generate a random username based on UUID."""
    return str(uuid.uuid4()).replace("-", "")


def get_serialized_enum(enum, locale=None, field_name=None):
    """Serialize enum data into a dictionary."""
    return {
        "id": enum.value,
        "name": enum.name,
        "name_vernacular": str(enum.label),
        "icon_url": "",
    }


def format_value(value):
    if value is None:
        return "None"
    elif isinstance(value, list):
        return "~".join(map(str, sorted(value)))
    elif isinstance(value, (int, bool)):
        return str(value)
    else:
        return value


def build_cache_key(template_type: CacheKeys, **kwargs) -> str:
    """
    Centralized method to generate cache keys based on a template type and the provided keyword arguments.
    """
    formatted_args = {key: format_value(value) for key, value in kwargs.items()}
    return template_type.value.format(**formatted_args)


def build_user_filter_cache_key(
    search_queries: list[str] or None,
    organization_id: int or None,
    designation: list[int] or None,
    place_id: list[int] or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "search_queries": "~".join(search_queries) if search_queries else "None",
        "organization_id": organization_id if organization_id else "None",
        "designation": "/".join(map(str, sorted(designation))) if designation else "None",
        "place_id": "_".join(map(str, sorted(place_id))) if place_id else "None",
        "is_active": str(is_active) if is_active else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.USER_LIST.format(**args)
    return cache_key


def build_fish_filter_cache_key(
    name: str or None,
    organization_id: int or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "name": name if name else "None",
        "organization_id": organization_id if organization_id else "None",
        "is_active": str(is_active) if is_active else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.FISH_LIST.format(**args)
    return cache_key


def build_fish_variant_filter_cache_key(
    fish_id: int or None,
    name: str or None,
    organization_id: int or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "fish_id": fish_id if fish_id else "None",
        "name": name if name else "None",
        "organization_id": organization_id if organization_id else "None",
        "is_active": str(is_active) if is_active else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.FISH_VARIANT_LIST.format(**args)
    return cache_key


def build_discount_filter_cache_key(
    organization_id: int or None,
    name: str or None,
    type: int or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "type": type if type else "None",
        "name": name if name else "None",
        "organization_id": organization_id if organization_id else "None",
        "is_active": str(is_active) if is_active else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.DISCOUNT_LIST.format(**args)
    return cache_key


def build_price_history_cache_key(
    fish_id: int or None,
    fish_variant_id: int or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "fish_id": fish_id if fish_id else "None",
        "fish_variant_id": fish_variant_id if fish_variant_id else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.PRICE_HISTORY_LIST.format(**args)
    return cache_key


def build_place_filter_cache_key(
    organization_id: int or None,
    name: str or None,
    type: int or None,
    is_active: bool or None,
    center_id: int or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "organization_id": organization_id if organization_id else "None",
        "name": name if name else "None",
        "type": type if type else "None",
        "is_active": str(is_active) if is_active else "None",
        "center_id": center_id if center_id else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.PLACE_LIST.format(**args)
    return cache_key


def build_organization_filter_cache_key(
    name: str or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "name": name if name else "None",
        "is_active": str(is_active) if is_active else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.ORGANIZATION_LIST.format(**args)
    return cache_key


def build_record_filter_cache_key(
    organization_id: int or None,
    user_id: int or None,
    import_from_id: int or None,
    export_to_id: int or None,
    record_type: int or None,
    discount_id: int or None,
    fish_variant_id: int or None,
    weigh_place_id: int or None,
    is_SP: bool or None,
    is_active: bool or None,
    start_time: str or None,
    end_time: str or None,
    ordering: str or None,
    page: int or None,
    locale: str,
):
    args = {
        "organization_id": str(organization_id) if organization_id is not None else "None",
        "user_id": str(user_id) if user_id is not None else "None",
        "import_from_id": str(import_from_id) if import_from_id is not None else "None",
        "export_to_id": str(export_to_id) if export_to_id is not None else "None",
        "record_type": str(record_type) if record_type is not None else "None",
        "discount_id": str(discount_id) if discount_id is not None else "None",
        "fish_variant_id": str(fish_variant_id) if fish_variant_id is not None else "None",
        "weigh_place_id": str(weigh_place_id) if weigh_place_id is not None else "None",
        "is_SP": str(is_SP) if is_SP is not None else "None",
        "is_active": str(is_active) if is_active is not None else "None",
        "start_time": start_time if start_time is not None else "None",
        "end_time": end_time if end_time is not None else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page is not None else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.RECORD_LIST.format(**args)
    return cache_key


def build_expense_filter_cache_key(
    organization_id: int or None,
    user_id: int or None,
    type_id: int or None,
    desc: str or None,
    start_time: str or None,
    end_time: str or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "organization_id": organization_id if organization_id else "None",
        "user_id": user_id if user_id else "None",
        "type_id": type_id if type_id else "None",
        "desc": desc if desc else "None",
        "start_time": start_time if start_time else "None",
        "end_time": end_time if end_time else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.EXPENSE_LIST.format(**args)
    return cache_key


def build_expense_type_filter_cache_key(
    name: str or None,
    organization_id: int or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "name": name if name else "None",
        "organization_id": organization_id if organization_id else "None",
        "is_active": str(is_active) if is_active else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.EXPENSE_TYPE_LIST.format(**args)
    return cache_key


def build_bill_filter_cache_key(
    organization_id: int or None,
    user_id: int or None,
    bill_place_id: int or None,
    discount_id: int or None,
    pay_type: int or None,
    is_active: bool or None,
    start_time: str or None,
    end_time: str or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "organization_id": organization_id if organization_id else "None",
        "user_id": user_id if user_id else "None",
        "bill_place_id": bill_place_id if bill_place_id else "None",
        "discount_id": discount_id if discount_id else "None",
        "pay_type": str(pay_type) if pay_type else "None",
        "is_active": str(is_active) if is_active is not None else "None",
        "start_time": start_time if start_time else "None",
        "end_time": end_time if end_time else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.BILL_LIST.format(**args)
    return cache_key


def build_bill_item_filter_cache_key(
    bill_id: int or None,
    fish_variant_id: int or None,
    is_SP: bool or None,
    is_active: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "bill_id": bill_id if bill_id else "None",
        "fish_variant_id": fish_variant_id if fish_variant_id else "None",
        "is_SP": str(is_SP) if is_SP is not None else "None",
        "is_active": str(is_active) if is_active is not None else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.BILL_ITEM_LIST.format(**args)
    return cache_key


def build_stock_filter_cache_key(
    organization_id: int or None,
    place_id: int or None,
    fish_variant_id: int or None,
    is_SP: bool or None,
    ordering: str or None,
    page: int or None,
    locale,
):
    args = {
        "organization_id": organization_id if organization_id else "None",
        "place_id": place_id if place_id else "None",
        "fish_variant_id": fish_variant_id if fish_variant_id else "None",
        "is_SP": str(is_SP) if is_SP is not None else "None",
        "ordering": ordering if ordering else "None",
        "page": str(page) if page else "None",
        "locale": locale,
    }

    cache_key = CacheKeys.STOCK_LIST.value.format(**args)
    return cache_key
