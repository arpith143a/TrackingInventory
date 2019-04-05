from models import Item, Base, DATABASE_URI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class InventoryTracker(object):
    def __init__(self):
        super(InventoryTracker, self).__init__()
        self.inventory = []

        engine = create_engine(DATABASE_URI, echo=False)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

    def add_item(self, name, serial_number, value):
        new_item = Item(name=name, serial_number=serial_number, value=value)
        self.session.add(new_item)
        self.session.commit()
    
    def remove_item(self, item_id):
        self.session.query(Item).filter_by(id=item_id).delete()
        self.session.commit()

    def write_csv(self, path="./out.csv"):
        items = self.session.query(Item).all()
        with open(path, "w") as f:
            f.write("id, name, serial_number, value\n")
            for item in items:
                line = "%d, %s, %s, %s\n" % (item.id, item.name, item.serial_number,
                                           item.value)
                f.write(line)

    def print(self):
        items = self.session.query(Item).all()
        for item in items:
            print(item.id, item.name, item.serial_number, item.value)

if __name__ == '__main__':
    inventoryTracker = InventoryTracker()

    while(1):
        print("************************************************************")
        print("Select one of the following:")
        ip = input("1. Add item\n2. Remove item\n3. Generate CSV\n4. Print\n5. Exit\n")

        if ip == '1':
            print("> Add item:")
            name = input(">> name:")
            serial_number = input(">> serial number:")
            value = int(input(">> value:"))

            inventoryTracker.add_item(name, serial_number, value)

            print("> Added item!")

        elif ip == '2':
            print("> Remove item:")
            print("> All Items:")
            inventoryTracker.print()
            item_id = input(">> Item id:")
            inventoryTracker.remove_item(item_id)

            print("> Removed item!")
        elif ip == '3':
            inventoryTracker.write_csv()
        elif ip == '4':
            inventoryTracker.print()
        elif ip == '5':
            print("Bye!")
            break
        else:
            print("> Invalid option.")
