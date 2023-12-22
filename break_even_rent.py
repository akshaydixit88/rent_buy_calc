def future_value(present_value, interest_rate, n):
  """
    Future value of the investment.
  """
  return present_value * (1 + interest_rate) ** n


def calculate_buying_cost(house_price, down_payment_rate, cost_buying, cost_selling,
                           mortgage_rate, property_tax_rate, maintenance_rate,
                           insurance_rate, inflation_rate, mortgage_term,own_term, investment_return, HOA_fee, property_inflation):
  """
  Calculates the total cost of buying a house in year 10, accounting for inflation and growth.

  Returns:
    Total cost of buying the house at term
  """
  # Calculate total down payment and closing costs
  initial_investment = (down_payment_rate + cost_buying) * house_price
  principle = house_price * (1 - down_payment_rate)
  #print("Principle:", principle)
  #print("initial_investment:", initial_investment)

  # Calculate opportunity cost of down payment and closing costs
  future_investment = future_value(initial_investment, investment_return, own_term)
 
   # Monthly mortgage payments
  monthly_interest_rate = mortgage_rate / 12
  number_of_payments = mortgage_term * 12
  monthly_payment = (principle * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-number_of_payments))
  #print("Monthly mortgage payment:", monthly_payment)
  
  # Remaining principle 
  remaining_payments = (mortgage_term - own_term) *12
  actual_payments = own_term * 12
  remaining_principal = (principle * (1 + monthly_interest_rate) ** actual_payments) - (monthly_payment * (1/monthly_interest_rate) * (((1 + monthly_interest_rate) ** actual_payments) - 1))
  #print("remaining_principal:", remaining_principal)
  
  # Other recurring costs
  monthly_recurring_cost = house_price * (property_tax_rate + maintenance_rate + insurance_rate) * (1/12) + HOA_fee
  #print("monthly_recurring_cost:", monthly_recurring_cost)
  total_recurring_cost = 0
  for year in range(1, own_term + 1):
        # Calculate the variable cost for the current year
        annual_recurring_cost = monthly_payment * 12 + ((monthly_recurring_cost * 12) * (1 + inflation_rate) ** (year - 1))
        ##print("Year", year, "recurring payment:", annual_recurring_cost)
        total_recurring_cost += future_value(annual_recurring_cost, investment_return, own_term - year)
        ##print("Year", year, "recurring payment:", annual_recurring_cost, "adj_recurring_payment", future_value(annual_recurring_cost, investment_return, own_term - year))

  #future sale price
  future_sale_price = future_value(house_price, property_inflation, own_term)
  #print("Future value of initial investment:", future_investment)
  #print("Future value of total_recurring_cost", total_recurring_cost)
  #print("Net Proceed:", future_sale_price * ( 1 - cost_selling) - remaining_principal)
  
  house_gain = (future_sale_price * ( 1 - cost_selling)) - house_price
  
  if house_gain > 500000:
    taxable_gain = house_gain - 500000
    capital_tax = taxable_gain * 0.2
  else:
    capital_tax = 0
  
  # Calculate total cost in year 10
  total_cost = future_investment + total_recurring_cost - future_sale_price * (1 - cost_selling) + remaining_principal + capital_tax
  return total_cost

def calculate_renting_cost(monthly_rent, security_deposit, broker_fee, renter_insurance, own_term, 
                          rental_inflation_rate, investment_return):
  
  # Security deposit
  initial_deposit = monthly_rent * security_deposit + monthly_rent * broker_fee
  rental_future_investment = future_value(initial_deposit, investment_return, own_term)
  #print("rental_FV_initial_investment:", rental_future_investment)
   
  # Calculate annual rent
  annual_rent = monthly_rent * 12 * (1 + renter_insurance)
  #print("annual_rent:", annual_rent)
  total_renting_recurring_cost = 0
  for year in range(1, own_term + 1):
        # Calculate the variable cost for the current year
        annual_renting_cost = annual_rent * (1 + rental_inflation_rate) ** (year - 1)
        #print("Year", year, "annual_renting_cost:", annual_renting_cost)
        total_renting_recurring_cost += future_value(annual_renting_cost, investment_return, own_term - year)


  total_reting_cost = rental_future_investment + total_renting_recurring_cost
  return total_reting_cost


# Input parameters
house_price = 1750000
down_payment_rate = 0.2 
cost_buying = 0.02 
cost_selling = 0.05
mortgage_rate = 0.08
property_tax_rate = 0.0125
maintenance_rate = 0.005
insurance_rate = 0.005
inflation_rate = 0.03
mortgage_term = 30
own_term = 10
investment_return = 0.08
HOA_fee = 50
property_inflation = 0.05
monthly_rent = 3000
security_deposit = 1
broker_fee = 1 
renter_insurance = 0.013
rental_inflation_rate = 0.03

total_buying_cost = calculate_buying_cost(house_price, down_payment_rate, cost_buying, cost_selling,
                           mortgage_rate, property_tax_rate, maintenance_rate,
                           insurance_rate, inflation_rate, mortgage_term,own_term, investment_return, HOA_fee, property_inflation)


total_renting_cost = calculate_renting_cost(monthly_rent, security_deposit, broker_fee, renter_insurance, own_term, 
                          rental_inflation_rate, investment_return)
                          
#print("Total cost of buying over", own_term, "years:", total_buying_cost)
#print("Total cost of reting over", own_term, "years:", total_renting_cost)


def find_break_even_rent(initial_rent, house_price, mortgage_rate, own_term, step_size=100, max_iterations=100):
    buying_cost = calculate_buying_cost(house_price, down_payment_rate, cost_buying, cost_selling,
                           mortgage_rate, property_tax_rate, maintenance_rate,
                           insurance_rate, inflation_rate, mortgage_term,own_term, investment_return, HOA_fee, property_inflation)

    renting_cost = calculate_renting_cost(initial_rent, security_deposit, broker_fee, renter_insurance, own_term, 
                          rental_inflation_rate, investment_return)
    iteration = 0
    while abs(buying_cost - renting_cost) / buying_cost * 100 > 2 and iteration < max_iterations:
        initial_rent += step_size
        renting_cost = calculate_renting_cost(initial_rent, security_deposit, broker_fee, renter_insurance, own_term, 
                          rental_inflation_rate, investment_return)
        iteration += 1

    if iteration < max_iterations:
        return initial_rent
    else:
        raise ValueError("Break-even rent not found within the maximum number of iterations.")



