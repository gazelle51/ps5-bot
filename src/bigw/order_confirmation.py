def get_order_data(soup):
    '''
    Get order data from an order confirmation Soup object.

    :param BeautifulSoup soup: Beautiful Soup object for order confirmation.
    :return: order data as a string
    :rtype: string
    '''

    # Set up order data
    order_data = ''

    # Find tables
    tables = soup.findAll('table')
    for table in tables:
        # Stop if not "Order Details"
        if not table.findPreviousSibling().text.lower() == 'order details':
            continue

        # Update order data with table details
        order_data = order_data + '-------------\nOrder details\n-------------\n\n'
        rows = table.findAll('tr')
        for row in rows:
            table_data = row.findAll('td')
            order_data = order_data + table_data[0].text.strip() + ': ' + table_data[1].text.strip() + '\n'

        order_data = order_data + '\n'

    # Find addresses
    addresses = soup.findAll('address')
    for address in addresses:
        # Update order data with address details
        order_data = order_data + '----------------\n' + address.findPreviousSibling().text.strip() + '\n----------------\n\n'
        divs = address.findAll('div')
        for div in divs:
            order_data = order_data + div.text.strip() + '\n'

        order_data = order_data + '\n'

    # Find order summary
    order_summary = soup.find('div', {'class': 'OrderConfirmationSummary'})

    # Update order data with address details
    order_data = order_data + '-------------\nOrder Summary\n-------------\n\n'
    items = order_summary.findAll('div', {'class': 'CartSummaryEntryItem'})
    for i, item in enumerate(items):
        product = item.find('div', {'class': 'product'})
        quantity = item.find('div', {'class': 'quantity'})
        price = item.find('span', {'class': 'price'})
        order_data = order_data + '{}. {} (x{}) {}\n'.format(i+1, product.text.strip(),
                                                             quantity.text.strip(), price.text.strip().replace('\n', ''))

    # Item subtotal
    subtotal = soup.find('div', {'class': 'summary-detail'}) \
        .find('div', {'class': 'CartSummaryRow'}) \
        .find('span', {'class': 'Price'})
    order_data = order_data + '\nItem subtotal: {}\n'.format(subtotal.text.strip().replace('\n', ''))

    # Final total
    total = soup.find('div', {'class': 'order-summary-total'}) \
        .find('span', {'class': 'Price'})
    order_data = order_data + 'Total after discounts and shipping: {}'.format(total.text.strip().replace('\n', ''))

    return order_data
