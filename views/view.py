import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date

class SubscriptionSevice:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscraption: Subscription):
        with Session(self.engine) as session:
            session.add(subscraption)
            session.commit()
            return subscraption
        
    def list_all(self):
        with Session(self.engine) as session:
            statiment = select(Subscription)
            results = session.exec(statiment).all()
        return results
    
    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).where(Subscription.empresa==subscription.empresa)
            results =  session.exec(statement).all()
            
            pago = False
            for result in results:
                if result.date.month == date.today().month:
                    pago = True
                    
                if self._has_pay(results):
                    question = input('Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N: ')

                    if not question.upper() == 'Y':
                        return
                    
                pay = Payments(subscription_id=subscription.id, date=date.today())
                session.add(pay)
                session.commit()
    
ss = SubscriptionSevice(engine)
subscription = Subscription(empresa='Pythonando', site='pythonando.com.br', data_assinatura=date.today(), valor=37.90)
ss.pay(subscription)
