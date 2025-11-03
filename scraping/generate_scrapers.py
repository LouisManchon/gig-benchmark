#!/usr/bin/env python3
"""
Script pour générer automatiquement tous les scrapers pour football, tennis, basketball et rugby
"""

import os
import re

# =============================================================================
# DONNÉES : Football (91 compétitions)
# =============================================================================
football_competitions = [
    {"name": "Coupe de France", "url": "https://www.coteur.com/cotes/foot/france/coupe-de-france"},
    {"name": "Ligue 1", "url": "https://www.coteur.com/cotes/foot/france/ligue-1"},
    {"name": "Ligue 2", "url": "https://www.coteur.com/cotes/foot/france/ligue-2"},
    {"name": "Division 1 Algérie", "url": "https://www.coteur.com/cotes/foot/algerie/division-1-1"},
    {"name": "Bundesliga 2", "url": "https://www.coteur.com/cotes/foot/allemagne/bundesliga-2"},
    {"name": "Bundesliga", "url": "https://www.coteur.com/cotes/foot/allemagne/bundesliga-d1"},
    {"name": "Pokal Cup", "url": "https://www.coteur.com/cotes/foot/allemagne/pokal-cup"},
    {"name": "Copa Libertadores", "url": "https://www.coteur.com/cotes/foot/amerique-du-sud/copa-libertadores"},
    {"name": "Qualif WC Amérique du Sud", "url": "https://www.coteur.com/cotes/foot/amerique-du-sud/qualification-coupe-du-monde-zone-amsud"},
    {"name": "FA Cup", "url": "https://www.coteur.com/cotes/foot/angleterre/fa-cup"},
    {"name": "League Cup EFL", "url": "https://www.coteur.com/cotes/foot/angleterre/league-cup-efl"},
    {"name": "Premier League", "url": "https://www.coteur.com/cotes/foot/angleterre/premier-league"},
    {"name": "Championship", "url": "https://www.coteur.com/cotes/foot/angleterre/the-championship"},
    {"name": "Community Shield", "url": "https://www.coteur.com/cotes/foot/angleterre/community-shield"},
    {"name": "Saudi Pro League", "url": "https://www.coteur.com/cotes/foot/arabie-saoudite/saudi-pro-league"},
    {"name": "Primera Division Argentine", "url": "https://www.coteur.com/cotes/foot/argentine/primera-division-2"},
    {"name": "A-League", "url": "https://www.coteur.com/cotes/foot/australie/a-league"},
    {"name": "Bundesliga Autriche", "url": "https://www.coteur.com/cotes/foot/autriche/bundesliga"},
    {"name": "Première Division Azerbaïdjan", "url": "https://www.coteur.com/cotes/foot/azerbaidjan/premiere-division-1"},
    {"name": "Jupiler Pro Ligue", "url": "https://www.coteur.com/cotes/foot/belgique/jupiler-pro-ligue"},
    {"name": "Premier Liga Bosnie", "url": "https://www.coteur.com/cotes/foot/bosnie-herzegovine/premier-liga-1"},
    {"name": "A PFG", "url": "https://www.coteur.com/cotes/foot/bulgarie/a-pfg"},
    {"name": "Primera Division Chili", "url": "https://www.coteur.com/cotes/foot/chili/primera-division-4"},
    {"name": "1ère division Chypre", "url": "https://www.coteur.com/cotes/foot/chypre/1ere-division"},
    {"name": "Liga Postobon I", "url": "https://www.coteur.com/cotes/foot/colombie/liga-postobon-i"},
    {"name": "K-League 1", "url": "https://www.coteur.com/cotes/foot/coree-du-sud/k-league-1"},
    {"name": "1.HNL", "url": "https://www.coteur.com/cotes/foot/croatie/1-hnl"},
    {"name": "Superligaen", "url": "https://www.coteur.com/cotes/foot/danemark/superligaen"},
    {"name": "Premiership Ecosse", "url": "https://www.coteur.com/cotes/foot/ecosse/premiership"},
    {"name": "Série A Equateur", "url": "https://www.coteur.com/cotes/foot/equateur/serie-a-3"},
    {"name": "Coupe du roi", "url": "https://www.coteur.com/cotes/foot/espagne/coupe-du-roi"},
    {"name": "Liga Adelante", "url": "https://www.coteur.com/cotes/foot/espagne/liga-adelante"},
    {"name": "La Liga", "url": "https://www.coteur.com/cotes/foot/espagne/liga-bbva"},
    {"name": "Meistriliiga", "url": "https://www.coteur.com/cotes/foot/estonie/meistriliiga"},
    {"name": "Major League Soccer", "url": "https://www.coteur.com/cotes/foot/etats-unis/major-league-soccer"},
    {"name": "Ligue Europa", "url": "https://www.coteur.com/cotes/foot/europe/ligue-europa-1"},
    {"name": "Ligue des Nations", "url": "https://www.coteur.com/cotes/foot/europe/ligue-des-nations"},
    {"name": "Champions League", "url": "https://www.coteur.com/cotes/foot/europe/ligue-des-champions"},
    {"name": "UEFA Conference League", "url": "https://www.coteur.com/cotes/foot/europe/uefa-conference-league"},
    {"name": "Super League Grèce", "url": "https://www.coteur.com/cotes/foot/grece/super-league-2"},
    {"name": "NB I Hongrie", "url": "https://www.coteur.com/cotes/foot/hongrie/nb-i"},
    {"name": "Premiership Irlande du Nord", "url": "https://www.coteur.com/cotes/foot/irlande-du-nord/premiership-2"},
    {"name": "Winner League", "url": "https://www.coteur.com/cotes/foot/israel/winner-league"},
    {"name": "Coupe d'Italie", "url": "https://www.coteur.com/cotes/foot/italie/coupe-ditalie"},
    {"name": "Serie A", "url": "https://www.coteur.com/cotes/foot/italie/serie-a"},
    {"name": "Serie B", "url": "https://www.coteur.com/cotes/foot/italie/serie-b"},
    {"name": "J. League", "url": "https://www.coteur.com/cotes/foot/japon/j-league"},
    {"name": "Virsliga", "url": "https://www.coteur.com/cotes/foot/lettonie/virsliga"},
    {"name": "A Lyga", "url": "https://www.coteur.com/cotes/foot/lituanie/a-lyga"},
    {"name": "BOV Premier Division", "url": "https://www.coteur.com/cotes/foot/malte/bov-premier-division"},
    {"name": "Super League Maroc", "url": "https://www.coteur.com/cotes/foot/maroc/super-league-1"},
    {"name": "Liga MX", "url": "https://www.coteur.com/cotes/foot/mexique/primera-division-5"},
    {"name": "CONCACAF Ligue des Nations", "url": "https://www.coteur.com/cotes/foot/monde/concacaf-ligue-des-nations"},
    {"name": "Qualif WC Europe", "url": "https://www.coteur.com/cotes/foot/monde/qualifications-coupe-du-monde-europe"},
    {"name": "Eliteserien", "url": "https://www.coteur.com/cotes/foot/norvege/eliteserien"},
    {"name": "Primera Division Paraguay", "url": "https://www.coteur.com/cotes/foot/paraguay/primera-division-1"},
    {"name": "League Of Wales", "url": "https://www.coteur.com/cotes/foot/pays-de-galles/league-of-wales"},
    {"name": "Casino Eredivisie", "url": "https://www.coteur.com/cotes/foot/pays-bas/casino-eredivisie"},
    {"name": "Orange Ekstraklasa", "url": "https://www.coteur.com/cotes/foot/pologne/orange-ekstraklasa"},
    {"name": "Liga 2 Cabovisao", "url": "https://www.coteur.com/cotes/foot/portugal/liga-2-cabovisao"},
    {"name": "Primeira Liga", "url": "https://www.coteur.com/cotes/foot/portugal/primeira-liga"},
    {"name": "Premier Division Irlande", "url": "https://www.coteur.com/cotes/foot/rep-dirlande/premier-division"},
    {"name": "Liga 1 Roumanie", "url": "https://www.coteur.com/cotes/foot/roumanie/liga-1"},
    {"name": "HET Liga", "url": "https://www.coteur.com/cotes/foot/republique-tcheque/het-liga"},
    {"name": "Super League Serbie", "url": "https://www.coteur.com/cotes/foot/serbie/super-league-3"},
    {"name": "Superliga Slovaquie", "url": "https://www.coteur.com/cotes/foot/slovaquie/superliga-1"},
    {"name": "PrvaLiga", "url": "https://www.coteur.com/cotes/foot/slovenie/prvaliga"},
    {"name": "Super League Suisse", "url": "https://www.coteur.com/cotes/foot/suisse/super-league"},
    {"name": "Allsvenskan", "url": "https://www.coteur.com/cotes/foot/suede/allsvenskan"},
    {"name": "Super Ligi", "url": "https://www.coteur.com/cotes/foot/turquie/super-ligi"},
    {"name": "Premier Liga Ukraine", "url": "https://www.coteur.com/cotes/foot/ukraine/premier-liga"},
    {"name": "Qualif WC Afrique", "url": "https://www.coteur.com/cotes/foot/afrique/coupe-du-monde-qualifications-afrique"},
    {"name": "Qualif WC Asie", "url": "https://www.coteur.com/cotes/foot/asie/qualification-coupe-du-monde-asie"},
    {"name": "Asian Champions League", "url": "https://www.coteur.com/cotes/foot/monde-1/ldc-dasie-phase-finale"},
    {"name": "Erovnuli Liga", "url": "https://www.coteur.com/cotes/foot/georgie/erovnuli-liga"},
    {"name": "Veikkausliiga", "url": "https://www.coteur.com/cotes/foot/finlande/veikkausliiga"},
    {"name": "Urvalsdeild", "url": "https://www.coteur.com/cotes/foot/islande/urvalsdeild"},
    {"name": "Coupe du monde des Clubs", "url": "https://www.coteur.com/cotes/foot/monde/coupe-du-monde-des-clubs"},
    {"name": "Copa Sudamericana", "url": "https://www.coteur.com/cotes/foot/amerique-du-sud/copa-sudamericana"},
    {"name": "Brasileirao", "url": "https://www.coteur.com/cotes/foot/bresil/serie-a-1"},
    {"name": "Ligue des Nations F", "url": "https://www.coteur.com/cotes/foot/europe/europe-ligue-des-nations-f"},
    {"name": "Amical International W", "url": "https://www.coteur.com/cotes/foot/monde/matches-amicaux-internationaux-f"},
    {"name": "Amical International", "url": "https://www.coteur.com/cotes/foot/monde/international-matchs-amicaux"},
    {"name": "Qualif WC CONCACAF", "url": "https://www.coteur.com/cotes/foot/amerique/qualification-coupe-du-monde-concacaf"},
    {"name": "Euro U21 Qualif", "url": "https://www.coteur.com/cotes/foot/europe/championnat-deurope-u21-qualification"},
    {"name": "Super League Chine", "url": "https://www.coteur.com/cotes/foot/chine/super-league-5"},
    {"name": "Euro Femmes", "url": "https://www.coteur.com/cotes/foot/europe/euro-femmes"},
    {"name": "CONCACAF Gold Cup", "url": "https://www.coteur.com/cotes/foot/amerique/concacaf-gold-cup"},
    {"name": "Leagues Cup", "url": "https://www.coteur.com/cotes/foot/monde-1/international-leagues-cup"},
    {"name": "BGL Ligue", "url": "https://www.coteur.com/cotes/foot/luxembourg/bgl-ligue"},
    {"name": "Ligue des Champions F", "url": "https://www.coteur.com/cotes/foot/europe/ligue-des-champions-f"},
    {"name": "Coupe d'Asie", "url": "https://www.coteur.com/cotes/foot/asie/coupe-dasie-des-nations"},
]

