import os
import requests
from PIL import Image

# Directory to store the icons
ICON_DIR = 'icons'

FACTIONS = [
    {"name": "The Arborec", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/e/eb/Arborec.png/revision/latest?cb=20201104005226"},
    {"name": "The Barony of Letnev", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/2/20/Barony.png/revision/latest?cb=20201104005247"},
    {"name": "The Clan of Saar", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/b/b0/Saar.png/revision/latest?cb=20201104005333"},
    {"name": "The Embers of Muaat", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/6/60/Muaat.png/revision/latest?cb=20201104005351"},
    {"name": "The Emirates of Hacan", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/f/f8/Hacan.png/revision/latest?cb=20201104005408"},
    {"name": "The Federation of Sol", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/0/01/Sol.png/revision/latest?cb=20201104005426"},
    {"name": "The Ghosts of Creuss", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/7/7f/Ghosts.png/revision/latest?cb=20201104005444"},
    {"name": "The L1Z1X Mindnet", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/e/ec/L1Z1X.png/revision/latest?cb=20201104231507"},
    {"name": "The Mentak Coalition", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/3/3c/Mentak.png/revision/latest?cb=20201104005517"},
    {"name": "The Naalu Collective", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/a/a7/Naalu.png/revision/latest?cb=20201104005533"},
    {"name": "The Nekro Virus", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/2/22/Nekro.png/revision/latest?cb=20201104005553"},
    {"name": "Sardakk N’orr", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/1/1d/Sardakk.png/revision/latest?cb=20201104005618"},
    {"name": "The Universities of Jol-Nar", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/0/06/Jol-Nar.png/revision/latest?cb=20201104005643"},
    {"name": "The Winnu", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/c/cd/Winnu.png/revision/latest?cb=20201104005702"},
    {"name": "The Xxcha Kingdom", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/1/1a/Xxcha.png/revision/latest?cb=20201104005721"},
    {"name": "The Yin Brotherhood", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/f/f6/Yin.png/revision/latest?cb=20201104005738"},
    {"name": "The Yssaril Tribes", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/a/ac/Yssaril.png/revision/latest?cb=20201104005757"},
    {"name": "The Argent Flight", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/1/13/ArgentFactionSymbol.png/revision/latest?cb=20201103113416"},
    {"name": "The Empyrean", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/c/ca/EmpyreanFactionSymbol.png/revision/latest?cb=20201103113437"},
    {"name": "The Mahact Gene-Sorcerers", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/3/35/MahactFactionSymbol.png/revision/latest?cb=20201103113459"},
    {"name": "The Naaz-Rokha Alliance", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/c/c3/NaazRokhaFactionSymbol.png/revision/latest?cb=20201105035733"},
    {"name": "The Nomad", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/5/5e/NomadFactionSheet.png/revision/latest?cb=20201104084557"},
    {"name": "The Titans of Ul", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/6/6d/UlFactionSymbol.png/revision/latest?cb=20201103113547"},
    {"name": "The Vuil'Raith Cabal", "icon": "https://static.wikia.nocookie.net/twilight-imperium-4/images/0/04/CabalFactionSymbol.png/revision/latest?cb=20201103113606"}
]

# Create the icons directory if it doesn't exist
if not os.path.exists(ICON_DIR):
    os.makedirs(ICON_DIR)

# Download and cache the icons
for faction in FACTIONS:
    icon_url = faction['icon']
    icon_name = faction['name'].replace(' ', '_') + '.png'
    icon_path = os.path.join(ICON_DIR, icon_name)

    # Check if the icon is already cached
    if not os.path.exists(icon_path):
        response = requests.get(icon_url)
        with open(icon_path, 'wb') as file:
            file.write(response.content)

        # Optionally, resize the image to 100x100
        with Image.open(icon_path) as img:
            img = img.resize((100, 100), Image.LANCZOS)
            img.save(icon_path)

    # Update the faction icon with the local path
    faction['icon'] = icon_path
