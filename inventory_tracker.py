from models import Item, Base, DATABASE_URI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import locale
locale.setlocale(locale.LC_ALL, '')

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

    def search(self, query, prefix=""):
        query = "%"+query+"%"
        items = self.session.query(Item).filter(Item.name.like(query)).all()
        for item in items:
            print(prefix+str(item.id), item.name, item.serial_number, item.value)

    def write_csv(self, path="./out.csv"):
        items = self.session.query(Item).all()
        with open(path, "w") as f:
            f.write("id, name, serial_number, value\n")
            for item in items:
                cents = int(item.value % 100)
                line = "%d, %s, %s, %s\n" % (item.id, item.name, item.serial_number,
                                           locale.currency(item.value / 100))
                f.write(line)

    def print(self, prefix=""):
        items = self.session.query(Item).all()
        for item in items:
            print(prefix+str(item.id), item.name, item.serial_number, item.value, sep='\t')

if __name__ == '__main__':
    inventoryTracker = InventoryTracker()

    while(1):
        print("************************************************************")
        print("Select one of the following:")
        ip = input("\t1. Add item\n\t2. Remove item\n\t3. Generate CSV\n\t4. Print\n\t5. Search\n\t6. Exit\n")

        if ip == '1':
            print("***Adding item***")
            name = input("\t>> name:")
            serial_number = input("\t>> serial number:")
            value = int(input("\t>> value (in cents):"))

            inventoryTracker.add_item(name, serial_number, value)

            print("***Added item!***")

        elif ip == '2':
            print("***Removing item***")
            print("\t> All Items:")
            inventoryTracker.print()
            item_id = input("\t>> Item id:")
            inventoryTracker.remove_item(item_id)

            print("> Removed item!")
        elif ip == '3':
            inventoryTracker.write_csv()
        elif ip == '4':
            print("***All items***")
            inventoryTracker.print("\t\t")
        elif ip == '5':
            print("***Searching inventory***")
            query = input("\t> Search query: ")
            print("\t> Search results:")
            inventoryTracker.search(query, "\t\t")
        elif ip == '6':
            print("Bye!")
            break
        else:
            print("***Invalid option***")
