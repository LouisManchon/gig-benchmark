"""
Worker principal pour le système de scraping multi-sports
Écoute RabbitMQ et dispatche vers les scrapers appropriés

Supporte tous les sports : Football (105), Basketball (15), Rugby (3), Tennis (89)
Total: 212 scrapers
"""
import os
import sys
import time
import json
import pika
import traceback
from typing import Dict, Callable

sys.path.insert(0, '/app')

print("Chargement des scrapers...")

# ============================================================================
# IMPORTS DES SCRAPERS (212 total)
# ============================================================================
scrapers_loaded = []
scrapers_failed = []

# FOOTBALL
from src.football.coupe_de_france import scrape_coupe_de_france
from src.football.ligue_1 import scrape_ligue_1
from src.football.ligue_2 import scrape_ligue_2
from src.football.division_1_algerie import scrape_division_1_algerie
from src.football.bundesliga_2 import scrape_bundesliga_2
from src.football.bundesliga import scrape_bundesliga
from src.football.pokal_cup import scrape_pokal_cup
from src.football.copa_libertadores import scrape_copa_libertadores
from src.football.qualif_wc_amerique_du_sud import scrape_qualif_wc_amerique_du_sud
from src.football.fa_cup import scrape_fa_cup
from src.football.league_cup_efl import scrape_league_cup_efl
from src.football.premier_league import scrape_premier_league
from src.football.championship import scrape_championship
from src.football.community_shield import scrape_community_shield
from src.football.saudi_pro_league import scrape_saudi_pro_league
from src.football.primera_division_argentine import scrape_primera_division_argentine
from src.football.a_league import scrape_a_league
from src.football.bundesliga_autriche import scrape_bundesliga_autriche
from src.football.premiere_division_azerbaidjan import scrape_premiere_division_azerbaidjan
from src.football.jupiler_pro_ligue import scrape_jupiler_pro_ligue
from src.football.premier_liga_bosnie import scrape_premier_liga_bosnie
from src.football.a_pfg import scrape_a_pfg
from src.football.primera_division_chili import scrape_primera_division_chili
from src.football.division_1_chypre import scrape_division_1_chypre
from src.football.liga_postobon_i import scrape_liga_postobon_i
from src.football.k_league_1 import scrape_k_league_1
from src.football.hnl_1 import scrape_hnl_1
from src.football.superligaen import scrape_superligaen
from src.football.premiership_ecosse import scrape_premiership_ecosse
from src.football.serie_a_equateur import scrape_serie_a_equateur
from src.football.coupe_du_roi import scrape_coupe_du_roi
from src.football.liga_adelante import scrape_liga_adelante
from src.football.la_liga import scrape_la_liga
from src.football.meistriliiga import scrape_meistriliiga
from src.football.major_league_soccer import scrape_major_league_soccer
from src.football.ligue_europa import scrape_ligue_europa
from src.football.ligue_des_nations import scrape_ligue_des_nations
from src.football.champions_league import scrape_champions_league
from src.football.uefa_conference_league import scrape_uefa_conference_league
from src.football.super_league_grece import scrape_super_league_grece
from src.football.nb_i_hongrie import scrape_nb_i_hongrie
from src.football.premiership_irlande_du_nord import scrape_premiership_irlande_du_nord
from src.football.winner_league import scrape_winner_league
from src.football.coupe_d_italie import scrape_coupe_d_italie
from src.football.serie_a import scrape_serie_a
from src.football.serie_b import scrape_serie_b
from src.football.j_league import scrape_j_league
from src.football.virsliga import scrape_virsliga
from src.football.a_lyga import scrape_a_lyga
from src.football.bov_premier_division import scrape_bov_premier_division
from src.football.super_league_maroc import scrape_super_league_maroc
from src.football.liga_mx import scrape_liga_mx
from src.football.concacaf_ligue_des_nations import scrape_concacaf_ligue_des_nations
from src.football.qualif_wc_europe import scrape_qualif_wc_europe
from src.football.eliteserien import scrape_eliteserien
from src.football.primera_division_paraguay import scrape_primera_division_paraguay
from src.football.league_of_wales import scrape_league_of_wales
from src.football.casino_eredivisie import scrape_casino_eredivisie
from src.football.orange_ekstraklasa import scrape_orange_ekstraklasa
from src.football.liga_2_cabovisao import scrape_liga_2_cabovisao
from src.football.primeira_liga import scrape_primeira_liga
from src.football.premier_division_irlande import scrape_premier_division_irlande
from src.football.liga_1_roumanie import scrape_liga_1_roumanie
from src.football.het_liga import scrape_het_liga
from src.football.super_league_serbie import scrape_super_league_serbie
from src.football.superliga_slovaquie import scrape_superliga_slovaquie
from src.football.prvaliga import scrape_prvaliga
from src.football.super_league_suisse import scrape_super_league_suisse
from src.football.allsvenskan import scrape_allsvenskan
from src.football.super_ligi import scrape_super_ligi
from src.football.premier_liga_ukraine import scrape_premier_liga_ukraine
from src.football.qualif_wc_afrique import scrape_qualif_wc_afrique
from src.football.qualif_wc_asie import scrape_qualif_wc_asie
from src.football.asian_champions_league import scrape_asian_champions_league
from src.football.erovnuli_liga import scrape_erovnuli_liga
from src.football.veikkausliiga import scrape_veikkausliiga
from src.football.urvalsdeild import scrape_urvalsdeild
from src.football.coupe_du_monde_des_clubs import scrape_coupe_du_monde_des_clubs
from src.football.copa_sudamericana import scrape_copa_sudamericana
from src.football.brasileirao import scrape_brasileirao
from src.football.ligue_des_nations_f import scrape_ligue_des_nations_f
from src.football.amical_international_w import scrape_amical_international_w
from src.football.amical_international import scrape_amical_international
from src.football.qualif_wc_concacaf import scrape_qualif_wc_concacaf
from src.football.euro_u21_qualif import scrape_euro_u21_qualif
from src.football.super_league_chine import scrape_super_league_chine
from src.football.euro_femmes import scrape_euro_femmes
from src.football.concacaf_gold_cup import scrape_concacaf_gold_cup
from src.football.leagues_cup import scrape_leagues_cup
from src.football.bgl_ligue import scrape_bgl_ligue
from src.football.ligue_des_champions_f import scrape_ligue_des_champions_f
from src.football.coupe_d_asie import scrape_coupe_d_asie

