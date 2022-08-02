
Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""
from __future__ import print_function

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75,
               'limes': 0.75, 'strawberries': 1.00}


def buyLotsOfFruit(orderList):
    """
	orderList: List of (fruit, numPounds) tuples

    Returns cost of order
    """
    totalCost = 0.0
    "*** YOUR CODE HERE ***"
    list_length = len(orderList)
    order_cost = 0
    for i in range(list_length):
        if 'apples' == orderList[i][0]:
          apples_requested = orderList[i][1]
          order_cost += fruitPrices['apples']*apples_requested
        if 'oranges' == orderList[i][0]:
          oranges_requested = orderList[i][1]
          order_cost += fruitPrice['oranges'] * oranges_requested
        if 'pears' == orderList[i][0]:
          pears_requested = orderList[i][1]
          order_cost += fruitPrices['pears']*pears_requested
        if 'limes' == orderList[i][0]:
          limes_requested = orderList[i][1] 
          order_cost += fruitPrices['limes']*limes_requested
        if 'strawberries' == orderList[i][0]:
          strawberries_requested = orderList[i][0]
          order_cost += fruitPrices['strawberries']*strawberries_requested
    
    return order_cost


# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)]
    print('Cost of', orderList, 'is', buyLotsOfFruit(orderList))
