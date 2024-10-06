# from django.db.models import Sum
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.utils import timezone
# from datetime import timedelta
# from order.models import Order
# from customer.models import Customer
# from decimal import Decimal
#
#
# @api_view(['GET'])
# def dashboard_stats(request):
#
#     # Get current time
#     current_time = timezone.now()
#
#     # Sales and order data
#     first_day_of_month = current_time.replace(day=1)
#     sales_this_month = Order.objects.filter(created_at__gte=first_day_of_month).aggregate(
#         total_sales=Sum('grand_total'))['total_sales'] or Decimal('0')
#
#     start_of_today = current_time.replace(hour=0, minute=0, second=0)
#     sales_today = Order.objects.filter(created_at__gte=start_of_today).aggregate(
#         total_sales=Sum('grand_total'))['total_sales'] or Decimal('0')
#
#     orders_today = Order.objects.filter(created_at__gte=start_of_today).count()
#
#     new_customers = Customer.objects.filter(created__gte=first_day_of_month).count()
#
#     # Sales growth percentage (compare last month with this month)
#     last_month_start = (first_day_of_month - timedelta(days=1)).replace(day=1)
#     last_month_end = first_day_of_month - timedelta(seconds=1)
#
#     last_month_sales = Order.objects.filter(created_at__range=(last_month_start, last_month_end)).aggregate(
#         total_sales=Sum('grand_total')
#     )['total_sales'] or Decimal('0')
#
#     growth_percentage = 0
#     if last_month_sales > 0:
#         growth_percentage = ((sales_this_month or Decimal('0')) - last_month_sales) / last_month_sales * 100
#
#     # Sales by city (grouped by city from ShippingAddress)
#     sales_by_city = Order.objects.values('shipping_address__city').annotate(
#         total_sales=Sum('grand_total')
#     ).order_by('shipping_address__city')
#
#     # Prepare response data
#     response_data = {
#         'sales_this_month': sales_this_month,
#         'sales_today': sales_today,
#         'orders_today': orders_today,
#         'new_customers': new_customers,
#         'growth_percentage': round(growth_percentage, 2),
#         'sales_by_city': list(sales_by_city)
#     }
#
#     return Response({
#         "status": 200,
#         "message": "Dashboard data retrieved successfully",
#         "data": response_data
#     })


from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from order.models import Order
from customer.models import Customer
from decimal import Decimal


@api_view(['GET'])
def dashboard_stats(request):

    # Get current time
    current_time = timezone.now()

    # Sales and order data
    first_day_of_month = current_time.replace(day=1)
    sales_this_month = Order.objects.filter(created_at__gte=first_day_of_month).aggregate(
        total_sales=Sum('grand_total'))['total_sales'] or Decimal('0')

    start_of_today = current_time.replace(hour=0, minute=0, second=0)
    sales_today = Order.objects.filter(created_at__gte=start_of_today).aggregate(
        total_sales=Sum('grand_total'))['total_sales'] or Decimal('0')

    orders_today = Order.objects.filter(created_at__gte=start_of_today).count()

    new_customers = Customer.objects.filter(created__gte=first_day_of_month).count()

    # Sales growth percentage (compare last month with this month)
    last_month_start = (first_day_of_month - timedelta(days=1)).replace(day=1)
    last_month_end = first_day_of_month - timedelta(seconds=1)

    last_month_sales = Order.objects.filter(created_at__range=(last_month_start, last_month_end)).aggregate(
        total_sales=Sum('grand_total')
    )['total_sales'] or Decimal('0')

    growth_percentage = 0
    if last_month_sales > 0:
        growth_percentage = ((sales_this_month or Decimal('0')) - last_month_sales) / last_month_sales * 100

    # Sales by city (grouped by city from ShippingAddress)
    sales_by_city = Order.objects.values('shipping_address__city').annotate(
        total_sales=Sum('grand_total')
    ).order_by('shipping_address__city')

    # Calculate percentage for each city
    sales_by_city_with_percentage = []
    for city in sales_by_city:
        if sales_this_month > 0:
            city_sales_percentage = (city['total_sales'] / sales_this_month) * 100
        else:
            city_sales_percentage = 0
        sales_by_city_with_percentage.append({
            'city': city['shipping_address__city'],
            'total_sales': city['total_sales'],
            'sales_percentage': round(city_sales_percentage, 2)
        })

    # Prepare response data
    response_data = {
        'sales_this_month': sales_this_month,
        'sales_today': sales_today,
        'orders_today': orders_today,
        'new_customers': new_customers,
        'growth_percentage': round(growth_percentage, 2),
        'sales_by_city': sales_by_city_with_percentage
    }

    return Response({
        "status": 200,
        "message": "Dashboard data retrieved successfully",
        "data": response_data
    })