# =============================================================================
# DONNÉES : Tennis (89 compétitions)
# =============================================================================
tennis_competitions = [
    {"name": "ATP Miami", "url": "https://www.coteur.com/cotes/tennis/monde/atp-masters-miami"},
    {"name": "WTA Miami", "url": "https://www.coteur.com/cotes/tennis/monde/wta-miami"},
    {"name": "ATP Bucharest", "url": "https://www.coteur.com/cotes/tennis/monde/atp-bucarest"},
    {"name": "ATP Houston", "url": "https://www.coteur.com/cotes/tennis/monde/atp-houston"},
    {"name": "ATP Marrakech", "url": "https://www.coteur.com/cotes/tennis/monde/atp-marrakech"},
    {"name": "WTA Bogota", "url": "https://www.coteur.com/cotes/tennis/monde/wta-bogota"},
    {"name": "WTA Charleston", "url": "https://www.coteur.com/cotes/tennis/monde/wta-charleston"},
    {"name": "ATP Monte-Carlo", "url": "https://www.coteur.com/cotes/tennis/monde/masters-atp-monte-carlo"},
    {"name": "ATP Barcelone", "url": "https://www.coteur.com/cotes/tennis/monde/atp-barcelone"},
    {"name": "ATP Munich", "url": "https://www.coteur.com/cotes/tennis/monde/atp-munich"},
    {"name": "WTA Rouen", "url": "https://www.coteur.com/cotes/tennis/monde-1/wta-rouen"},
    {"name": "WTA Stuttgart", "url": "https://www.coteur.com/cotes/tennis/monde/wta-stuttgart"},
    {"name": "WTA Madrid", "url": "https://www.coteur.com/cotes/tennis/monde/wta-madrid"},
    {"name": "ATP Madrid", "url": "https://www.coteur.com/cotes/tennis/monde/masters-madrid"},
    {"name": "ATP Rome", "url": "https://www.coteur.com/cotes/tennis/monde/masters-atp-rome"},
    {"name": "WTA Rome", "url": "https://www.coteur.com/cotes/tennis/monde/wta-rome"},
    {"name": "WTA Strasbourg", "url": "https://www.coteur.com/cotes/tennis/monde/wta-strasbourg"},
    {"name": "WTA Rabat", "url": "https://www.coteur.com/cotes/tennis/monde/wta-rabat"},
    {"name": "ATP Geneve", "url": "https://www.coteur.com/cotes/tennis/monde/atp-geneve"},
    {"name": "ATP Hambourg", "url": "https://www.coteur.com/cotes/tennis/monde/atp-hambourg"},
    {"name": "Roland-Garros M", "url": "https://www.coteur.com/cotes/tennis/monde/atp-roland-garros"},
    {"name": "Roland-Garros W", "url": "https://www.coteur.com/cotes/tennis/monde/wta-roland-garros"},
    {"name": "Roland-Garros Doubles M", "url": "https://www.coteur.com/cotes/tennis/monde/atp-roland-garros-doubles"},
    {"name": "Roland-Garros Doubles W", "url": "https://www.coteur.com/cotes/tennis/monde/wta-roland-garros-doubles"},
    {"name": "Roland-Garros Doubles X", "url": "https://www.coteur.com/cotes/tennis/monde/atp-roland-garros-doubles-mixte"},
    {"name": "WTA Londres", "url": "https://www.coteur.com/cotes/tennis/monde-1/wta-londres"},
    {"name": "ATP Hertogenbosch", "url": "https://www.coteur.com/cotes/tennis/monde/atp-s-hertogenbosch"},
    {"name": "WTA Hertogenbosch", "url": "https://www.coteur.com/cotes/tennis/monde/wta-s-hertogenbosch"},
    {"name": "ATP Stuttgart", "url": "https://www.coteur.com/cotes/tennis/monde/atp-stuttgart"},
    {"name": "ATP London", "url": "https://www.coteur.com/cotes/tennis/monde/atp-londres-queens"},
    {"name": "ATP Halle", "url": "https://www.coteur.com/cotes/tennis/monde/atp-halle"},
    {"name": "WTA Berlin", "url": "https://www.coteur.com/cotes/tennis/monde/wta-berlin"},
    {"name": "WTA Nottingham", "url": "https://www.coteur.com/cotes/tennis/monde/wta-nottingham"},
    {"name": "ATP Majorque", "url": "https://www.coteur.com/cotes/tennis/monde/atp-majorque"},
    {"name": "ATP Eastbourne", "url": "https://www.coteur.com/cotes/tennis/monde/atp-eastbourne"},
    {"name": "WTA Bad Homburg", "url": "https://www.coteur.com/cotes/tennis/monde/wta-bad-homburg"},
    {"name": "WTA Eastbourne", "url": "https://www.coteur.com/cotes/tennis/monde/wta-eastbourne"},
    {"name": "ATP Wimbledon", "url": "https://www.coteur.com/cotes/tennis/monde/wimbledon-simples-hommes"},
    {"name": "WTA Wimbledon", "url": "https://www.coteur.com/cotes/tennis/monde/wimbledon-simples-dames"},
    {"name": "Wimbledon Double M", "url": "https://www.coteur.com/cotes/tennis/monde/wimbledon-doubles-hommes"},
    {"name": "Wimbledon Double W", "url": "https://www.coteur.com/cotes/tennis/monde/wimbledon-doubles-dames"},
    {"name": "Wimbledon Double X", "url": "https://www.coteur.com/cotes/tennis/monde/atp-wimbledon-doubles-mixte"},
    {"name": "ATP Los Cabos", "url": "https://www.coteur.com/cotes/tennis/monde/atp-los-cabos"},
    {"name": "ATP Bastad", "url": "https://www.coteur.com/cotes/tennis/monde/atp-bastad"},
    {"name": "ATP Gstaad", "url": "https://www.coteur.com/cotes/tennis/monde/atp-gstaad"},
    {"name": "WTA Iasi", "url": "https://www.coteur.com/cotes/tennis/monde-1/wta-iasi"},
    {"name": "WTA Hamburg", "url": "https://www.coteur.com/cotes/tennis/monde/wta-hambourg"},
    {"name": "ATP Kitzbuhel", "url": "https://www.coteur.com/cotes/tennis/monde/atp-kitzbuhel-1"},
    {"name": "WTA Prague", "url": "https://www.coteur.com/cotes/tennis/monde/wta-prague"},
    {"name": "ATP Umag", "url": "https://www.coteur.com/cotes/tennis/monde/atp-umag"},
    {"name": "ATP Washington", "url": "https://www.coteur.com/cotes/tennis/monde/atp-washington"},
    {"name": "WTA Washington", "url": "https://www.coteur.com/cotes/tennis/monde/wta-washington"},
    {"name": "WTA Montreal", "url": "https://www.coteur.com/cotes/tennis/monde/wta-montreal"},
    {"name": "ATP Toronto", "url": "https://www.coteur.com/cotes/tennis/monde/atp-toronto"},
    {"name": "ATP Cincinnati", "url": "https://www.coteur.com/cotes/tennis/monde/masters-cincinnati"},
    {"name": "WTA Cincinnati", "url": "https://www.coteur.com/cotes/tennis/monde/wta-cincinnati"},
    {"name": "WTA Monterrey", "url": "https://www.coteur.com/cotes/tennis/monde/wta-monterrey"},
    {"name": "ATP Winston-Salem", "url": "https://www.coteur.com/cotes/tennis/monde/atp-winston-salem"},
    {"name": "WTA Cleveland", "url": "https://www.coteur.com/cotes/tennis/monde/wta-cleveland"},
    {"name": "ATP US Open", "url": "https://www.coteur.com/cotes/tennis/monde/us-open"},
    {"name": "WTA US Open", "url": "https://www.coteur.com/cotes/tennis/monde/us-open-femmes"},
    {"name": "ATP US Open - Double", "url": "https://www.coteur.com/cotes/tennis/monde/us-open-double-hommes"},
    {"name": "WTA US Open - Double", "url": "https://www.coteur.com/cotes/tennis/monde/us-open-doubles-femmes"},
    {"name": "WTA Guadalajara", "url": "https://www.coteur.com/cotes/tennis/monde/wta-guadalajara"},
    {"name": "WTA Sao Paulo", "url": "https://www.coteur.com/cotes/tennis/monde-1/wta-sao-paulo"},
    {"name": "Coupe Davis", "url": "https://www.coteur.com/cotes/tennis/monde/coupe-davis"},
    {"name": "WTA Séoul", "url": "https://www.coteur.com/cotes/tennis/monde/wta-seoul"},
    {"name": "ATP Chengdu", "url": "https://www.coteur.com/cotes/tennis/monde/atp-chengdu"},
    {"name": "ATP Hangzhou", "url": "https://www.coteur.com/cotes/tennis/monde-1/atp-hangzhou"},
    {"name": "WTA Pékin", "url": "https://www.coteur.com/cotes/tennis/monde/wta-pekin"},
    {"name": "ATP Tokyo", "url": "https://www.coteur.com/cotes/tennis/monde/atp-tokyo"},
    {"name": "ATP Pékin", "url": "https://www.coteur.com/cotes/tennis/monde/atp-pekin"},
    {"name": "ATP Shanghai", "url": "https://www.coteur.com/cotes/tennis/monde/masters-shanghai"},
    {"name": "WTA Wuhan", "url": "https://www.coteur.com/cotes/tennis/monde/wta-wuhan"},
    {"name": "ATP Almaty", "url": "https://www.coteur.com/cotes/tennis/monde-1/atp-almaty"},
    {"name": "ATP Bruxelles", "url": "https://www.coteur.com/cotes/tennis/monde-1/atp-bruxelles"},
    {"name": "ATP Stockholm", "url": "https://www.coteur.com/cotes/tennis/monde/atp-stockholm"},
    {"name": "WTA Osaka", "url": "https://www.coteur.com/cotes/tennis/monde/wta-osaka"},
    {"name": "WTA Ningbo", "url": "https://www.coteur.com/cotes/tennis/monde/wta-ningbo"},
    {"name": "WTA Tokyo", "url": "https://www.coteur.com/cotes/tennis/monde/wta-tokyo"},
    {"name": "ATP Vienne", "url": "https://www.coteur.com/cotes/tennis/monde/atp-vienne"},
    {"name": "ATP Basel", "url": "https://www.coteur.com/cotes/tennis/monde/atp-bale"},
    {"name": "WTA Guangzhou", "url": "https://www.coteur.com/cotes/tennis/monde/wta-guangzhou"},
    {"name": "ATP Paris", "url": "https://www.coteur.com/cotes/tennis/monde/masters-paris"},
    {"name": "WTA Chennai", "url": "https://www.coteur.com/cotes/tennis/monde/wta-chennai"},
    {"name": "WTA Hong Kong", "url": "https://www.coteur.com/cotes/tennis/monde/wta-hong-kong"},
    {"name": "WTA Jiujiang", "url": "https://www.coteur.com/cotes/tennis/monde-1/wta-jiujiang"},
    {"name": "WTA Finals (Riyadh)", "url": "https://www.coteur.com/cotes/tennis/monde-1/wta-finals"},
    {"name": "ATP Athens", "url": "https://www.coteur.com/cotes/tennis/monde-1/atp-athenes"},
]

