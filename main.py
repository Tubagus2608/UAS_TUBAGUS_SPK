# main.py
import sys
from colorama import Fore, Style
from models import Base, Handphone
from engine import engine
from tabulate import tabulate
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import DEV_SCALE

session = Session(engine)


def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has been created!')


def review_data():
    query = select(Handphone)
    for phone in session.scalars(query):
        print(phone)


class BaseMethod():

    def __init__(self):
        # 1-5
        self.raw_weight = {'kamera': 3, 'ram': 4, 'baterai': 4, 'harga': 3, 'ukuranlayar': 3}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Handphone.id, Handphone.kamera, Handphone.ram, Handphone.baterai,
                       Handphone.harga, Handphone.ukuranlayar)
        result = session.execute(query).fetchall()
        return [{'id': phone.id, 'kamera': phone.kamera, 'ram': phone.ram, 'baterai': phone.baterai,
                'harga': phone.harga, 'ukuranlayar': phone.ukuranlayar} for phone in result]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        kamera_values = []  # max
        ram_values = []  # max
        baterai_values = []  # max
        harga_values = []  # min
        ukuranlayar_values = []  # max

        for data in self.data:
            # Kamera
            kamera_values.append(data['kamera'])

            # RAM
            ram_values.append(data['ram'])

            # Baterai
            baterai_values.append(data['baterai'])

            # Harga
            harga_values.append(data['harga'])

            # Ukuran Layar
            ukuranlayar_values.append(data['ukuranlayar'])

        return [
            {'id': data['id'],
             'kamera': data['kamera'] / max(kamera_values),
             'ram': data['ram'] / max(ram_values),
             'baterai': data['baterai'] / max(baterai_values),
             'harga': min(harga_values) / data['harga'] if data['harga'] != 0 else 0,
             'ukuranlayar': data['ukuranlayar'] / max(ukuranlayar_values)
             }
            for data in self.data
        ]


class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                'id': row['id'],
                'produk': row['kamera']**self.weight['kamera'] *
                row['ram']**self.weight['ram'] *
                row['baterai']**self.weight['baterai'] *
                row['harga']**self.weight['harga'] *
                row['ukuranlayar']**self.weight['ukuranlayar']
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'id': product['id'],
                'kamera': product['produk'] / self.weight['kamera'],
                'ram': product['produk'] / self.weight['ram'],
                'baterai': product['produk'] / self.weight['baterai'],
                'harga': product['produk'] / self.weight['harga'],
                'ukuranlayar': product['produk'] / self.weight['ukuranlayar'],
                'score': product['produk']  # Nilai skor akhir
            }
            for product in sorted_produk
        ]
        return sorted_data


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
                  round(row['kamera'] * weight['kamera'] +
                        row['ram'] * weight['ram'] +
                        row['baterai'] * weight['baterai'] +
                        row['harga'] * weight['harga'] +
                        row['ukuranlayar'] * weight['ukuranlayar'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result


def run_saw():
    saw = SimpleAdditiveWeighting()
    result = saw.calculate
    print(tabulate([(k, v) for k, v in result.items()], headers=['ID', 'Score'], tablefmt='pretty'))


def run_wp():
    wp = WeightedProduct()
    result = wp.calculate
    headers = result[0].keys()
    rows = [
        {k: round(v, 4) if isinstance(v, float) else v for k, v in val.items()}
        for val in result
    ]
    print(tabulate(rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == 'create_table':
            create_table()
        elif arg == 'review_data':
            review_data()
        elif arg == 'saw':
            run_saw()
        elif arg == 'wp':
            run_wp()
        else:
            print('Command not found')
    else:
        print('Please provide a command')
