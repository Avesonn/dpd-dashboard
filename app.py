import streamlit as st
import pandas as pd
import ftplib
import io

# --- KOMPLETNÍ SLOVNÍK STÁTŮ ---
nazvy_statu = {
    "AF": "Afghánistán", "AX": "Alandy", "AL": "Albánie", "DZ": "Alžírsko", "AS": "Americká Samoa",
    "VI": "Americké Panenské Ostrovy", "AD": "Andorra", "AO": "Angola", "AI": "Anguilla", "AQ": "Antarktida",
    "AG": "Antigua a Barbuda", "AR": "Argentina", "AM": "Arménie", "AW": "Aruba", "AU": "Austrálie",
    "AZ": "Ázerbájdžán", "ZZ": "Azory", "BS": "Bahamy", "BH": "Bahrajn", "BD": "Bangladéš",
    "BB": "Barbados", "BE": "Belgie", "BZ": "Belize", "BY": "Bělorusko", "BJ": "Benin",
    "BM": "Bermudy", "BT": "Bhútán", "BO": "Bolívie", "BA": "Bosna a Hercegovina", "BW": "Botswana",
    "BV": "Bouvetův Ostrov", "BR": "Brazílie", "IO": "Britské Indickoocéánské Území", "VG": "Britské Panenské Ostrovy", "BN": "Brunej",
    "BG": "Bulharsko", "BF": "Burkina Faso", "BI": "Burundi", "CK": "Cookovy Ostrovy", "TD": "Čad",
    "CZ": "Česká Republika", "CN": "Čína", "DK": "Dánsko", "CD": "Demokratická Republika Kongo", "DM": "Dominika",
    "DO": "Dominikánská Republika", "DJ": "Džibutsko", "EG": "Egypt", "EC": "Ekvádor", "ER": "Eritrea",
    "EE": "Estonsko", "ET": "Etiopie", "FO": "Faerské Ostrovy", "FK": "Falklandy", "FJ": "Fidži",
    "PH": "Filipíny", "FI": "Finsko", "FR": "Francie", "GF": "Francouzská Guyana", "TF": "Francouzská Jižní Území",
    "PF": "Francouzská Polynésie", "GA": "Gabon", "GM": "Gambie", "GH": "Ghana", "GI": "Gibraltar",
    "GD": "Grenada", "GL": "Grónsko", "GE": "Gruzie", "GP": "Guadeloupe", "GU": "Guam",
    "GT": "Guatemala", "GG": "Guernsey", "GN": "Guinea", "GW": "Guinea-Bissau", "GY": "Guyana",
    "HT": "Haiti", "HM": "Heardův Ostrov", "HN": "Honduras", "HK": "Hongkong", "CL": "Chile",
    "HR": "Chorvatsko", "IN": "Indie", "ID": "Indonésie", "IQ": "Irák", "IR": "Írán",
    "IE": "Irsko", "IS": "Island", "IT": "Itálie", "IL": "Izrael", "JM": "Jamajka",
    "JP": "Japonsko", "YE": "Jemen", "JE": "Jersey", "ZA": "Jihoafrická Republika", "GS": "Jižní Georgie",
    "KR": "Jižní Korea", "SS": "Jižní Súdán", "JO": "Jordánsko", "KY": "Kajmanské Ostrovy", "KH": "Kambodža",
    "CM": "Kamerun", "CA": "Kanada", "IC": "Kanárské Ostrovy", "CV": "Kapverdy", "QA": "Katar",
    "KZ": "Kazachstán", "KE": "Keňa", "KI": "Kiribati", "CC": "Kokosové Ostrovy", "CO": "Kolumbie",
    "KM": "Komory", "CG": "Kongo", "CR": "Kostarika", "CU": "Kuba", "KW": "Kuvajt",
    "CY": "Kypr", "KG": "Kyrgyzstán", "LA": "Laos", "LS": "Lesotho", "LB": "Libanon",
    "LR": "Libérie", "LY": "Libye", "LI": "Lichtenštejnsko", "LT": "Litva", "LV": "Lotyšsko",
    "LU": "Lucembursko", "MO": "Macao", "MG": "Madagaskar", "HU": "Maďarsko", "MK": "Makedonie",
    "MY": "Malajsie", "MW": "Malawi", "MV": "Maledivy", "ML": "Mali", "MT": "Malta",
    "MA": "Maroko", "MH": "Marshallovy Ostrovy", "MQ": "Martinik", "MU": "Mauricius", "MR": "Mauritánie",
    "YT": "Mayotte", "UM": "Menší Odlehlé Ostrovy USA", "MX": "Mexiko", "FM": "Mikronésie", "MD": "Moldavsko",
    "MC": "Monako", "MN": "Mongolsko", "MS": "Montserrat", "MZ": "Mosambik", "MM": "Myanmar",
    "NA": "Namibie", "NR": "Nauru", "DE": "Německo", "NP": "Nepál", "NE": "Niger",
    "NG": "Nigérie", "NI": "Nikaragua", "NU": "Niue", "AN": "Nizozemské Antily", "NL": "Nizozemsko",
    "NF": "Norfolk", "NO": "Norsko", "NC": "Nová Kaledonie", "NZ": "Nový Zéland", "OM": "Omán",
    "IM": "Ostrov Man", "PK": "Pákistán", "PW": "Palau", "PS": "Palestina", "PA": "Panama",
    "PG": "Papua-Nová Guinea", "PY": "Paraguay", "PE": "Peru", "PN": "Pitcairnovy Ostrovy", "PL": "Polsko",
    "PR": "Portoriko", "PT": "Portugalsko", "AT": "Rakousko", "RE": "Réunion", "GQ": "Rovníková Guinea",
    "RO": "Rumunsko", "RU": "Rusko", "RW": "Rwanda", "GR": "Řecko", "BL": "Saint-Barthelemy",
    "PM": "Saint-Pierre a Miquelon", "SV": "Salvador", "WS": "Samoa", "SM": "San Marino", "SA": "Saúdská Arábie",
    "SN": "Senegal", "KP": "Severní Korea", "MP": "Severní Mariany", "SC": "Seychely", "SL": "Sierra Leone",
    "SG": "Singapur", "SK": "Slovensko", "SI": "Slovinsko", "SO": "Somálsko", "AE": "Spojené Arabské Emiráty",
    "GB": "Spojené Království", "US": "Spojené Státy Americké", "RS": "Srbsko", "LK": "Srí Lanka", "CF": "Středoafrická Republika",
    "SR": "Surinam", "SH": "Svatá Helena", "LC": "Svatá Lucie", "KN": "Svatý Kryštof a Nevis", "ST": "Svatý Tomáš",
    "VC": "Svatý Vincenc", "SZ": "Svazijsko", "SY": "Sýrie", "SB": "Šalamounovy Ostrovy", "ES": "Španělsko",
    "SJ": "Špicberky", "SE": "Švédsko", "CH": "Švýcarsko", "TJ": "Tádžikistán", "TZ": "Tanzanie",
    "TH": "Thajsko", "TW": "Tchaj-wan", "TG": "Togo", "TK": "Tokelau", "TO": "Tonga",
    "TT": "Trinidad a Tobago", "TN": "Tunisko", "TR": "Turecko", "TM": "Turkmenistán", "TC": "Turks a Caicos",
    "TV": "Tuvalu", "UG": "Uganda", "UA": "Ukrajina", "UY": "Uruguay", "UZ": "Uzbekistán",
    "CX": "Vánoční Ostrov", "VU": "Vanuatu", "VA": "Vatikán", "VE": "Venezuela", "VN": "Vietnam",
    "TL": "Východní Timor", "WF": "Wallis a Futuna", "ZM": "Zambie", "ZW": "Zimbabwe"
}

