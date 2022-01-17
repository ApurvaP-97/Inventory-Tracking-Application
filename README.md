#   
##  Inventory Tracking Application
### Installation Instructions:
1. Download the Inventory-Tracking-Application repository from the following git link: 
https://github.com/ApurvaP-97/Inventory-Tracking-Application
2. Place the downloaded zip folder under your Users directory “PycharmProjects” 
3. Install all the dependencies included in the requirements.txt file (Pycharm -> Tools -> Sync Python Requirements)
4. Open the Inventory-Tracking-Application Project in Pycharm, Select Project Files from dropdown
   - Run the app.py file under Application folder
   - Run models.py to reset the inventory table (By default one item will always exist in the inventory)
5. Visit the website :  http://127.0.0.1:5000/
6. To login to the website(Use the credentials - Username: admin Password: admin)

### Exploring the Dashboard
The inventory dashboard has the following basic functionalities:
1. Add Product : Add a new product by entering the Product ID, Product Name, Price and Quantity
2. Update Product : Enter the name and ID of the product you want to update. Enter the new price. To add x items to the original order, enter x in the quantity field
3. Delete Product : Enter the ID of the product to be deleted
4. View All Products : Click on this to view the inventory details
5. Export Product Data to CSV : Click on this to export the inventory details to CSV. A file : inventoryTable.csv will be downloaded to the Application folder in the backend



