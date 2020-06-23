## Create Super User

 `docker-compose run app sh -c "python manage.py createsuperuser"`


 ## Database

- User
  - first name
  - last name
  - email
  - password
  - government_id
  - profile_image
  - user_type ('buyer', 'merchant')

- Address
  - user(fk)
  - name
  - full address
  - city
  - latitude
  - longitude

- Category
  - name

- Store
  - name
  - address(fk)
  - user(fk) -> merchant of the store

- Product
  - category(fk)
  - store(fk)
  - name
  - description
  - price -> estimated price
  - image
  - other details

- Order Item
  - product(fk)
  - user(fk)
  - quantity (5)
  - estimated total price(5 * product.price)

- Invoice
  - order(fk)
  - status('issued', 'picked up', 'completed', 'cancelled')
  - price -> if the status is picked up this shows the actual price of the order item
  - payment ('Cash on Delivery')
  - date_issued

- Transaction
  - invoice(fk)
  - user(fk) -> for merchant only