# =============================================================================
# DONNÉES : Basketball (14 compétitions)
# =============================================================================
basketball_competitions = [
    {"name": "NBA", "url": "https://www.coteur.com/cotes/basket/etats-unis/nba"},
    {"name": "Bundesliga", "url": "https://www.coteur.com/cotes/basket/allemagne/bundesliga-1"},
    {"name": "NBL", "url": "https://www.coteur.com/cotes/basket/australie/nbl"},
    {"name": "Euroligue", "url": "https://www.coteur.com/cotes/basket/europe/euroligue"},
    {"name": "Eurocup", "url": "https://www.coteur.com/cotes/basket/europe/eurocup-hommes"},
    {"name": "League ABA", "url": "https://www.coteur.com/cotes/basket/europe/nlb-league-aba"},
    {"name": "Euroligue Women", "url": "https://www.coteur.com/cotes/basket/europe/euroligue-femmes"},
    {"name": "Coupe d'Europe FIBA", "url": "https://www.coteur.com/cotes/basket/europe/coupe-deurope-fiba"},
    {"name": "Eurocup Women", "url": "https://www.coteur.com/cotes/basket/europe/eurocoupe-f"},
    {"name": "Ligue des Champions", "url": "https://www.coteur.com/cotes/basket/europe/ligue-des-champions-2"},
    {"name": "Betclic Elite", "url": "https://www.coteur.com/cotes/basket/france/pro-a"},
    {"name": "A1", "url": "https://www.coteur.com/cotes/basket/grece/a1-hommes"},
    {"name": "Lega A", "url": "https://www.coteur.com/cotes/basket/italie/lega-a"},
    {"name": "Serie A2", "url": "https://www.coteur.com/cotes/basket/italie/serie-a2"},
]

