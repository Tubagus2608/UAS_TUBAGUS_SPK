from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Handphone(Base):
    __tablename__ = "pemilihan_hp"
    id = Column(Integer, primary_key=True)
    kamera = Column(Integer)
    ram = Column(Integer)
    baterai = Column(Integer)
    harga = Column(Integer)
    ukuranlayar = Column(Integer)

    def __init__(self, kamera, ram, baterai, harga, ukuranlayar):
        self.kamera = kamera
        self.ram = ram
        self.baterai = baterai
        self.harga = harga
        self.ukuranlayar = ukuranlayar

    def calculate_score(self, dev_scale):
        score = 0
        score += self.kamera * dev_scale['kamera']
        score += self.ram * dev_scale['ram']
        score += self.baterai * dev_scale['baterai']
        score -= self.harga * dev_scale['harga']
        score += self.ukuranlayar * dev_scale['ukuranlayar']
        
        return score

    def __repr__(self):
        return f"Handphone(id={self.id!r}, kamera={self.kamera!r}, ram={self.ram!r}, baterai={self.baterai!r}, harga={self.harga!r}, ukuranlayar={self.ukuranlayar!r})"