# TENNIS
from src.tennis.atp_miami import scrape_atp_miami
from src.tennis.wta_miami import scrape_wta_miami
from src.tennis.atp_bucharest import scrape_atp_bucharest
from src.tennis.atp_houston import scrape_atp_houston
from src.tennis.atp_marrakech import scrape_atp_marrakech
from src.tennis.wta_bogota import scrape_wta_bogota
from src.tennis.wta_charleston import scrape_wta_charleston
from src.tennis.atp_monte_carlo import scrape_atp_monte_carlo
from src.tennis.atp_barcelone import scrape_atp_barcelone
from src.tennis.atp_munich import scrape_atp_munich
from src.tennis.wta_rouen import scrape_wta_rouen
from src.tennis.wta_stuttgart import scrape_wta_stuttgart
from src.tennis.wta_madrid import scrape_wta_madrid
from src.tennis.atp_madrid import scrape_atp_madrid
from src.tennis.atp_rome import scrape_atp_rome
from src.tennis.wta_rome import scrape_wta_rome
from src.tennis.wta_strasbourg import scrape_wta_strasbourg
from src.tennis.wta_rabat import scrape_wta_rabat
from src.tennis.atp_geneve import scrape_atp_geneve
from src.tennis.atp_hambourg import scrape_atp_hambourg
from src.tennis.roland_garros_m import scrape_roland_garros_m
from src.tennis.roland_garros_w import scrape_roland_garros_w
from src.tennis.roland_garros_doubles_m import scrape_roland_garros_doubles_m
from src.tennis.roland_garros_doubles_w import scrape_roland_garros_doubles_w
from src.tennis.roland_garros_doubles_x import scrape_roland_garros_doubles_x
from src.tennis.wta_londres import scrape_wta_londres
from src.tennis.atp_hertogenbosch import scrape_atp_hertogenbosch
from src.tennis.wta_hertogenbosch import scrape_wta_hertogenbosch
from src.tennis.atp_stuttgart import scrape_atp_stuttgart
from src.tennis.atp_london import scrape_atp_london
from src.tennis.atp_halle import scrape_atp_halle
from src.tennis.wta_berlin import scrape_wta_berlin
from src.tennis.wta_nottingham import scrape_wta_nottingham
from src.tennis.atp_majorque import scrape_atp_majorque
from src.tennis.atp_eastbourne import scrape_atp_eastbourne
from src.tennis.wta_bad_homburg import scrape_wta_bad_homburg
from src.tennis.wta_eastbourne import scrape_wta_eastbourne
from src.tennis.atp_wimbledon import scrape_atp_wimbledon
from src.tennis.wta_wimbledon import scrape_wta_wimbledon
from src.tennis.wimbledon_double_m import scrape_wimbledon_double_m
from src.tennis.wimbledon_double_w import scrape_wimbledon_double_w
from src.tennis.wimbledon_double_x import scrape_wimbledon_double_x
from src.tennis.atp_los_cabos import scrape_atp_los_cabos
from src.tennis.atp_bastad import scrape_atp_bastad
from src.tennis.atp_gstaad import scrape_atp_gstaad
from src.tennis.wta_iasi import scrape_wta_iasi
from src.tennis.wta_hamburg import scrape_wta_hamburg
from src.tennis.atp_kitzbuhel import scrape_atp_kitzbuhel
from src.tennis.wta_prague import scrape_wta_prague
from src.tennis.atp_umag import scrape_atp_umag
from src.tennis.atp_washington import scrape_atp_washington
from src.tennis.wta_washington import scrape_wta_washington
from src.tennis.wta_montreal import scrape_wta_montreal
from src.tennis.atp_toronto import scrape_atp_toronto
from src.tennis.atp_cincinnati import scrape_atp_cincinnati
from src.tennis.wta_cincinnati import scrape_wta_cincinnati
from src.tennis.wta_monterrey import scrape_wta_monterrey
from src.tennis.atp_winston_salem import scrape_atp_winston_salem
from src.tennis.wta_cleveland import scrape_wta_cleveland
from src.tennis.atp_us_open import scrape_atp_us_open
from src.tennis.wta_us_open import scrape_wta_us_open
from src.tennis.atp_us_open_double import scrape_atp_us_open_double
from src.tennis.wta_us_open_double import scrape_wta_us_open_double
from src.tennis.wta_guadalajara import scrape_wta_guadalajara
from src.tennis.wta_sao_paulo import scrape_wta_sao_paulo
from src.tennis.coupe_davis import scrape_coupe_davis
from src.tennis.wta_seoul import scrape_wta_seoul
from src.tennis.atp_chengdu import scrape_atp_chengdu
from src.tennis.atp_hangzhou import scrape_atp_hangzhou
from src.tennis.wta_pekin import scrape_wta_pekin
from src.tennis.atp_tokyo import scrape_atp_tokyo
from src.tennis.atp_pekin import scrape_atp_pekin
from src.tennis.atp_shanghai import scrape_atp_shanghai
from src.tennis.wta_wuhan import scrape_wta_wuhan
from src.tennis.atp_almaty import scrape_atp_almaty
from src.tennis.atp_bruxelles import scrape_atp_bruxelles
from src.tennis.atp_stockholm import scrape_atp_stockholm
from src.tennis.wta_osaka import scrape_wta_osaka
from src.tennis.wta_ningbo import scrape_wta_ningbo
from src.tennis.wta_tokyo import scrape_wta_tokyo
from src.tennis.atp_vienne import scrape_atp_vienne
from src.tennis.atp_basel import scrape_atp_basel
from src.tennis.wta_guangzhou import scrape_wta_guangzhou
from src.tennis.atp_paris import scrape_atp_paris
from src.tennis.wta_chennai import scrape_wta_chennai
from src.tennis.wta_hong_kong import scrape_wta_hong_kong
from src.tennis.wta_jiujiang import scrape_wta_jiujiang
from src.tennis.wta_finals_riyadh import scrape_wta_finals_riyadh
from src.tennis.atp_athens import scrape_atp_athens

