
from abc import ABC, abstractmethod

class BankInterface(ABC):
    @abstractmethod
    def get_balance():
      pass

    @abstractmethod
    def get_bank_name():
      pass


from .dcuBank import DCUBank

#Factory class, used to actually create the correct bank Implementation
class BankFactory():
  @staticmethod
  def factory(type):
    if type=="DCU": return DCUBank()
    if type=="FAKEBANK": return FakeBank()
    assert 0, "Type not supported: %s" %(type)\


from .bankInterface import BankInterface

class DCUBank(BankInterface):
  def get_balance(self):
    return 1000

  def get_bank_name(self):
    return "DCU"
