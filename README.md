# Define the Projects Purpose
The name of the system that I am building is called a Smart Inventory Management System (SIMS).This current project will be the backend API system for the system.
It will manage the products, customers, suppliers, warehouses, order and employees

# Identify the different user roles
It will have different users such as 
1. Super Admin : Has access to everything
2. Warehouse Manager : Add products, updates inventory, receive shipments
3. Sales Representatives : sells product, views products, view prices, record payments
4. Accountants : View invoices, record payments, record purchase
5. Customers : Views products, place orders, view own invoices, view prices

# List the Applications's Features
It performs several features including:
1. It ensures an effortless and very concise way of managing the flow of products, money and the overall system.
2. It ensure credibility
3. It ensures concurrency and transparency
4. It simplifies the complex management of systems
5. It provides checks and effective management

# Sketch the database entities
The database will comprise of several tables which will relate with one another. The tables include:
1. User: id, first name, last name, email, password.
2. UserRoles: id, user_id, role_id
3. Role: id, role.
4. Products: id, track_id,name, price, category_id.
5. Categories: id, name.
6. Warehouses: id, name, location.
7. Inventory: id, warehouse_id, quantity, product_id
8. InventoryTransaction: id, inventory_id, user_id, transaction_type, quantity_changed, created_At
9. Orders: id, total_amount, user_id, order_date. 
10. OrderItems: id, order_id, amount, quantity, product_id, 
11. Suppliers: id, name, location, address.
12. SupplyOrders: id, supplier_id, total_amount, order_date
13. SupplyOrdersItems: id, supply_order_id, product_id, quantity, unit_cost
14. Payments: id, user_id, amount, payment_date, payment_method
15. OrderPayment: id, payment_id, order_id, amount_applied

The relations between these tables will be as follows:
1. User will have a Many-to-Many relationship with Role
2. User will have a One-to-Many relationship with Order
3. User will have a One-to-Many relationship with Payment
4. Products will have a Many-to-One relationship with Categories
5. OrderItem will have a Many-to-One relationship with Order
6. Inventory will have a Many-to-One relationship with Warehouse
7. SupplyOrder will have a Many-to-One realtionship with Suppliers
8. SupplyOrder will have a Many-to-Many relationship with Product
9. Payment will have a Many-to-One relationship with User
10. Payment will have a Many-to-Many relationship with Order

Constraints
1. UNIQUE: (user_id and role_id) TABLE USERROLES
2. UNIQUE: (warehouse_id and product_id) TABLE INVENTORY
3. UNIQUE: (email) TABLE users



Transactions
1. for the InventoryTransaction TABLE, Transaction type (ENUM: 'recieve', 'ship', 'adjustment', 'damage', 'return')
# Design the folder Structure

inventory-api/
    app/
        __init__.py
        config.py
        extensions.py

        auth/
        users/
        roles/
        products/
        inventory/
        warehouses/
        suppliers/
        orders/
        payments/
        dashboard/
        reports/
        notifications/

        models/
        schemas/
        services/
        repositories/
        cache/
        tasks/
        security/
        middleware/
        utils/
        errors/
    migrtaions/
    test/
    docs/
    instance/
    requirements.txt
    .env
    .env.example
    run.py
    README.md
    docker-compose.yml


# Learn the Request/Response Lifecycle in Flask