# =============================================================================
# DONNÉES : Rugby (3 compétitions)
# =============================================================================
rugby_competitions = [
    {"name": "Top 14", "url": "https://www.coteur.com/cotes/rugby/france/top-14"},
    {"name": "Pro D2", "url": "https://www.coteur.com/cotes/rugby/france/pro-d2"},
    {"name": "Test-Match", "url": "https://www.coteur.com/cotes/rugby/monde/international-test-match"},
]


def slugify(text):
    """Convertit un nom en slug pour nom de fichier"""
    # Enlever les accents et caractères spéciaux
    text = text.lower()
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[àâä]', 'a', text)
    text = re.sub(r'[îï]', 'i', text)
    text = re.sub(r'[ôö]', 'o', text)
    text = re.sub(r'[ùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)

    # Remplacer les espaces et caractères spéciaux par des underscores
    text = re.sub(r'[^a-z0-9]+', '_', text)

    # Enlever les underscores multiples et ceux en début/fin
    text = re.sub(r'_+', '_', text)
    text = text.strip('_')

    return text


def generate_scraper_file(sport, comp):
    """Génère un fichier scraper pour une compétition"""
    filename = slugify(comp['name'])
    function_name = f"scrape_{filename}"

    content = f"""# scraping/src/{sport}/{filename}.py

from ._scraper_utils import scrape_league


def {function_name}():
    \"\"\"Scrape {comp['name']}\"\"\"
    return scrape_league(
        league_name="{comp['name']}",
        league_url="{comp['url']}",
        display_name="{comp['name']}"
    )
"""

    return filename, content, function_name


def main():
    print("\n" + "="*60)
    print("GÉNÉRATION DES SCRAPERS")
    print("="*60)

    sports = {
        'football': football_competitions,
        'tennis': tennis_competitions,
        'basketball': basketball_competitions,
        'rugby': rugby_competitions
    }

    total_created = 0
    all_scrapers_info = {}

    for sport, competitions in sports.items():
        print(f"\n{sport.upper()} ({len(competitions)} compétitions)")
        print("-" * 60)

        output_dir = f"src/{sport}"
        scrapers_info = []

        # Créer le dossier s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)

        for comp in competitions:
            filename, content, function_name = generate_scraper_file(sport, comp)

            # Créer le fichier
            filepath = os.path.join(output_dir, f"{filename}.py")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"{filename}.py")
            total_created += 1

            scrapers_info.append({
                'filename': filename,
                'function_name': function_name,
                'display_name': comp['name'],
                'scraper_key': f"{sport}.{filename}"
            })

        all_scrapers_info[sport] = scrapers_info

    print("\n" + "="*60)
    print(f"RÉSUMÉ")
    print("="*60)
    print(f"Football: {len(football_competitions)} fichiers")
    print(f"Tennis: {len(tennis_competitions)} fichiers")
    print(f"Basketball: {len(basketball_competitions)} fichiers")
    print(f"Rugby: {len(rugby_competitions)} fichiers")
    print(f"TOTAL: {total_created} fichiers créés")
    print("="*60 + "\n")

    # Sauvegarder les informations pour worker.py
    print("Sauvegarde des informations pour worker.py et tasks.py...")
    with open('/tmp/all_scrapers_info.txt', 'w', encoding='utf-8') as f:
        f.write("# " + "="*60 + "\n")
        f.write("# IMPORTS POUR WORKER.PY\n")
        f.write("# " + "="*60 + "\n\n")

        for sport, scrapers in all_scrapers_info.items():
            f.write(f"\n# {sport.upper()}\n")
            for info in scrapers:
                f.write(f"from src.{sport}.{info['filename']} import {info['function_name']}\n")

        f.write("\n\n# " + "="*60 + "\n")
        f.write("# REGISTRY POUR WORKER.PY\n")
        f.write("# " + "="*60 + "\n\n")

        for sport, scrapers in all_scrapers_info.items():
            f.write(f"\n# {sport.upper()}\n")
            for info in scrapers:
                f.write(f"SCRAPERS_REGISTRY['{info['scraper_key']}'] = {info['function_name']}\n")

        f.write("\n\n# " + "="*60 + "\n")
        f.write("# LISTE POUR TASKS.PY\n")
        f.write("# " + "="*60 + "\n\n")

        f.write("leagues = [\n")
        for sport, scrapers in all_scrapers_info.items():
            f.write(f"\n    # {sport.upper()}\n")
            for info in scrapers:
                f.write(f"    '{info['scraper_key']}',\n")
        f.write("]\n")

    print("Informations sauvegardées dans /tmp/all_scrapers_info.txt")
    print("\nVous pouvez maintenant mettre à jour worker.py et tasks.py avec ces informations.")


if __name__ == "__main__":
    main()
