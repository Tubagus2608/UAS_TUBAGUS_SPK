USER = 'postgres'
PASSWORD = 'admin123'
HOST = 'localhost'
PORT = '5432'
DATABASE_NAME = 'pemilihan_hp' 
DEV_SCALE = {
    'kamera': {
        '≥ 64 MP': 5,
        '48 MP - 60 MP': 3,
        '≤ 24 MP': 1,
    },
      'ram': {
        '12 GB': 5,
        '8 GB': 3,
        '4 GB': 1,
    },
    'baterai': {
        '>= 5.500 mAh': 5,
        '4.300 mAh - 4.700 mAh': 3,
        '<= 3.095 mAh': 1,
    },
     'harga': {
        '>= Rp 13.500.000': 1,
        'Rp6.000.000 - Rp 13.000.000': 3,
        '<= Rp.5.999.999': 5,
    },
    'ukuranlayar': {
        '>= 6.7': 5,
        '6 inch ': 3,
        '<= 5.9 ': 1,
    },
}