# BASKETBALL
from src.basketball.nba import scrape_nba
from src.basketball.bundesliga import scrape_bundesliga
from src.basketball.nbl import scrape_nbl
from src.basketball.euroligue import scrape_euroligue
from src.basketball.eurocup import scrape_eurocup
from src.basketball.league_aba import scrape_league_aba
from src.basketball.euroligue_women import scrape_euroligue_women
from src.basketball.coupe_d_europe_fiba import scrape_coupe_d_europe_fiba
from src.basketball.eurocup_women import scrape_eurocup_women
from src.basketball.ligue_des_champions import scrape_ligue_des_champions
from src.basketball.betclic_elite import scrape_betclic_elite
from src.basketball.a1 import scrape_a1
from src.basketball.lega_a import scrape_lega_a
from src.basketball.serie_a2 import scrape_serie_a2

# RUGBY
from src.rugby.top_14 import scrape_top_14
from src.rugby.pro_d2 import scrape_pro_d2
from src.rugby.test_match import scrape_test_match


# ============================================================================
# Configuration RabbitMQ
# ============================================================================
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'gig_user')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'gig_password')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'scraping_tasks')

# ============================================================================
# Registre des scrapers disponibles (212 total)
# ============================================================================
SCRAPERS_REGISTRY: Dict[str, Callable] = {}

