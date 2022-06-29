from dataclasses import dataclass
@dataclass
class DataClassCard:
    rank : str
    suit : str


if __name__ == '__main__' :
    data = DataClassCard("number one","2")
    print(data.rank)

