from typing import TypedDict


class Station(TypedDict):
    code: str
    name: str


STATIONS: dict[str, list[Station]] = {
    "L8": [
        {"code": "JPR", "name": "Júlio Prestes"},  
        {"code": "BFU", "name": "Palmeiras-Barra Funda"},  
        {"code": "LAB", "name": "Lapa"},
        {"code": "DMO", "name": "Domingos de Moraes"},  
        {"code": "ILE", "name": "Imperatriz Leopoldina"},
        {"code": "PAL", "name": "Presidente Altino"},
        {"code": "OSA", "name": "Osasco"},
        {"code": "CSA", "name": "Comandante Sampaio"},  
        {"code": "QTU", "name": "Quitaúna"},  
        {"code": "GMC", "name": "General Miguel Costa"},
        {"code": "CPB", "name": "Carapicuíba"},  
        {"code": "STE", "name": "Santa Terezinha"},  
        {"code": "AJO", "name": "Antônio João"},  
        {"code": "BRU", "name": "Barueri"},  
        {"code": "JBE", "name": "Jardim Belval"},  
        {"code": "JSI", "name": "Jardim Silveira"},  
        {"code": "JDI", "name": "Jandira"},
        {"code": "SCO", "name": "Sagrado Coração"},  
        {"code": "ECD", "name": "Engenheiro Cardoso"},  
        {"code": "IPV", "name": "Itapevi"},  
        {"code": "SRT", "name": "Santa Rita"},  
        {"code": "AMB", "name": "Ambuitá"},  
        {"code": "ABU", "name": "Amador Bueno"}  
    ],
    "L9": [
        {"code": "OSA", "name": "Osasco"},
        {"code": "PAL", "name": "Presidente Altino"},  
        {"code": "CEA", "name": "Ceasa"},  
        {"code": "JAG", "name": "Vila Lobos-Jaguaré"},  
        {"code": "USP", "name": "Cidade Universitária"},  
        {"code": "PIN", "name": "Pinheiros"},  
        {"code": "HBR", "name": "Hebraica-Rebouças"},  
        {"code": "CJD", "name": "Cidade Jardim"},  
        {"code": "VOL", "name": "Vila Olímpia"},  
        {"code": "BRR", "name": "Berrini"},  
        {"code": "MRB", "name": "Morumbi"},  
        {"code": "GJT", "name": "Granja Julieta"},  
        {"code": "JOD", "name": "João Dias"},  
        {"code": "SAM", "name": "Santo Amaro"},  
        {"code": "SOC", "name": "Socorro"},  
        {"code": "JUR", "name": "Jurubatuba"},  
        {"code": "AUT", "name": "Autódromo"},  
        {"code": "INT", "name": "Primavera-Interlagos"},  
        {"code": "GRA", "name": "Grajaú"},  
        {"code": "MVN", "name": "Bruno Covas/Mendes-Vila Natal"},  
        {"code": "VAG", "name": "Varginha"}  
    ],
}
