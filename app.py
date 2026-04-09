import streamlit as st
import pandas as pd
import ftplib
import io

# --- SLOVNÍKY ---
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

# --- AKTUALIZOVANÝ SLOVNÍK SLUŽEB ---
mapovani_sluzeb = {
    "101": "Classic", 
    "109": "Classic + COD", 
    "113": "Výměna",
    "155": "DPD 18:00 / Guarantee", 
    "161": "DPD 18:00 dobírka", 
    "164": "DPD 18:00 výměna",
    "179": "DPD 10:00", 
    "191": "DPD 10:00 dobírka", 
    "197": "DPD 10:00 výměna",
    "225": "DPD 12:00", 
    "237": "DPD 12:00 dobírka", 
    "243": "DPD 12:00 výměna",
    "302": "DPD EXPRESS", 
    "327": "Private", 
    "329": "Private + COD", 
    "332": "DPD RETURN", 
    "337": "DPD ParcelShop", 
    "341": "DPD ParcelShop dobírka", 
    "345": "SHOP2SHOP / PickupPoint", 
    "365": "PNEU", 
    "367": "PNEU dobírka", 
    "404": "SHOP2HOME", 
    "415": "Dedicated Direct Truck Load", 
    "571": "Private výměna (legacy)", 
    "572": "Private dobírka výměna (legacy)",
    "827": "Private výměna",
    "829": "Private sobotní doručení",
    "831": "Private sobotní doručení + COD",
    "835": "Private výměna + COD",
    "839": "Private večerní doručení",
    "841": "Private večerní doručení + COD"
}

st.set_page_config(page_title="DPD Routing Dashboard", layout="wide", page_icon="🚚")
st.title("📦 DPD Routing Dashboard")

# --- FTP SPOJENÍ ---
@st.cache_data(ttl=600)
def ziskej_seznam_souboru():
    try:
        ftp = ftplib.FTP("ftp-routing.dpd.cz")
        ftp.login("custrouting", "65-K12_x-1")
        seznam = ftp.nlst()
        nejnovejsi = {}
        for s in seznam:
            if s.upper().startswith("ROUTING_"):
                parts = s.split('_')
                if len(parts) >= 3:
                    stat_key = f"{parts[1]}_{parts[2]}"
                    if stat_key not in nejnovejsi or s > nejnovejsi[stat_key]:
                        nejnovejsi[stat_key] = s
        ftp.quit()
        return nejnovejsi, None
    except Exception as e: return None, str(e)

@st.cache_data(ttl=600)
def nacti_df(soubor):
    try:
        ftp = ftplib.FTP("ftp-routing.dpd.cz")
        ftp.login("custrouting", "65-K12_x-1")
        buffer = io.BytesIO()
        ftp.retrbinary(f"RETR {soubor}", buffer.write)
        ftp.quit()
        buffer.seek(0)
        return pd.read_csv(buffer, sep='|', comment='#', header=None, on_bad_lines='skip', low_memory=False)
    except: return None

# --- START ---
seznam_souboru, chyba = ziskej_seznam_souboru()

if chyba:
    st.error(f"❌ Chyba připojení k FTP: {chyba}")
else:
    # --- SEKCE 1: VYHLEDÁVAČ PSČ ---
    st.header("🔎 1. Ověření dostupnosti podle PSČ")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            seznam_statu = sorted([(k.split('_')[1], nazvy_statu.get(k.split('_')[1], k)) for k in seznam_souboru.keys()], key=lambda x: x[1])
            index_cz = next((i for i, s in enumerate(seznam_statu) if s[0] == "CZ"), 0)
            vybrany_stat = st.selectbox("Vyber cílový stát:", seznam_statu, index=index_cz, format_func=lambda x: x[1])
        with c2:
            vstup_psc = st.text_input("Zadej PSČ (např. 25401):", "").replace(" ", "")

        if vstup_psc:
            soubor = seznam_souboru.get(f"CZ_{vybrany_stat[0]}")
            if soubor:
                df = nacti_df(soubor)
                if df is not None:
                    try:
                        if vstup_psc.isdigit():
                            vstup_num = float(vstup_psc)
                            zip_from_num = pd.to_numeric(df[3], errors='coerce')
                            zip_to_num = pd.to_numeric(df[4], errors='coerce')
                            match = df[(zip_from_num <= vstup_num) & (zip_to_num >= vstup_num)]
                        else:
                            vstup_str = str(vstup_psc).upper()
                            match = df[(df[3].astype(str).str.upper() <= vstup_str) & (df[4].astype(str).str.upper() >= vstup_str)]

                        if not match.empty:
                            kody = match[5].dropna().unique()
                            st.success(f"✅ Pro PSČ **{vstup_psc}** ({vybrany_stat[1]}) jsou dostupné tyto služby:")
                            cols = st.columns(4)
                            for idx, k in enumerate(kody):
                                k_str = str(int(float(str(k).strip())))
                                nazev = mapovani_sluzeb.get(k_str, f"Kód {k_str}")
                                with cols[idx % 4]:
                                    st.info(f"**{nazev}**")
                        else:
                            st.warning(f"⚠️ Pro PSČ {vstup_psc} v zemi {vybrany_stat[1]} nebyla nalezena žádná specifická pravidla.")
                        
                        with st.expander("Zobrazit data ze souboru (pro kontrolu)"):
                            st.dataframe(match.head(15))

                    except Exception as e:
                        st.error(f"Chyba při zpracování: {e}")
            else:
                st.error(f"Soubor pro směr CZ -> {vybrany_stat[0]} nebyl nalezen.")

    st.markdown("---")

    # --- SEKCE 2 + 3: FILTR A KARTY ---
    st.header("📋 2. Filtr a 🌍 3. Přehled států")
    search_query = st.text_input("Napiš název státu pro odfiltrování karet:")
    
    filtr_klicu = []
    for klic, soubor in seznam_souboru.items():
        kod_zeme = klic.split('_')[1]
        nazev_zeme = nazvy_statu.get(kod_zeme, kod_zeme)
        if search_query.lower() in nazev_zeme.lower() or search_query.upper() in kod_zeme:
            filtr_klicu.append((klic, soubor, nazev_zeme))

    if filtr_klicu:
        vysledky_karty = []
        with st.status("Načítám přehled států...", expanded=False) as status:
            for idx, (klic, soubor, nazev) in enumerate(filtr_klicu):
                df_karta = nacti_df(soubor)
                if df_karta is not None:
                    kody = df_karta[5].dropna().unique()
                    sluzby = sorted(list(set([mapovani_sluzeb.get(str(int(float(str(k).strip()))), f"Kód {k}") for k in kody if str(k).strip().replace('.','').isdigit()])))
                    vysledky_karty.append({"stat": nazev, "soubor": soubor, "sluzby": sluzby})
            status.update(label="Načteno!", state="complete")

        for i in range(0, len(vysledky_karty), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(vysledky_karty):
                    item = vysledky_karty[i+j]
                    with cols[j]:
                        with st.container(border=True):
                            st.subheader(f"{item['stat']}")
                            for s in item['sluzby']:
                                if "COD" in s: st.write(f"💰 **{s}**")
                                else: st.write(f"🔹 {s}")

if st.sidebar.button('🔄 Obnovit data z FTP'):
    st.cache_data.clear()
    st.rerun()