# Ajout automatique de tous les scrapers au registry
SCRAPERS_REGISTRY['football.coupe_de_france'] = scrape_coupe_de_france
SCRAPERS_REGISTRY['football.ligue_1'] = scrape_ligue_1
SCRAPERS_REGISTRY['football.ligue_2'] = scrape_ligue_2
SCRAPERS_REGISTRY['football.division_1_algerie'] = scrape_division_1_algerie
SCRAPERS_REGISTRY['football.bundesliga_2'] = scrape_bundesliga_2
SCRAPERS_REGISTRY['football.bundesliga'] = scrape_bundesliga
SCRAPERS_REGISTRY['football.pokal_cup'] = scrape_pokal_cup
SCRAPERS_REGISTRY['football.copa_libertadores'] = scrape_copa_libertadores
SCRAPERS_REGISTRY['football.qualif_wc_amerique_du_sud'] = scrape_qualif_wc_amerique_du_sud
SCRAPERS_REGISTRY['football.fa_cup'] = scrape_fa_cup
SCRAPERS_REGISTRY['football.league_cup_efl'] = scrape_league_cup_efl
SCRAPERS_REGISTRY['football.premier_league'] = scrape_premier_league
SCRAPERS_REGISTRY['football.championship'] = scrape_championship
SCRAPERS_REGISTRY['football.community_shield'] = scrape_community_shield
SCRAPERS_REGISTRY['football.saudi_pro_league'] = scrape_saudi_pro_league
SCRAPERS_REGISTRY['football.primera_division_argentine'] = scrape_primera_division_argentine
SCRAPERS_REGISTRY['football.a_league'] = scrape_a_league
SCRAPERS_REGISTRY['football.bundesliga_autriche'] = scrape_bundesliga_autriche
SCRAPERS_REGISTRY['football.premiere_division_azerbaidjan'] = scrape_premiere_division_azerbaidjan
SCRAPERS_REGISTRY['football.jupiler_pro_ligue'] = scrape_jupiler_pro_ligue
SCRAPERS_REGISTRY['football.premier_liga_bosnie'] = scrape_premier_liga_bosnie
SCRAPERS_REGISTRY['football.a_pfg'] = scrape_a_pfg
SCRAPERS_REGISTRY['football.primera_division_chili'] = scrape_primera_division_chili
SCRAPERS_REGISTRY['football.1ere_division_chypre'] = scrape_division_1_chypre
SCRAPERS_REGISTRY['football.liga_postobon_i'] = scrape_liga_postobon_i
SCRAPERS_REGISTRY['football.k_league_1'] = scrape_k_league_1
SCRAPERS_REGISTRY['football.1_hnl'] = scrape_hnl_1
SCRAPERS_REGISTRY['football.superligaen'] = scrape_superligaen
SCRAPERS_REGISTRY['football.premiership_ecosse'] = scrape_premiership_ecosse
SCRAPERS_REGISTRY['football.serie_a_equateur'] = scrape_serie_a_equateur
SCRAPERS_REGISTRY['football.coupe_du_roi'] = scrape_coupe_du_roi
SCRAPERS_REGISTRY['football.liga_adelante'] = scrape_liga_adelante
SCRAPERS_REGISTRY['football.la_liga'] = scrape_la_liga
SCRAPERS_REGISTRY['football.meistriliiga'] = scrape_meistriliiga
SCRAPERS_REGISTRY['football.major_league_soccer'] = scrape_major_league_soccer
SCRAPERS_REGISTRY['football.ligue_europa'] = scrape_ligue_europa
SCRAPERS_REGISTRY['football.ligue_des_nations'] = scrape_ligue_des_nations
SCRAPERS_REGISTRY['football.champions_league'] = scrape_champions_league
SCRAPERS_REGISTRY['football.uefa_conference_league'] = scrape_uefa_conference_league
SCRAPERS_REGISTRY['football.super_league_grece'] = scrape_super_league_grece
SCRAPERS_REGISTRY['football.nb_i_hongrie'] = scrape_nb_i_hongrie
SCRAPERS_REGISTRY['football.premiership_irlande_du_nord'] = scrape_premiership_irlande_du_nord
SCRAPERS_REGISTRY['football.winner_league'] = scrape_winner_league
SCRAPERS_REGISTRY['football.coupe_d_italie'] = scrape_coupe_d_italie
SCRAPERS_REGISTRY['football.serie_a'] = scrape_serie_a
SCRAPERS_REGISTRY['football.serie_b'] = scrape_serie_b
SCRAPERS_REGISTRY['football.j_league'] = scrape_j_league
SCRAPERS_REGISTRY['football.virsliga'] = scrape_virsliga
SCRAPERS_REGISTRY['football.a_lyga'] = scrape_a_lyga
SCRAPERS_REGISTRY['football.bov_premier_division'] = scrape_bov_premier_division
SCRAPERS_REGISTRY['football.super_league_maroc'] = scrape_super_league_maroc
SCRAPERS_REGISTRY['football.liga_mx'] = scrape_liga_mx
SCRAPERS_REGISTRY['football.concacaf_ligue_des_nations'] = scrape_concacaf_ligue_des_nations
SCRAPERS_REGISTRY['football.qualif_wc_europe'] = scrape_qualif_wc_europe
SCRAPERS_REGISTRY['football.eliteserien'] = scrape_eliteserien
SCRAPERS_REGISTRY['football.primera_division_paraguay'] = scrape_primera_division_paraguay
SCRAPERS_REGISTRY['football.league_of_wales'] = scrape_league_of_wales
SCRAPERS_REGISTRY['football.casino_eredivisie'] = scrape_casino_eredivisie
SCRAPERS_REGISTRY['football.orange_ekstraklasa'] = scrape_orange_ekstraklasa
SCRAPERS_REGISTRY['football.liga_2_cabovisao'] = scrape_liga_2_cabovisao
SCRAPERS_REGISTRY['football.primeira_liga'] = scrape_primeira_liga
SCRAPERS_REGISTRY['football.premier_division_irlande'] = scrape_premier_division_irlande
SCRAPERS_REGISTRY['football.liga_1_roumanie'] = scrape_liga_1_roumanie
SCRAPERS_REGISTRY['football.het_liga'] = scrape_het_liga
SCRAPERS_REGISTRY['football.super_league_serbie'] = scrape_super_league_serbie
SCRAPERS_REGISTRY['football.superliga_slovaquie'] = scrape_superliga_slovaquie
SCRAPERS_REGISTRY['football.prvaliga'] = scrape_prvaliga
SCRAPERS_REGISTRY['football.super_league_suisse'] = scrape_super_league_suisse
SCRAPERS_REGISTRY['football.allsvenskan'] = scrape_allsvenskan
SCRAPERS_REGISTRY['football.super_ligi'] = scrape_super_ligi
SCRAPERS_REGISTRY['football.premier_liga_ukraine'] = scrape_premier_liga_ukraine
SCRAPERS_REGISTRY['football.qualif_wc_afrique'] = scrape_qualif_wc_afrique
SCRAPERS_REGISTRY['football.qualif_wc_asie'] = scrape_qualif_wc_asie
SCRAPERS_REGISTRY['football.asian_champions_league'] = scrape_asian_champions_league
SCRAPERS_REGISTRY['football.erovnuli_liga'] = scrape_erovnuli_liga
SCRAPERS_REGISTRY['football.veikkausliiga'] = scrape_veikkausliiga
SCRAPERS_REGISTRY['football.urvalsdeild'] = scrape_urvalsdeild
SCRAPERS_REGISTRY['football.coupe_du_monde_des_clubs'] = scrape_coupe_du_monde_des_clubs
SCRAPERS_REGISTRY['football.copa_sudamericana'] = scrape_copa_sudamericana
SCRAPERS_REGISTRY['football.brasileirao'] = scrape_brasileirao
SCRAPERS_REGISTRY['football.ligue_des_nations_f'] = scrape_ligue_des_nations_f
SCRAPERS_REGISTRY['football.amical_international_w'] = scrape_amical_international_w
SCRAPERS_REGISTRY['football.amical_international'] = scrape_amical_international
SCRAPERS_REGISTRY['football.qualif_wc_concacaf'] = scrape_qualif_wc_concacaf
SCRAPERS_REGISTRY['football.euro_u21_qualif'] = scrape_euro_u21_qualif
SCRAPERS_REGISTRY['football.super_league_chine'] = scrape_super_league_chine
SCRAPERS_REGISTRY['football.euro_femmes'] = scrape_euro_femmes
SCRAPERS_REGISTRY['football.concacaf_gold_cup'] = scrape_concacaf_gold_cup
SCRAPERS_REGISTRY['football.leagues_cup'] = scrape_leagues_cup
SCRAPERS_REGISTRY['football.bgl_ligue'] = scrape_bgl_ligue
SCRAPERS_REGISTRY['football.ligue_des_champions_f'] = scrape_ligue_des_champions_f
SCRAPERS_REGISTRY['football.coupe_d_asie'] = scrape_coupe_d_asie
# Alias mappings (point to existing scrapers)
SCRAPERS_REGISTRY['football.club_world_cup'] = scrape_coupe_du_monde_des_clubs
SCRAPERS_REGISTRY['football.conference_league'] = scrape_uefa_conference_league
SCRAPERS_REGISTRY['football.coupe_asie'] = scrape_coupe_d_asie
SCRAPERS_REGISTRY['football.division_1_chypre'] = scrape_division_1_chypre
SCRAPERS_REGISTRY['football.ekstraklasa'] = scrape_orange_ekstraklasa
SCRAPERS_REGISTRY['football.eredivisie'] = scrape_casino_eredivisie
SCRAPERS_REGISTRY['football.europa_league'] = scrape_ligue_europa
SCRAPERS_REGISTRY['football.hnl_1'] = scrape_hnl_1
SCRAPERS_REGISTRY['football.hnl_croatie'] = scrape_hnl_1
SCRAPERS_REGISTRY['football.liga_2_portugal'] = scrape_liga_2_cabovisao
SCRAPERS_REGISTRY['football.liga_postobon'] = scrape_liga_postobon_i
SCRAPERS_REGISTRY['football.ligue_nations_f'] = scrape_ligue_des_nations_f
SCRAPERS_REGISTRY['football.mls'] = scrape_major_league_soccer
SCRAPERS_REGISTRY['football.qualif_world_cup_south_america'] = scrape_qualif_wc_amerique_du_sud
SCRAPERS_REGISTRY['football.ucl_femmes'] = scrape_ligue_des_champions_f
SCRAPERS_REGISTRY['tennis.atp_miami'] = scrape_atp_miami
SCRAPERS_REGISTRY['tennis.wta_miami'] = scrape_wta_miami
SCRAPERS_REGISTRY['tennis.atp_bucharest'] = scrape_atp_bucharest
SCRAPERS_REGISTRY['tennis.atp_houston'] = scrape_atp_houston
SCRAPERS_REGISTRY['tennis.atp_marrakech'] = scrape_atp_marrakech
SCRAPERS_REGISTRY['tennis.wta_bogota'] = scrape_wta_bogota
SCRAPERS_REGISTRY['tennis.wta_charleston'] = scrape_wta_charleston
SCRAPERS_REGISTRY['tennis.atp_monte_carlo'] = scrape_atp_monte_carlo
SCRAPERS_REGISTRY['tennis.atp_barcelone'] = scrape_atp_barcelone
SCRAPERS_REGISTRY['tennis.atp_munich'] = scrape_atp_munich
SCRAPERS_REGISTRY['tennis.wta_rouen'] = scrape_wta_rouen
SCRAPERS_REGISTRY['tennis.wta_stuttgart'] = scrape_wta_stuttgart
SCRAPERS_REGISTRY['tennis.wta_madrid'] = scrape_wta_madrid
SCRAPERS_REGISTRY['tennis.atp_madrid'] = scrape_atp_madrid
SCRAPERS_REGISTRY['tennis.atp_rome'] = scrape_atp_rome
SCRAPERS_REGISTRY['tennis.wta_rome'] = scrape_wta_rome
SCRAPERS_REGISTRY['tennis.wta_strasbourg'] = scrape_wta_strasbourg
SCRAPERS_REGISTRY['tennis.wta_rabat'] = scrape_wta_rabat
SCRAPERS_REGISTRY['tennis.atp_geneve'] = scrape_atp_geneve
SCRAPERS_REGISTRY['tennis.atp_hambourg'] = scrape_atp_hambourg
SCRAPERS_REGISTRY['tennis.roland_garros_m'] = scrape_roland_garros_m
SCRAPERS_REGISTRY['tennis.roland_garros_w'] = scrape_roland_garros_w
SCRAPERS_REGISTRY['tennis.roland_garros_doubles_m'] = scrape_roland_garros_doubles_m
SCRAPERS_REGISTRY['tennis.roland_garros_doubles_w'] = scrape_roland_garros_doubles_w
SCRAPERS_REGISTRY['tennis.roland_garros_doubles_x'] = scrape_roland_garros_doubles_x
SCRAPERS_REGISTRY['tennis.wta_londres'] = scrape_wta_londres
SCRAPERS_REGISTRY['tennis.atp_hertogenbosch'] = scrape_atp_hertogenbosch
SCRAPERS_REGISTRY['tennis.wta_hertogenbosch'] = scrape_wta_hertogenbosch
SCRAPERS_REGISTRY['tennis.atp_stuttgart'] = scrape_atp_stuttgart
SCRAPERS_REGISTRY['tennis.atp_london'] = scrape_atp_london
SCRAPERS_REGISTRY['tennis.atp_halle'] = scrape_atp_halle
SCRAPERS_REGISTRY['tennis.wta_berlin'] = scrape_wta_berlin
SCRAPERS_REGISTRY['tennis.wta_nottingham'] = scrape_wta_nottingham
SCRAPERS_REGISTRY['tennis.atp_majorque'] = scrape_atp_majorque
SCRAPERS_REGISTRY['tennis.atp_eastbourne'] = scrape_atp_eastbourne
SCRAPERS_REGISTRY['tennis.wta_bad_homburg'] = scrape_wta_bad_homburg
SCRAPERS_REGISTRY['tennis.wta_eastbourne'] = scrape_wta_eastbourne
SCRAPERS_REGISTRY['tennis.atp_wimbledon'] = scrape_atp_wimbledon
SCRAPERS_REGISTRY['tennis.wta_wimbledon'] = scrape_wta_wimbledon
SCRAPERS_REGISTRY['tennis.wimbledon_double_m'] = scrape_wimbledon_double_m
SCRAPERS_REGISTRY['tennis.wimbledon_double_w'] = scrape_wimbledon_double_w
SCRAPERS_REGISTRY['tennis.wimbledon_double_x'] = scrape_wimbledon_double_x
SCRAPERS_REGISTRY['tennis.atp_los_cabos'] = scrape_atp_los_cabos
SCRAPERS_REGISTRY['tennis.atp_bastad'] = scrape_atp_bastad
SCRAPERS_REGISTRY['tennis.atp_gstaad'] = scrape_atp_gstaad
SCRAPERS_REGISTRY['tennis.wta_iasi'] = scrape_wta_iasi
SCRAPERS_REGISTRY['tennis.wta_hamburg'] = scrape_wta_hamburg
SCRAPERS_REGISTRY['tennis.atp_kitzbuhel'] = scrape_atp_kitzbuhel
SCRAPERS_REGISTRY['tennis.wta_prague'] = scrape_wta_prague
SCRAPERS_REGISTRY['tennis.atp_umag'] = scrape_atp_umag
SCRAPERS_REGISTRY['tennis.atp_washington'] = scrape_atp_washington
SCRAPERS_REGISTRY['tennis.wta_washington'] = scrape_wta_washington
SCRAPERS_REGISTRY['tennis.wta_montreal'] = scrape_wta_montreal
SCRAPERS_REGISTRY['tennis.atp_toronto'] = scrape_atp_toronto
SCRAPERS_REGISTRY['tennis.atp_cincinnati'] = scrape_atp_cincinnati
SCRAPERS_REGISTRY['tennis.wta_cincinnati'] = scrape_wta_cincinnati
SCRAPERS_REGISTRY['tennis.wta_monterrey'] = scrape_wta_monterrey
SCRAPERS_REGISTRY['tennis.atp_winston_salem'] = scrape_atp_winston_salem
SCRAPERS_REGISTRY['tennis.wta_cleveland'] = scrape_wta_cleveland
SCRAPERS_REGISTRY['tennis.atp_us_open'] = scrape_atp_us_open
SCRAPERS_REGISTRY['tennis.wta_us_open'] = scrape_wta_us_open
SCRAPERS_REGISTRY['tennis.atp_us_open_double'] = scrape_atp_us_open_double
SCRAPERS_REGISTRY['tennis.wta_us_open_double'] = scrape_wta_us_open_double
SCRAPERS_REGISTRY['tennis.wta_guadalajara'] = scrape_wta_guadalajara
SCRAPERS_REGISTRY['tennis.wta_sao_paulo'] = scrape_wta_sao_paulo
SCRAPERS_REGISTRY['tennis.coupe_davis'] = scrape_coupe_davis
SCRAPERS_REGISTRY['tennis.wta_seoul'] = scrape_wta_seoul
SCRAPERS_REGISTRY['tennis.atp_chengdu'] = scrape_atp_chengdu
SCRAPERS_REGISTRY['tennis.atp_hangzhou'] = scrape_atp_hangzhou
SCRAPERS_REGISTRY['tennis.wta_pekin'] = scrape_wta_pekin
SCRAPERS_REGISTRY['tennis.atp_tokyo'] = scrape_atp_tokyo
SCRAPERS_REGISTRY['tennis.atp_pekin'] = scrape_atp_pekin
SCRAPERS_REGISTRY['tennis.atp_shanghai'] = scrape_atp_shanghai
SCRAPERS_REGISTRY['tennis.wta_wuhan'] = scrape_wta_wuhan
SCRAPERS_REGISTRY['tennis.atp_almaty'] = scrape_atp_almaty
SCRAPERS_REGISTRY['tennis.atp_bruxelles'] = scrape_atp_bruxelles
SCRAPERS_REGISTRY['tennis.atp_stockholm'] = scrape_atp_stockholm
SCRAPERS_REGISTRY['tennis.wta_osaka'] = scrape_wta_osaka
SCRAPERS_REGISTRY['tennis.wta_ningbo'] = scrape_wta_ningbo
SCRAPERS_REGISTRY['tennis.wta_tokyo'] = scrape_wta_tokyo
SCRAPERS_REGISTRY['tennis.atp_vienne'] = scrape_atp_vienne
SCRAPERS_REGISTRY['tennis.atp_basel'] = scrape_atp_basel
SCRAPERS_REGISTRY['tennis.wta_guangzhou'] = scrape_wta_guangzhou
SCRAPERS_REGISTRY['tennis.atp_paris'] = scrape_atp_paris
SCRAPERS_REGISTRY['tennis.wta_chennai'] = scrape_wta_chennai
SCRAPERS_REGISTRY['tennis.wta_hong_kong'] = scrape_wta_hong_kong
SCRAPERS_REGISTRY['tennis.wta_jiujiang'] = scrape_wta_jiujiang
SCRAPERS_REGISTRY['tennis.wta_finals_riyadh'] = scrape_wta_finals_riyadh
SCRAPERS_REGISTRY['tennis.atp_athens'] = scrape_atp_athens
SCRAPERS_REGISTRY['basketball.nba'] = scrape_nba
SCRAPERS_REGISTRY['basketball.bundesliga'] = scrape_bundesliga
SCRAPERS_REGISTRY['basketball.nbl'] = scrape_nbl
SCRAPERS_REGISTRY['basketball.euroligue'] = scrape_euroligue
SCRAPERS_REGISTRY['basketball.eurocup'] = scrape_eurocup
SCRAPERS_REGISTRY['basketball.league_aba'] = scrape_league_aba
SCRAPERS_REGISTRY['basketball.euroligue_women'] = scrape_euroligue_women
SCRAPERS_REGISTRY['basketball.coupe_d_europe_fiba'] = scrape_coupe_d_europe_fiba
SCRAPERS_REGISTRY['basketball.eurocup_women'] = scrape_eurocup_women
SCRAPERS_REGISTRY['basketball.ligue_des_champions'] = scrape_ligue_des_champions
SCRAPERS_REGISTRY['basketball.betclic_elite'] = scrape_betclic_elite
SCRAPERS_REGISTRY['basketball.a1'] = scrape_a1
SCRAPERS_REGISTRY['basketball.lega_a'] = scrape_lega_a
SCRAPERS_REGISTRY['basketball.serie_a2'] = scrape_serie_a2
SCRAPERS_REGISTRY['rugby.top_14'] = scrape_top_14
SCRAPERS_REGISTRY['rugby.pro_d2'] = scrape_pro_d2
SCRAPERS_REGISTRY['rugby.test_match'] = scrape_test_match


