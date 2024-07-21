import dateutil
import shippo
from shippo.models import components

import os
from dotenv import load_dotenv
load_dotenv()
api_shippo_key =  os.getenv("shippo_api")


s = shippo.Shippo(
    api_key_header=api_shippo_key,
    shippo_api_version='2018-02-08',
)


def calculate_shipping_cost():
    res = s.orders.create(request=components.OrderCreateRequest(
        placed_at='2016-09-23T01:28:12Z',
        to_address=components.AddressCreateRequest(
            country='US',
            name='Shwan Ippotle',
            company='Shippo',
            street1='215 Clayton St.',
            street3='',
            street_no='',
            city='San Francisco',
            state='CA',
            zip='94117',
            phone='+1 555 341 9393',
            email='shippotle@shippo.com',
            is_residential=True,
            metadata='Customer ID 123456',
            validate=True,
        ),
        currency='USD',
        notes='This customer is a VIP',
        order_number='#1068',
        order_status=components.OrderStatusEnum.PAID,
        shipping_cost='12.83',
        shipping_cost_currency='USD',
        shipping_method='USPS First Class Package',
        subtotal_price='12.1',
        total_price='24.93',
        total_tax='0.0',
        weight='0.4',
        weight_unit=components.WeightUnitEnum.LB,
        from_address=components.AddressCreateRequest(
            country='US',
            name='Shwan Ippotle',
            company='Shippo',
            street1='215 Clayton St.',
            street3='',
            street_no='',
            city='San Francisco',
            state='CA',
            zip='94117',
            phone='+1 555 341 9393',
            email='shippotle@shippo.com',
            is_residential=True,
            metadata='Customer ID 123456',
            validate=True,
        ),
        line_items=[
            components.LineItemBase(
                currency='USD',
                manufacture_country='US',
                max_delivery_time=dateutil.parser.isoparse('2016-07-23T00:00:00Z'),
                max_ship_time=dateutil.parser.isoparse('2016-07-23T00:00:00Z'),
                quantity=20,
                sku='HM-123',
                title='Hippo Magazines',
                total_price='12.1',
                variant_title='June Edition',
                weight='0.4',
                weight_unit=components.WeightUnitEnum.LB,
            ),
        ],
    ))
    if res is not None:
        return res.shipping_cost
        