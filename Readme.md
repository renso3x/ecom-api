## Create Super User

 `docker-compose run app sh -c "python manage.py createsuperuser"`


 ## Database

- User - Done
  - first name
  - last name
  - email
  - password
  - government_id
  - profile_image
  - user_type ('buyer', 'merchant')

- Address - Done
  - user(fk)
  - name
  - full address
  - city
  - latitude
  - longitude

- Category - Done
  - name

- Store - done
  - name
  - address(fk)
  - user(fk) -> merchant of the store

- Product - Done
  - category(fk)
  - store(fk)
  - name
  - description
  - price -> estimated price
  - image

- Order Item - Done
  - product(fk)
  - user(fk)
  - quantity (5)
  - estimated total price(5 * product.price)

* From Order Table if final
- Invoice
  - order(fk)
  - status('issued', 'picked up', 'completed', 'cancelled')
  - price -> if the status is picked up this shows the actual price of the order item
  - payment ('Cash on Delivery')
  - date_issued

- Transaction
  - invoice(fk)
  - user(fk) -> for merchant only




