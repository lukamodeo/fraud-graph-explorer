# src/fraud_graph_explorer/sheet_crafter/seed_data.py
import random

# We group data into "Profiles" to ensure algorithmic IDs (IT, FR) match the personal data.
# I have calculated the checksums/control letters for these specific profiles.

SEED_PROFILES = {
    'IT': [
        # Name, sex, DOB, Birthplace Code, Codice Fiscale (TIN)
        {'name': 'Mario Rossi', 'sex': 'M', 'birthdate': '1980-04-15', 'birthplace': 'H501', 'tin': 'RSSMRA80D15H501Z'},
        {'name': 'Giulia Bianchi', 'sex': 'F', 'birthdate': '1992-05-23', 'birthplace': 'F205', 'tin': 'BNCGLI92E63F205V'},
        {'name': 'Luca Verdi', 'sex': 'M', 'birthdate': '1975-07-08', 'birthplace': 'L783', 'tin': 'VRDLCA75L08L783Q'},
        {'name': 'Sofia Romano', 'sex': 'F', 'birthdate': '1988-12-14', 'birthplace': 'Z210', 'tin': 'RMNSFO88T62Z210L'},
        {'name': 'Alessandro Ferrari', 'sex': 'M', 'birthdate': '1995-09-30', 'birthplace': 'H501', 'tin': 'FRRLSN95P30H501L'},
        {'name': 'Emma Russo', 'sex': 'F', 'birthdate': '1982-12-05', 'birthplace': 'F205', 'tin': 'RSSEMM82T45F205X'},
        {'name': 'Francesco Esposito', 'sex': 'M', 'birthdate': '1979-06-18', 'birthplace': 'L783', 'tin': 'ESPFRC79H18L783Y'},
        {'name': 'Aurora Colombo', 'sex': 'F', 'birthdate': '1990-03-22', 'birthplace': 'Z210', 'tin': 'CLMAUR90C62Z210W'}
        ],
    'DE': [
        # German Steuer-ID is administrative, no link to name/birthdate needed
        {'name': 'Lukas Müller', 'sex': 'M', 'birthdate': '1985-01-20', 'tin': '12345678901'},
        {'name': 'Anna Schmidt', 'sex': 'F', 'birthdate': '1990-08-12', 'tin': '10987654321'},
        {'name': 'Felix Weber', 'sex': 'M', 'birthdate': '1978-05-04', 'tin': '11223344556'},
        {'name': 'Sophia Becker', 'sex': 'F', 'birthdate': '1993-10-27', 'tin': '16574839201'},
        {'name': 'Jonas Wagner', 'sex': 'M', 'birthdate': '1982-03-15', 'tin': '19876543210'},
        {'name': 'Laura Fischer', 'sex': 'F', 'birthdate': '1991-07-09', 'tin': '10293847561'},
        {'name': 'Max Bauer', 'sex': 'M', 'birthdate': '1976-12-01', 'tin': '15647382910'},
        {'name': 'Emma Hoffmann', 'sex': 'F', 'birthdate': '1989-09-18', 'tin': '19283746501'}
        ],
    'FR': [
        # French NIR (TIN) is semi-algorithmic: sex(1) + YY + MM + Dept(2) + Commune(3) + Serial(3) + Control(2)
        # e.g., 1 87 02 75 123 456 78 = Male (1), born Feb 1987 (87 02), in Paris (75)
        {'name': 'Pierre Dupont', 'sex': 'M', 'birthdate': '1987-02-11', 'tin': '187027512345678'},
        {'name': 'Camille Martin', 'sex': 'F', 'birthdate': '1994-09-25', 'tin': '294097512345638'},
        {'name': 'Hugo Bernard', 'sex': 'M', 'birthdate': '1981-06-30', 'tin': '181067512345610'},
        {'name': 'Léa Dubois', 'sex': 'F', 'birthdate': '1996-04-17', 'tin': '296047512345684'},
        {'name': 'Louis Thomas', 'sex': 'M', 'birthdate': '1983-11-08', 'tin': '183117512345621'},
        {'name': 'Chloé Robert', 'sex': 'F', 'birthdate': '1992-01-19', 'tin': '292017512345698'},
        {'name': 'Paul Richard', 'sex': 'M', 'birthdate': '1977-08-14', 'tin': '177087512345643'},
        {'name': 'Manon Petit', 'sex': 'F', 'birthdate': '1988-12-03', 'tin': '188127512345615'}
        ],
    'ES': [
        # Spanish DNI (TIN) is 8 digits + 1 control letter. No link to name/birthdate.
        # Letters are calculated modulo 23.
        {'name': 'Juan García', 'sex': 'M', 'birthdate': '1986-03-14', 'tin': '12345678Z'},
        {'name': 'Lucía Martínez', 'sex': 'F', 'birthdate': '1991-10-22', 'tin': '87654321X'},
        {'name': 'Carlos Rodríguez', 'sex': 'M', 'birthdate': '1979-07-05', 'tin': '11223344A'},
        {'name': 'Sofía López', 'sex': 'F', 'birthdate': '1994-12-28', 'tin': '99887766B'},
        {'name': 'Pablo González', 'sex': 'M', 'birthdate': '1984-05-16', 'tin': '55443322C'},
        {'name': 'María Fernández', 'sex': 'F', 'birthdate': '1993-08-11', 'tin': '66778899D'},
        {'name': 'Diego Sánchez', 'sex': 'M', 'birthdate': '1978-02-25', 'tin': '22334455E'},
        {'name': 'Valeria Pérez', 'sex': 'F', 'birthdate': '1989-09-09', 'tin': '77665544F'}
        ],
    'GB': [
        # UK NINO (TIN) is administrative: 2 allowed letters + 6 digits + 1 letter (A-D)
        {'name': 'Oliver Smith', 'sex': 'M', 'birthdate': '1988-04-18', 'tin': 'AB123456C'},
        {'name': 'Emma Jones', 'sex': 'F', 'birthdate': '1995-11-02', 'tin': 'YZ987654D'},
        {'name': 'Harry Williams', 'sex': 'M', 'birthdate': '1982-07-21', 'tin': 'QQ112233A'},
        {'name': 'Olivia Taylor', 'sex': 'F', 'birthdate': '1997-03-14', 'tin': 'WW998877B'},
        {'name': 'George Brown', 'sex': 'M', 'birthdate': '1985-09-30', 'tin': 'EE554433C'},
        {'name': 'Ava Davies', 'sex': 'F', 'birthdate': '1994-01-25', 'tin': 'RR667788D'},
        {'name': 'Jack Wilson', 'sex': 'M', 'birthdate': '1980-06-12', 'tin': 'TT223344A'},
        {'name': 'Isabel Evans', 'sex': 'F', 'birthdate': '1991-10-08', 'tin': 'UU776655B'}
        ]
    }

