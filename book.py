from functools import total_ordering


class Order:
    def __init__(self, quantity, price, buy=True, identity=0):
        self.quantity = quantity
        self.price = price
        self.buy = buy
        self.identity = identity

    def quantity(self):
        return self.__quantity if self.buy else -self.__quantity

    def side_order(self):
        if self.buy==True:
            return "BUY"
        else:
            return "SELL"
    
    def __str__(self): # human-readable content
        return "%s@%s" % (self.quantity, self.price)

    def __repr__(self): # unambiguous representation of the object
        return "Order(%s, %s)" % (self.quantity, self.price)
    
    def __eq__(self, other): # self == other
        return other and self.quantity == other.quantity and self.price== other.price

    def __lt__(self, other): # self < other
        return other and self.price < other.price


class Book:

    def __init__(self, name):
        self.name = name
        self.buy_orders = []
        self.sell_orders = []
        self.ordered_orders = []
        self.count = 0

    def count_add(self):
        self.count +=1

    #def insert_order(self, order):  # Plus généraliste
    #    if order.buy==True:
    #        self.buy_orders.append(order)
    #    else:
    #        self.sell_orders.append(order)

    def orders_match(self,order):
        quantities_traded = []
        matched_orders = []

        for element in self.ordered_orders:
            if order.buy==False and order.buy != element.buy  and order.price<=element.price:
                matched_orders.append(element)
            if order.buy==True and order.buy != element.buy  and order.price>=element.price:
                matched_orders.append(element)

        quantity_left = order.quantity
        for element  in matched_orders:
            quantities_traded.append([min(element.quantity, quantity_left),element.price])
            q = quantity_left
            quantity_left = quantity_left-element.quantity
            for offer in self.ordered_orders:
                if element.identity == offer.identity:
                     offer.quantity = offer.quantity - q
                if offer.quantity <=0:
                    self.ordered_orders.remove(offer)
            if quantity_left <=0:
                break
        
        if quantity_left>0:
            self.ordered_orders.append(order)
        
        self.ordered_orders = sorted(self.ordered_orders, key= lambda x:(x.price,x.quantity),reverse=True)

        return quantities_traded


    def orders_dislplay(self,order):
        
        print("Book on {0}".format(self.name))

        if len(self.ordered_orders)==0:
            self.ordered_orders.append(order)
        else:
            quantities_after_execution = self.orders_match(order)
            if len(quantities_after_execution)!=0:
                for i in range(0,len(quantities_after_execution)):
                    print("Execute {0} at {1} on {2}".format(quantities_after_execution[i][0], quantities_after_execution[i][1], self.name))

        for i in range (0,len(self.ordered_orders)):
            print("         {0} {1} id={2}".format(self.ordered_orders[i].side_order(), self.ordered_orders[i].__str__(),self.ordered_orders[i].identity))


     def book_display(self):
        
        print("Affichage de notre book en format dataframe : ")
        
        ordres = []
        for i in range(0, len(self.ordered_orders)):
            if(self.ordered_orders[i].buy == 0.0):
                self.ordered_orders[i].buy = "SELL"
            else :
                self.ordered_orders[i].buy = "BUY"
            ordres.append([self.ordered_orders[i].quantity, self.ordered_orders[i].price, self.ordered_orders[i].buy, self.ordered_orders[i].identity])
        ordres2= np.array(ordres)
        
        our_book_buy = pd.DataFrame(ordres2, columns = ['Quantite','Prix','Type','id'])
        print(our_book_buy)  


    def insert_buy(self,quantity,price):

        self.count_add() # id ++
        order_buy = Order(quantity,price,True,self.count)
        self.buy_orders.append(order_buy)

        print("--- Insert BUY {0} id={1} on {2}".format(order_buy.__str__(),self.count,self.name))
        self.orders_dislplay(order_buy)
        print("-------------------------")

    def insert_sell(self,quantity,price):

        self.count_add() #id++
        order_sell = Order(quantity,price,False,self.count)
        self.sell_orders.append(order_sell)

        print("--- Insert SELL {0} id={1} on {2}".format(order_sell.__str__(),self.count,self.name))
        self.orders_dislplay(order_sell)
        print("-------------------------")

#booky = Book("TEST")
#booky.insert_buy(10,10)

book = Book("TEST")
book.insert_buy(10, 10.0)
book.insert_sell(120, 12.0)
book.insert_buy(5, 10.0)
book.insert_buy(2, 11.0)
book.insert_sell(1, 10.0)
book.insert_sell(10, 10.0)