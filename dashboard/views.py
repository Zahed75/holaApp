from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from order.models import Order
from customer.models import Customer
from products.models import Product
from outlet.models import Outlet
from django.db.models import Sum, F
from decimal import Decimal


@api_view(['GET'])
def dashboard_stats(request):
    # Get current time
    current_time = timezone.now()

    # Filter for sales this month
    first_day_of_month = current_time.replace(day=1)
    sales_this_month = Order.objects.filter(created_at__gte=first_day_of_month).aggregate(
        total_sales=Sum('grand_total'))

    # Filter for orders created today
    start_of_today = current_time.replace(hour=0, minute=0, second=0)
    orders_today = Order.objects.filter(created_at__gte=start_of_today).count()

    # New customers this month
    new_customers = Customer.objects.filter(created__gte=first_day_of_month).count()

    # Sales by location (aggregating by Outlet)
    sales_by_location = Outlet.objects.annotate(
        total_sales=Sum(F('outlets__orders__grand_total'))
    ).values('outletName', 'location', 'total_sales')

    # Sales growth percentage (compare last month with this month)
    last_month_start = (first_day_of_month - timedelta(days=1)).replace(day=1)
    last_month_end = first_day_of_month - timedelta(seconds=1)

    last_month_sales = Order.objects.filter(created_at__range=(last_month_start, last_month_end)).aggregate(
        total_sales=Sum('grand_total')
    )['total_sales'] or Decimal('0')

    growth_percentage = 0
    if last_month_sales > 0:
        growth_percentage = ((sales_this_month['total_sales'] or Decimal(
            '0')) - last_month_sales) / last_month_sales * 100

    # Prepare response data
    response_data = {
        'sales_this_month': sales_this_month['total_sales'],
        'orders_today': orders_today,
        'new_customers': new_customers,
        'sales_by_location': list(sales_by_location),
        'growth_percentage': round(growth_percentage, 2)
    }

    return Response({
        "status": 200,
        "message": "Dashboard data retrieved successfully",
        "data": response_data
    })