# --- SLOVNÍK SLUŽEB ---
mapovani_sluzeb = {
    "101": "Classic", "109": "Classic + COD", "113": "Výměna",
    "155": "DPD 18:00 / Guarantee", "161": "DPD 18:00 dobírka", "164": "DPD 18:00 výměna",
    "179": "DPD 10:00", "191": "DPD 10:00 dobírka", "197": "DPD 10:00 výměna",
    "225": "DPD 12:00", "237": "DPD 12:00 dobírka", "243": "DPD 12:00 výměna",
    "302": "DPD EXPRESS", "327": "Private", "329": "Private + COD", 
    "332": "DPD RETURN", "337": "DPD PARCEL SHOP", "341": "DPD PARCEL SHOP dobírka", 
    "345": "SHOP2SHOP / PickupPoint", "365": "PNEU", "367": "PNEU dobírka", 
    "404": "SHOP2HOME", "415": "Dedicated Direct Truck Load", 
    "571": "Private výměna", "572": "Private dobírka výměna"
}

st.set_page_config(page_title="DPD Routing Dashboard", layout="wide", page_icon="🚚")
st.title("📦 DPD Routing Dashboard")

@st.cache_data(ttl=600)
def stahni_data_z_ftp():
    HOST, USER, PASS = "ftp-routing.dpd.cz", "custrouting", "65-K12_x-1"
    try:
        ftp = ftplib.FTP(HOST)
        ftp.login(USER, PASS)
        seznam = ftp.nlst()
        
        nejnovejsi = {}
        for s in seznam:
            if s.upper().startswith("ROUTING_"):
                parts = s.split('_')
                if len(parts) >= 3:
                    # Klíč je CZ_AD nebo CZ_SK
                    stat_key = f"{parts[1]}_{parts[2]}"
                    if stat_key not in nejnovejsi or s > nejnovejsi[stat_key]:
                        nejnovejsi[stat_key] = s
        
        vysledky = []
        for stat_key, soubor in sorted(nejnovejsi.items()):
            try:
                buffer = io.BytesIO()
                ftp.retrbinary(f"RETR {soubor}", buffer.write)
                buffer.seek(0)
                df = pd.read_csv(buffer, sep='|', comment='#', header=None, on_bad_lines='skip', low_memory=False)
                
                if not df.empty and df.shape[1] >= 6:
                    kody = df[5].dropna().unique()
                    nazvy = sorted(list(set([mapovani_sluzeb.get(str(int(float(str(k).strip()))), f"Kód {k}") for k in kody if str(k).strip().replace('.','').isdigit()])))
                    
                    # OPRAVA LOGIKY STÁTU: Vezmeme tu část, která NENÍ "CZ"
                    p = stat_key.split('_')
                    kod_pro_preklad = p[1] if p[0] == "CZ" and len(p) > 1 else p[0]
                    if kod_pro_preklad == "CZ" and len(p) > 1: kod_pro_preklad = p[1]
                    
                    plny_nazev = nazvy_statu.get(kod_pro_preklad.upper(), kod_pro_preklad)
                    
                    vysledky.append({"stat": plny_nazev, "soubor": soubor, "sluzby": nazvy})
            except: continue
        ftp.quit()
        return vysledky, None
    except Exception as e: return None, str(e)

st.info("🔄 Aktualizuji přehled z DPD serveru...")
data, chyba = stahni_data_z_ftp()

if chyba: st.error(f"❌ Chyba: {chyba}")
elif not data: st.warning("⚠️ Žádná data.")
else:
    # Přidání vyhledávání
    search = st.text_input("🔍 Vyhledat stát (např. Belgie nebo BE):")
    
    filtered_data = [d for d in data if search.lower() in d['stat'].lower() or search.upper() in d['soubor']]
    
    st.success(f"✅ Načteno {len(filtered_data)} destinací.")
    
    for i in range(0, len(filtered_data), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(filtered_data):
                item = filtered_data[i+j]
                with cols[j]:
                    with st.container(border=True):
                        st.subheader(f"🌍 {item['stat']}")
                        st.caption(f"Soubor: {item['soubor']}")
                        for s in item['sluzby']:
                            if "COD" in s: st.write(f"💰 **{s}**")
                            else: st.write(f"🔹 {s}")

if st.sidebar.button('🔄 Obnovit data'):
    st.cache_data.clear()
    st.rerun()