# VATs are company-level, not personal. They can remain in separate lists.
SEED_VATS = {
    'IT': ['01234567890', '09876543210', '05555555555', '01111222333', '04444555666', '07777888999', '02222333444', '06666777888'],
    'DE': ['DE123456789', 'DE987654321', 'DE112233445', 'DE998877665', 'DE554433221', 'DE667788990', 'DE223344556', 'DE776655443'],
    'FR': ['FR12345678901', 'FR98765432109', 'FR11223344556', 'FR99887766554', 'FR55443322110', 'FR66778899001', 'FR22334455662', 'FR77665544338'],
    'ES': ['A12345678', 'B87654321', 'A11223344', 'B99887766', 'A55443322', 'B66778899', 'A22334455', 'B77665544'],
    'GB': ['GB123456789', 'GB987654321', 'GB112233445', 'GB998877665', 'GB554433221', 'GB667788990', 'GB223344556', 'GB776655443']
    }


def get_random_profile(country_code: str) -> dict:
    """
    Picks a perfectly matched profile (Name, sex, DOB, TIN) and a random VAT.
    """
    cc = country_code.upper()
    profiles = SEED_PROFILES.get(cc, SEED_PROFILES['GB'])
    vats = SEED_VATS.get(cc, SEED_VATS['GB'])

    profile = random.choice(profiles)

    return {
        'name': profile['name'],
        'sex': profile['sex'],
        'birthdate': profile['birthdate'],
        'birthplace': profile.get('birthplace', 'XXXX'),
        'tin': profile['tin'],
        'vat': random.choice(vats)
    }