def connect_rabbitmq(max_retries=10, retry_delay=5):
    """Connexion à RabbitMQ avec retry"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Tentative de connexion à RabbitMQ ({attempt}/{max_retries})...")
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=5672,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            print("Connecté à RabbitMQ")
            return connection
        except Exception as e:
            print(f"Erreur connexion RabbitMQ (tentative {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Nouvelle tentative dans {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print("Échec de connexion après toutes les tentatives")
                raise


def callback(ch, method, properties, body):
    """
    Callback appelé quand un message arrive dans la queue
    
    Format attendu du message JSON:
    {
        "scraper": "football.ligue_1",
        "params": {
            "url": "...",
            "options": {...}
        }
    }
    """
    try:
        # Décoder le message
        message = json.loads(body.decode('utf-8'))
        scraper_name = message.get('scraper')
        params = message.get('params', {})
        
        print(f"\n{'='*60}")
        print(f"NOUVELLE TÂCHE REÇUE")
        print(f"{'='*60}")
        print(f"Scraper: {scraper_name}")
        print(f"Params: {params}")
        print(f"Heure: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Vérifier que le scraper existe
        if scraper_name not in SCRAPERS_REGISTRY:
            print(f"ERREUR: Scraper inconnu '{scraper_name}'")
            print(f"\nScrapers disponibles:")
            for sport, scrapers in get_scrapers_by_sport().items():
                print(f"   {sport}:")
                for s in scrapers:
                    print(f"      - {s}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return
        
        # Récupérer et exécuter le scraper
        scraper_func = SCRAPERS_REGISTRY[scraper_name]
        print(f"Démarrage du scraper: {scraper_name}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        result = scraper_func(**params)
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print(f"SCRAPING TERMINÉ")
        print(f"{'='*60}")
        print(f"Durée: {elapsed_time:.2f}s")
        print(f"Résultat: {result}")
        print(f"{'='*60}\n")
        
        # Acquitter le message (succès)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON: {e}")
        print(f"Body reçu: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERREUR DURANT LE SCRAPING")
        print(f"{'='*60}")
        print(f"Message: {e}")
        print(f"Stacktrace:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        # Rejeter le message sans requeue pour éviter les boucles infinies
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def get_scrapers_by_sport():
    """Retourne les scrapers organisés par sport"""
    sports = {
        'Football': [],
        'Basketball': [],
        'Rugby': [],
        'Tennis': []
    }
    
    for scraper in SCRAPERS_REGISTRY.keys():
        if scraper.startswith('football.'):
            sports['Football'].append(scraper)
        elif scraper.startswith('basketball.'):
            sports['Basketball'].append(scraper)
        elif scraper.startswith('rugby.'):
            sports['Rugby'].append(scraper)
        elif scraper.startswith('tennis.'):
            sports['Tennis'].append(scraper)
    
    return sports


def print_startup_banner():
    """Affiche la bannière de démarrage"""
    print("\n" + "="*60)
    print("WORKER DE SCRAPING MULTI-SPORTS - GIG BENCHMARK")
    print("="*60)
    print(f"RabbitMQ Host: {RABBITMQ_HOST}")
    print(f"RabbitMQ User: {RABBITMQ_USER}")
    print(f"Queue: {RABBITMQ_QUEUE}")
    print("="*60)
    
    # Afficher les scrapers chargés par sport
    print(f"\nSCRAPERS DISPONIBLES ({len(SCRAPERS_REGISTRY)}):")
    sports = get_scrapers_by_sport()
    for sport, scrapers in sports.items():
        if scrapers:
            print(f"\n{sport} ({len(scrapers)}):")
            for scraper in sorted(scrapers)[:5]:  # Afficher les 5 premiers
                print(f"   ✓ {scraper}")
            if len(scrapers) > 5:
                print(f"   ... et {len(scrapers) - 5} autres")
    
    print("\n" + "="*60)
    print("COMMENT ENVOYER UNE TÂCHE:")
    print("="*60)
    print("Depuis Python:")
    print("  import pika, json")
    print("  conn = pika.BlockingConnection(...)")
    print("  ch = conn.channel()")
    print("  ch.basic_publish('', 'scraping_tasks',")
    print("    json.dumps({'scraper': 'football.ligue_1'}))")
    print("\nDepuis Django:")
    print("  python manage.py scrape football.ligue_1")
    print("\nDepuis le conteneur scraping:")
    print("  python send_task.py football.ligue_1")
    print("="*60 + "\n")


def main():
    """Fonction principale du worker"""
    print_startup_banner()
    
    # Connexion à RabbitMQ
    connection = connect_rabbitmq()
    channel = connection.channel()
    
    # Déclarer la queue (durable = survit aux redémarrages)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    
    # Configurer la consommation
    # prefetch_count=1 : Un seul message à la fois (évite la surcharge)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=False  # Acquittement manuel
    )
    
    print("EN ATTENTE DE TÂCHES...")
    print("Le worker est prêt à traiter les demandes de scraping")
    print("="*60 + "\n")
    
    try:
        # Démarrer la consommation (boucle infinie)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
        channel.stop_consuming()
    except Exception as e:
        print(f"\nErreur fatale: {e}")
        traceback.print_exc()
    finally:
        connection.close()
        print("\nWorker arrêté proprement")


if __name__ == "__main__":
    main()
